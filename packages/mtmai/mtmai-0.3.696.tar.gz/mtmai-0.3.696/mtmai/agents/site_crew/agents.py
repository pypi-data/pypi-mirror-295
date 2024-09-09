import logging
from textwrap import dedent

from crewai import Agent

from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


def step_callback(a):
    logger.info("调用 step_callback %s", a)


def joke_writer_agent():
    llm = get_llm_chatbot_default()

    return Agent(
        role="你是网站的站长，负责网站的运营和内容创作",
        goal="生成网站内容",
        backstory=dedent("""\
            作为一个网站的站长，你非常擅长运营网站，并且能够根据网站的定位和目标用户创作合适的内容"""),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        step_callback=step_callback,
    )
