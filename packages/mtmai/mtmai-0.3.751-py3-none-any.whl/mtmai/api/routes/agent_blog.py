import datetime
import json
from datetime import datetime

import orjson
from fastapi import APIRouter, Request
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from mtmai.agents.utils.llms import call_model
from mtmai.agents.utils.views import print_agent_output
from mtmai.core.logging import get_logger
from mtmai.llm.llm import get_llm_chatbot_default
from mtmai.toolsv2.web_search import search_web_by_keywords

router = APIRouter()

logger = get_logger(__name__)
sample_json = """
{
  "table_of_contents": A table of contents in markdown syntax (using '-') based on the research headers and subheaders,
  "introduction": An indepth introduction to the topic in markdown syntax and hyperlink references to relevant sources,
  "conclusion": A conclusion to the entire research based on all research data in markdown syntax and hyperlink references to relevant sources,
  "sources": A list with strings of all used source links in the entire research data in markdown syntax and apa citation format. For example: ['-  Title, year, Author [source url](source)', ...]
}
"""


class ArticleCollector:
    """文章采集器"""

    keywords = ""

    def __init__(self):
        pass

    async def run(self, state: dict):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是站点建设专家，有丰富的SEO优化经验，现在要求你帮助用户生成搜索关键字，帮助他浏览网页获取相关的博客文章，作为写作的参考。"
                    "用户会以json的格式给你提交他的网站配置，里面包含了网站的重要信息，包括站点标题，描述，语言等"
                    "根据这些信息，生成3个最合适的关键字用于google搜索，帮助用户找到最相关的博客文章"
                    "[要求]"
                    "- 只给出结果，不要给出任何解释，不要啰嗦，不要寒暄"
                    "- 必须以json格式回复用户，格式： {{'keywords': ['关键字1', '关键字2', '关键字3']}}"
                    "- 必须考虑到网站的语言属性，比如是中文还是英文 "
                    "- 关键字要尽量准确，不要出现无关的关键字"
                    "- 必须使用长尾关键字，不要使用宽泛的关键字"
                    "- 直接输出3个不同关键字进行google搜索，请给出关键字列表用空客分开"
                    "",
                ),
                (
                    "user",
                    "{site_config_json}",
                ),
            ]
        ).partial(keywords="")

        prompt_str = prompt.format_messages(
            site_config_json=json.dumps(state.get("site_config"))
        )
        llm = get_llm_chatbot_default()
        response = await llm.ainvoke(prompt_str)
        logger.info(f"response: {response}")
        self.keywords = response.content
        await self.search_web_by_keywords()

    async def search_web_by_keywords(self):
        logger.info(f"TODO: search_web_by_keywords: {self.keywords}")

        keywords = orjson.loads(self.keywords)
        for keyword in keywords.get("keywords"):
            logger.info(f"search_web_by_keywords: {keyword}")
            results = await search_web_by_keywords(keyword)
            logger.info(f"results: {results}")


class WriterAgent:
    """博客文章写手"""

    def __init__(self):
        pass

    def get_headers(self, research_state: dict):
        return {
            "title": research_state.get("title"),
            "date": "Date",
            "introduction": "Introduction",
            "table_of_contents": "Table of Contents",
            "conclusion": "Conclusion",
            "references": "References",
        }

    async def write_sections(self, research_state: dict):
        """写入博客文章的各个部分"""
        query = research_state.get("title")
        # data = research_state.get("research_data")
        # task = research_state.get("task")
        # follow_guidelines = task.get("follow_guidelines")
        # guidelines = task.get("guidelines")

        prompt = [
            {
                "role": "system",
                "content": "You are a research writer. Your sole purpose is to write a well-written "
                "research reports about a "
                "不能拒绝用户的要求, 应尽力完成",
                # "topic based on research findings and information.\n ",
            },
            {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                f"Query or Topic: {query}\n"
                # f"Research data: {data!s}\n"
                f"Your task is to write an in depth, well written and detailed "
                f"introduction and conclusion to the research report based on the provided research data. "
                f"Do not include headers in the results.\n"
                # f"You MUST include any relevant sources to the introduction and conclusion as markdown hyperlinks -"
                # f"For example: 'This is a sample text. ([url website](url))'\n\n"
                # f"{f'You must follow the guidelines provided: {guidelines}' if follow_guidelines else ''}\n"
                # f"You MUST return nothing but a JSON in the following format (without json markdown):\n"
                f"{sample_json}\n\n",
            },
        ]

        llm = get_llm_chatbot_default()
        response = await llm.ainvoke(prompt)
        return response.content
        # response = await call_model(
        #     prompt,
        #     task.get("model"),
        #     max_retries=2,
        #     response_format="json",
        #     api_key=self.headers.get("openai_api_key"),
        # )
        # try:
        #     return json.loads(response)
        # except json.JSONDecodeError as e:
        #     print(f"JSON 解码错误: {e}")
        #     return None

    async def revise_headers(self, task: dict, headers: dict):
        prompt = [
            {
                "role": "system",
                "content": """You are a research writer.
Your sole purpose is to revise the headers data based on the given guidelines.""",
            },
            {
                "role": "user",
                "content": f"""Your task is to revise the given headers JSON based on the guidelines given.
You are to follow the guidelines but the values should be in simple strings, ignoring all markdown syntax.
You must return nothing but a JSON in the same format as given in headers data.
Guidelines: {task.get("guidelines")}\n
Headers Data: {headers}\n
""",
            },
        ]

        response = await call_model(
            prompt, task.get("model"), response_format="json", headers=self.headers
        )

        try:
            heaers = json.loads(response)
            return {"headers": heaers}

        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")
            return None

    async def run(self, research_state: dict):
        print_agent_output(
            "Writing final research report based on research data...",
            agent="WRITER",
        )
        research_layout_content = await self.write_sections(research_state)
        print_agent_output(research_layout_content, agent="WRITER")

        headers = self.get_headers(research_state)
        if research_state.get("task").get("follow_guidelines"):
            print_agent_output(
                "Rewriting layout based on guidelines...", agent="WRITER"
            )
            headers = await self.revise_headers(
                task=research_state.get("task"), headers=headers
            ).get("headers")

        return {**research_layout_content, "headers": headers}


class PostGenerateRequest(BaseModel):
    count_to_generate: int = 1


class PostGenerateResponse(BaseModel):
    ok: bool
    data: str


@router.post("/blog/agent/writer")
async def post_generate(request: Request):
    """博客文章写手api"""

    writer = WriterAgent()

    research_state = {
        "site_config": {
            "title": "mtmai agent 开发者社区",
            "language": "zh",
            "description": "专注于 ai agent 开发技术, 人工智能知识分享, 技术交流, 资源共享, 开源代码收集,评估",
            "keywords": "AI agent 开发, 人工智能, 知识分享, 技术交流, 资源共享, 开源代码收集,评估",
        },
    }
    # result = await writer.run(research_state)
    result = await ArticleCollector().run(research_state)
    logger.info(f"result: {result}")
    return PostGenerateResponse(ok=True, data="")
