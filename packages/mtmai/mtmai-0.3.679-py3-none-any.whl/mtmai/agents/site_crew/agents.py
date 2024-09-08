import logging
from textwrap import dedent

from crewai import Agent

from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


def step_callback(a):
    logger.info("调用 step_callback %s", a)


# class SiteAgents:
#     def __init__(self):
#         pass


def joke_writer_agent():
    llm = get_llm_chatbot_default()

    return Agent(
        role="幽默段子写手",
        goal="创作幽默段子",
        backstory=dedent("""\
            作为一个网站的博主,你非常删除编写适合短视频社交平台的幽默段子， 作品容易吸引年轻人浏览，点击关注"""),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        step_callback=step_callback,
    )
