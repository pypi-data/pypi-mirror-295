import json
import logging
import os

import fastapi
from langchain.agents import (
    AgentExecutor,
    Tool,
    create_openai_tools_agent,
    create_tool_calling_agent,
)
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from requests import RequestException

# from tavily import TavilyClient
from mtmai.core.config import settings
from mtmai.mtlibs.aiutils import chat_completions, lcllm_openai_chat

router = fastapi.APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)


@router.get(f"{settings.API_V1_STR}/agent/hello")
async def agent_hello():
    """不使用 langchain 的agent."""
    prompt = "hello"
    model_name = "groq/llama3-8b-8192"
    messages = [{"role": "user", "content": prompt}]
    result = chat_completions(messages, model_name)
    return result.choices[0].message.content


@router.get("/agent/hello2")
async def agent_hello_2():
    """Langchain Agent 综合使用 数学运算|维基百科|字符统计."""
    llm = lcllm_openai_chat("groq/llama3-groq-70b-8192-tool-use-preview")
    problem_chain = LLMMathChain.from_llm(llm=llm)

    # langchain 内置的专门解决数学表达式运算的 tool
    math_tool = Tool.from_function(
        name="Calculator",
        func=problem_chain.run,
        verbose=True,
        description="Useful for when you need to answer numeric questions. This tool is "
        "only for math questions and nothing else. Only input math "
        "expressions, without text",
    )

    word_problem_template = """You are a reasoning agent tasked with solving the user's logic-based questions.
    Logically arrive at the solution, and be factual. In your answers, clearly detail the steps involved and give
    the final answer. Provide the response in bullet points. Question  {question} Answer"""
    math_assistant_prompt = PromptTemplate(
        input_variables=["question"], template=word_problem_template
    )
    word_problem_chain = LLMChain(llm=llm, prompt=math_assistant_prompt)
    word_problem_tool = Tool.from_function(
        name="Reasoning Tool",
        func=word_problem_chain.run,
        description="Useful for when you need to answer logic-based/reasoning  "
        "questions.",
    )

    # 维基百科
    wikipedia = WikipediaAPIWrapper()
    # Wikipedia Tool
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="A useful tool for searching the Internet to find information on world events, issues, dates, "
        "years, etc. Worth using for general topics. Use precise questions.",
    )

    tools = [math_tool, word_problem_tool, wikipedia_tool]
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI bot. Your name is {name}."),
            ("human", "Hello, how are you doing?"),
            ("ai", "I'm doing well, thanks!"),
            ("human", "{user_input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, chat_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # question1: give me the year when Tom Cruise's Top Gun released raised to the power 2
    # correct answer = 1987**2 = 3944196
    # question2: who are you? and Divide pi by 10, what is the result plus 100?
    # question2: Steve's sister is 10 years older than him. Steve was born when the cold war ended. When was Steve's sister born?
    # correct answer = 1991 - 10 = 1981

    # question3: I have 3 apples and 4 oranges. I give half of my oranges away and buy two dozen new ones, alongwith three packs of strawberries. Each pack of strawberry has 30 strawberries. How  many total pieces of fruit do I have at the end?
    # correct answer = 3 + 2 + 24 + 90 = 119

    # what is cube root of 81? Multiply with 13.27, and subtract 5.
    # correct answer = 52.4195
    result = await agent_executor.ainvoke(
        {
            "input": "hi!",
            "name": "bob",
            "user_input": "Steve's sister is 10 years older than him. Steve was born when the cold war ended. When was Steve's sister born?",
        }
    )
    return result


# memory = SqliteSaver.from_conn_string(":memory:")


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput)
def tavily_search(query) -> str:
    """Look up things online."""
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    try:
        response = tavily_client.search(query)
        # 返回前5个结果的标题、URL和内容摘要
        results = [
            {
                "title": r["title"],
                "url": r["url"],
                "content": r["content"][:200] + "...",  # 限制内容长度
            }
            for r in response["results"][:5]
        ]
        return json.dumps({"results": results})
    except RequestException as e:
        return json.dumps({"error": "Request failed: " + str(e)})
    except KeyError as e:
        return json.dumps({"error": "Key error: " + str(e)})
    except TypeError as e:
        return json.dumps({"error": "Type error: " + str(e)})
    # except Exception as e:  # 捕获所有其他未处理的异常
    #     return json.dumps({"error": "An unexpected error occurred: " + str(e)})


@router.get("/agent/search")
async def agent_search():
    """智能体, 实现互联网信息搜索."""
    # prompt = hub.pull("hwchase17/openai-tools-agent")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    llm = lcllm_openai_chat()

    # search = TavilySearchResults(max_results=2)
    tools = [tavily_search]
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    chunks = []
    # astream 使用交大粒度的流
    async for chunk in agent_executor.astream(
        {
            # "chat_history": messages,
            "input": "what's items are located where the cat is hiding?",
        },
    ):
        # Agent Action
        if "actions" in chunk:
            for action in chunk["actions"]:
                print(f"Calling Tool: `{action.tool}` with input `{action.tool_input}`")
        # Observation
        elif "steps" in chunk:
            for step in chunk["steps"]:
                print(f"Tool Result: `{step.observation}`")
        # Final result
        elif "output" in chunk:
            print(f'Final Output: {chunk["output"]}')
        else:
            raise ValueError
        print("---")
        chunks.append(chunk)
        # 输出：
        # Calling Tool: `where_cat_is_hiding` with input `{}`
        # ---
        # Tool Result: `on the shelf`
        # ---
        # Calling Tool: `get_items` with input `{'place': 'shelf'}`
        # ---
        # Tool Result: `books, penciles and pictures`
        # ---
        # Final Output: The items located where the cat is hiding on the shelf are books, pencils, and pictures.
        # ---

    # 使用小粒度的流，可以精确的每个 词语的事件
    async for event in agent_executor.astream_events(
        {"input": "where is the cat hiding? what items are in that location?"},
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":  # noqa: SIM102
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")

    return {"search_agent": "search_agent"}
