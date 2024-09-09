"""
博客网站生成团队
"""

from textwrap import dedent

from crewai import Crew
from pydantic import BaseModel

from mtmai.agents.site_crew.agents import joke_writer_agent
from mtmai.llm.llm import get_llm_chatbot_default
from mtmai.models.site import SiteBase


class SitePostGenerateInput(BaseModel):
    title: str
    site_data: SiteBase


async def crew_post_generate(input: SitePostGenerateInput):
    """
    博客网站生成任务
    """
    from crewai import Task

    llm = get_llm_chatbot_default()

    agent1 = joke_writer_agent()

    task1 = Task(
        description=dedent("""\
            以关键字: {keywords}和描述: {description}，生成一篇博客文章
            """),
        agent=agent1,
        expected_output="约1000字长度的专业博客文章,必须是中文",
    )

    input2 = {
        "keywords": input.title,
        "description": input.site_data.description,
    }
    crew = Crew(
        input=input2,
        agents=[
            agent1,
            # self.action_agent,
            # self.writer_agent,
        ],
        tasks=[
            task1,
        ],
        verbose=True,
        manager_llm=llm,
        function_calling_llm=llm,
        planning_llm=llm,
    )
    result = await crew.kickoff_async()
    return result
