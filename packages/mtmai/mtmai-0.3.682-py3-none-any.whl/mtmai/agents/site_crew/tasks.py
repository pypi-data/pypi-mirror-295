from textwrap import dedent

from crewai import Task


def post_generate_task(agent):
    task = Task(
        description=dedent("""\
            创作一个关于小猪的幽默段子
            """),
        agent=agent,
        expected_output="约100字长度的幽默笑话文章,必须是中文的",
    )
    return task
