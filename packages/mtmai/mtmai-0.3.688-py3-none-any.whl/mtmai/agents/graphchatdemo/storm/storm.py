import logging
from functools import lru_cache
from typing import Annotated

import fastapi
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.runnables import chain as as_runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from mtmai.llm.llm import get_fast_llm, get_llm_long_context_default
from mtmai.models.chat import MtmChatMessage
from mtmai.mtlibs import mtutils
from mtmai.mtlibs.aiutils import wf_to_chatstreams

router = APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)


direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific.",
        ),
        ("user", "{topic}"),
    ]
)


class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Content of the subsection")

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.description}".strip()


class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    description: str = Field(..., title="Content of the section")
    subsections: list[Subsection] | None = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Wikipedia page.",
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            f"### {subsection.subsection_title}\n\n{subsection.description}"
            for subsection in self.subsections or []
        )
        return f"## {self.section_title}\n\n{self.description}\n\n{subsections}".strip()


class Outline(BaseModel):
    page_title: str = Field(..., title="Title of the Wikipedia page")
    sections: list[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the Wikipedia page.",
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{sections}".strip()


generate_outline_direct = (
    direct_gen_outline_prompt | get_fast_llm().with_structured_output(Outline)
)


# Expand Topics

gen_related_topics_prompt = ChatPromptTemplate.from_template(
    """I'm writing a Wikipedia page for a topic mentioned below. Please identify and recommend some Wikipedia pages on closely related subjects. I'm looking for examples that provide insights into interesting aspects commonly associated with this topic, or examples that help me understand the typical content and structure included in Wikipedia pages for similar topics.

Please list the as many subjects and urls as you can.

Topic of interest: {topic}
"""
)


class RelatedSubjects(BaseModel):
    topics: list[str] = Field(
        description="Comprehensive list of related subjects as background research.",
    )


expand_chain = gen_related_topics_prompt | get_fast_llm().with_structured_output(
    RelatedSubjects
)


# Generate Perspectives
class Editor(BaseModel):
    affiliation: str = Field(
        description="Primary affiliation of the editor.",
    )
    name: str = Field(
        description="Name of the editor.", pattern=r"^[a-zA-Z0-9_-]{1,64}$"
    )
    role: str = Field(
        description="Role of the editor in the context of the topic.",
    )
    description: str = Field(
        description="Description of the editor's focus, concerns, and motives.",
    )

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"


class Perspectives(BaseModel):
    editors: list[Editor] = Field(
        description="Comprehensive list of editors with their roles and affiliations.",
        # Add a pydantic validation/restriction to be at most M editors
    )


gen_perspectives_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You need to select a diverse (and distinct) group of Wikipedia editors who will work together to create a comprehensive article on the topic. Each of them represents a different perspective, role, or affiliation related to this topic.\
    You can use other Wikipedia pages of related topics for inspiration. For each editor, add a description of what they will focus on.

    Wiki page outlines of related topics for inspiration:
    {examples}""",
        ),
        ("user", "Topic of interest: {topic}"),
    ]
)

# gen_perspectives_chain = gen_perspectives_prompt | ChatOpenAI(
#     model="gpt-3.5-turbo"
# ).with_structured_output(Perspectives)


# wikipedia_retriever = WikipediaRetriever(load_all_available_meta=True, top_k_results=1)


def format_doc(doc, max_length=1000):
    related = "- ".join(doc.metadata["categories"])
    return f"### {doc.metadata['title']}\n\nSummary: {doc.page_content}\n\nRelated\n{related}"[
        :max_length
    ]


def format_docs(docs):
    return "\n\n".join(format_doc(doc) for doc in docs)


# @as_runnable
# async def survey_subjects(topic: str):
#     related_subjects = await expand_chain.ainvoke({"topic": topic})
#     retrieved_docs = await wikipedia_retriever.abatch(
#         related_subjects.topics, return_exceptions=True
#     )
#     all_docs = []
#     for docs in retrieved_docs:
#         if isinstance(docs, BaseException):
#             continue
#         all_docs.extend(docs)
#     formatted = format_docs(all_docs)
#     # return await gen_perspectives_chain.ainvoke({"examples": formatted, "topic": topic})
#     return {}


# Expert Dialog


def add_messages(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def update_references(references, new_references):
    if not references:
        references = {}
    references.update(new_references)
    return references


def update_editor(editor, new_editor):
    # Can only set at the outset
    if not editor:
        return new_editor
    return editor


class InterviewState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    references: Annotated[dict | None, update_references]
    editor: Annotated[Editor | None, update_editor]


# Dialog Roles


gen_qn_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an experienced Wikipedia writer and want to edit a specific page. \
Besides your identity as a Wikipedia writer, you have a specific focus when researching the topic. \
Now, you are chatting with an expert to get information. Ask good questions to get more useful information.

When you have no more questions to ask, say "Thank you so much for your help!" to end the conversation.\
Please only ask one question at a time and don't ask what you have asked before.\
Your questions should be related to the topic you want to write.
Be comprehensive and curious, gaining as much unique insight from the expert as possible.\

Stay true to your specific perspective:

{persona}""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)


def tag_with_name(ai_message: AIMessage, name: str):
    ai_message.name = name
    return ai_message


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}


@as_runnable
async def generate_question(state: InterviewState):
    editor = state["editor"]
    gn_chain = (
        RunnableLambda(swap_roles).bind(name=editor.name)
        | gen_qn_prompt.partial(persona=editor.persona)
        | get_fast_llm()
        | RunnableLambda(tag_with_name).bind(name=editor.name)
    )
    result = await gn_chain.ainvoke(state)
    return {"messages": [result]}


# Expert Dialog


def add_messages(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def update_references(references, new_references):
    if not references:
        references = {}
    references.update(new_references)
    return references


def update_editor(editor, new_editor):
    # Can only set at the outset
    if not editor:
        return new_editor
    return editor


class InterviewState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    references: Annotated[dict | None, update_references]
    editor: Annotated[Editor | None, update_editor]


# Dialog Roles


gen_qn_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an experienced Wikipedia writer and want to edit a specific page. \
Besides your identity as a Wikipedia writer, you have a specific focus when researching the topic. \
Now, you are chatting with an expert to get information. Ask good questions to get more useful information.

When you have no more questions to ask, say "Thank you so much for your help!" to end the conversation.\
Please only ask one question at a time and don't ask what you have asked before.\
Your questions should be related to the topic you want to write.
Be comprehensive and curious, gaining as much unique insight from the expert as possible.\

Stay true to your specific perspective:

{persona}""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)


# Answer questions


class Queries(BaseModel):
    queries: list[str] = Field(
        description="Comprehensive list of search engine queries to answer the user's questions.",
    )


gen_queries_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful research assistant. Query the search engine to answer the user's questions.",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)
# gen_queries_chain = gen_queries_prompt | get_fast_llm().with_structured_output(
#     Queries, include_raw=True
# )


class AnswerWithCitations(BaseModel):
    answer: str = Field(
        description="Comprehensive answer to the user's question with citations.",
    )
    cited_urls: list[str] = Field(
        description="List of urls cited in the answer.",
    )

    @property
    def as_str(self) -> str:
        return f"{self.answer}\n\nCitations:\n\n" + "\n".join(
            f"[{i+1}]: {url}" for i, url in enumerate(self.cited_urls)
        )


gen_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert who can use information effectively. You are chatting with a Wikipedia writer who wants\
 to write a Wikipedia page on the topic you know. You have gathered the related information and will now use the information to form a response.

Make your response as informative as possible and make sure every sentence is supported by the gathered information.
Each response must be backed up by a citation from a reliable source, formatted as a footnote, reproducing the URLS after your response.""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)

gen_answer_chain = gen_answer_prompt | get_fast_llm().with_structured_output(
    AnswerWithCitations, include_raw=True
).with_config(run_name="GenerateAnswer")


'''
# Tavily is typically a better search engine, but your free queries are limited
search_engine = TavilySearchResults(max_results=4)

@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]
'''

# DDG
# search_engine = DuckDuckGoSearchAPIWrapper()


# @tool
# async def search_engine(query: str):
#     """Search engine to the internet."""
#     results = DuckDuckGoSearchAPIWrapper()._ddgs_text(query)
#     return [{"content": r["body"], "url": r["href"]} for r in results]


async def gen_answer(
    state: InterviewState,
    config: RunnableConfig | None = None,
    name: str = "Subject_Matter_Expert",
    max_str_len: int = 15000,
):
    swapped_state = swap_roles(state, name)  # Convert all other AI messages
    # queries = await gen_queries_chain.ainvoke(swapped_state)
    # query_results = await search_engine.abatch(
    #     queries["parsed"].queries, config, return_exceptions=True
    # )
    # successful_results = [
    #     res for res in query_results if not isinstance(res, Exception)
    # ]
    # all_query_results = {
    #     res["url"]: res["content"] for results in successful_results for res in results
    # }
    # We could be more precise about handling max token length if we wanted to here
    # dumped = json.dumps(all_query_results)[:max_str_len]
    # ai_message: AIMessage = queries["raw"]
    # tool_call = queries["raw"].additional_kwargs["tool_calls"][0]
    # tool_id = tool_call["id"]
    # tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)
    # swapped_state["messages"].extend([ai_message, tool_message])
    # Only update the shared state with the final answer to avoid
    # polluting the dialogue history with intermediate messages
    generated = await gen_answer_chain.ainvoke(swapped_state)
    cited_urls = set(generated["parsed"].cited_urls)
    # Save the retrieved information to a the shared state for future reference
    # cited_references = {k: v for k, v in all_query_results.items() if k in cited_urls}
    formatted_message = AIMessage(name=name, content=generated["parsed"].as_str)
    return {
        "messages": [formatted_message],
        # "references": cited_references
    }


# Construct the Interview Graph
max_num_turns = 5


def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return END
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return END
    return "ask_question"


# builder = StateGraph(InterviewState)

# builder.add_node("ask_question", generate_question)
# builder.add_node("answer_question", gen_answer)
# builder.add_conditional_edges("answer_question", route_messages)
# builder.add_edge("ask_question", "answer_question")

# builder.add_edge(START, "ask_question")
# interview_graph = builder.compile().with_config(run_name="Conduct Interviews")


# Generate Sections


class SubSection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    content: str = Field(
        ...,
        title="Full content of the subsection. Include [#] citations to the cited sources where relevant.",
    )

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.content}".strip()


class WikiSection(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    content: str = Field(..., title="Full content of the section")
    subsections: list[Subsection] | None = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Wikipedia page.",
    )
    citations: list[str] = Field(default_factory=list)

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            subsection.as_str for subsection in self.subsections or []
        )
        citations = "\n".join([f" [{i}] {cit}" for i, cit in enumerate(self.citations)])
        return (
            f"## {self.section_title}\n\n{self.content}\n\n{subsections}".strip()
            + f"\n\n{citations}".strip()
        )


# section_writer_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are an expert Wikipedia writer. Complete your assigned WikiSection from the following outline:\n\n"
#             "{outline}\n\nCite your sources, using the following references:\n\n<Documents>\n{docs}\n<Documents>",
#         ),
#         ("user", "Write the full WikiSection for the {section} section."),
#     ]
# )


async def retrieve(inputs: dict):
    # docs = await retriever.ainvoke(inputs["topic"] + ": " + inputs["section"])
    formatted = "\n".join(
        # [
        #     f'<Document href="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
        #     for doc in docs
        # ]
    )
    return {"docs": formatted, **inputs}


# section_writer = (
#     retrieve
#     | section_writer_prompt
#     | get_long_context_llm().with_structured_output(WikiSection)
# )


# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# reference_docs = [
#     Document(page_content=v, metadata={"source": k})
#     for k, v in final_state["references"].items()
# ]
# # This really doesn't need to be a vectorstore for this size of data.
# # It could just be a numpy matrix. Or you could store documents
# # across requests if you want.
# vectorstore = SKLearnVectorStore.from_documents(
#     reference_docs,
#     embedding=embeddings,
# )
# retriever = vectorstore.as_retriever(k=10)
# Generate final article
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Wikipedia author. Write the complete wiki article on {topic} using the following section drafts:\n\n"
            "{draft}\n\nStrictly follow Wikipedia format guidelines.",
        ),
        (
            "user",
            'Write the complete Wiki article using markdown format. Organize citations using footnotes like "[1]",'
            " avoiding duplicates in the footer. Include URLs in the footer.",
        ),
    ]
)

writer = writer_prompt | get_llm_long_context_default() | StrOutputParser()


# Final Flow


class ResearchState(TypedDict):
    topic: str
    outline: Outline
    editors: list[Editor]
    interview_results: list[InterviewState]
    # The final sections output
    sections: list[WikiSection]
    article: str


async def initialize_research(state: ResearchState):
    topic = state["topic"]
    # coros = (
    #     generate_outline_direct.ainvoke({"topic": topic}),
    #     survey_subjects.ainvoke(topic),
    # )
    # results = await asyncio.gather(*coros)
    return {
        **state,
        # "outline": results[0],
        # "editors": results[1].editors,
    }


async def conduct_interviews(state: ResearchState):
    topic = state["topic"]
    initial_states = [
        {
            "editor": editor,
            "messages": [
                AIMessage(
                    content=f"So you said you were writing an article on {topic}?",
                    name="Subject_Matter_Expert",
                )
            ],
        }
        for editor in state["editors"]
    ]
    # We call in to the sub-graph here to parallelize the interviews
    # interview_results = await interview_graph.abatch(initial_states)

    return {
        **state,
        # "interview_results": interview_results,
    }


def format_conversation(interview_state):
    messages = interview_state["messages"]
    convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
    return f'Conversation with {interview_state["editor"].name}\n\n' + convo


refine_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Wikipedia writer. You have gathered information from experts and search engines. Now, you are refining the outline of the Wikipedia page. \
You need to make sure that the outline is comprehensive and specific. \
Topic you are writing about: {topic}

Old outline:

{old_outline}""",
        ),
        (
            "user",
            "Refine the outline based on your conversations with subject-matter experts:\n\nConversations:\n\n{conversations}\n\nWrite the refined Wikipedia outline:",
        ),
    ]
)

# Using turbo preview since the context can get quite long
refine_outline_chain = (
    refine_outline_prompt
    | get_llm_long_context_default().with_structured_output(Outline)
)


async def refine_outline(state: ResearchState):
    convos = "\n\n".join(
        [
            format_conversation(interview_state)
            for interview_state in state["interview_results"]
        ]
    )

    updated_outline = await refine_outline_chain.ainvoke(
        {
            "topic": state["topic"],
            "old_outline": state["outline"].as_str,
            "conversations": convos,
        }
    )
    return {**state, "outline": updated_outline}


async def index_references(state: ResearchState):
    all_docs = []
    for interview_state in state["interview_results"]:
        reference_docs = [
            Document(page_content=v, metadata={"source": k})
            for k, v in interview_state["references"].items()
        ]
        all_docs.extend(reference_docs)
    # await vectorstore.aadd_documents(all_docs)
    return state


# refined_outline = refine_outline_chain.invoke(
#     {
#         # "topic": example_topic,
#         # "old_outline": initial_outline.as_str,
#         # "conversations": "\n\n".join(
#         #     # f"### {m.name}\n\n{m.content}" for m in final_state["messages"]
#         # ),
#         "conversations": "conversations TODO"
#     }
# )


async def write_sections(state: ResearchState):
    outline = state["outline"]
    # sections = await section_writer.abatch(
    #     [
    #         {
    #             # "outline": refined_outline.as_str,
    #             "section": section.section_title,
    #             "topic": state["topic"],
    #         }
    #         for section in outline.sections
    #     ]
    # )
    return {
        **state,
        # "sections": sections,
    }


async def write_article(state: ResearchState):
    topic = state["topic"]
    sections = state["sections"]
    draft = "\n\n".join([section.as_str for section in sections])
    article = await writer.ainvoke({"topic": topic, "draft": draft})
    return {
        **state,
        "article": article,
    }


@lru_cache
def get_workflow() -> CompiledStateGraph:
    builder_of_storm = StateGraph(ResearchState)

    nodes = [
        ("init_research", initialize_research),
        ("conduct_interviews", conduct_interviews),
        ("refine_outline", refine_outline),
        ("index_references", index_references),
        ("write_sections", write_sections),
        ("write_article", write_article),
    ]
    for i in range(len(nodes)):
        name, node = nodes[i]
        builder_of_storm.add_node(name, node)
        if i > 0:
            builder_of_storm.add_edge(nodes[i - 1][0], name)

    builder_of_storm.add_edge(START, nodes[0][0])
    builder_of_storm.add_edge(nodes[-1][0], END)
    storm = builder_of_storm.compile(checkpointer=MemorySaver())
    return storm


@router.post("/chat", tags=["joke"], response_model=ResearchState | None)
async def chat(messages: list[MtmChatMessage]):
    logger.info("JokeAgent handle Message %s", messages)

    latest_message = messages[-1]
    wf = get_workflow()

    state = ResearchState(
        messages=[{"role": "user", "content": latest_message.content}]
    )

    thread_id = mtutils.gen_orm_id_key()

    response = response = StreamingResponse(
        wf_to_chatstreams(wf=wf, state=state, thread_id=thread_id)
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
