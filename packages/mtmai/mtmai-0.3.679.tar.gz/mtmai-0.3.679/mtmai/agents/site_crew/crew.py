"""
博客网站生成团队
"""

from crewai import Crew

from mtmai.agents.site_crew.agents import joke_writer_agent
from mtmai.agents.site_crew.tasks import post_generate_task
from mtmai.llm.llm import get_llm_chatbot_default


async def post_generate(params: dict):
    """
    博客网站生成任务
    """
    llm = get_llm_chatbot_default()

    agent1 = joke_writer_agent()
    crew = Crew(
        agents=[
            agent1,
            # self.action_agent,
            # self.writer_agent,
        ],
        tasks=[
            post_generate_task(agent1),
            # tasks.action_required_emails_task(self.action_agent),
            # tasks.draft_responses_task(self.writer_agent),
        ],
        verbose=True,
        manager_llm=llm,
        function_calling_llm=llm,
        planning_llm=llm,
    )
    result = await crew.kickoff_async()
    return result
