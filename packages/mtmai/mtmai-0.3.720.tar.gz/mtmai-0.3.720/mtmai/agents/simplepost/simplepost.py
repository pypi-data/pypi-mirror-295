import logging

from crewai import Agent, Crew, Process, Task
from fastapi import APIRouter

from mtmai.tools.search_tools import SearchTools

logger = logging.getLogger()

router = APIRouter()


class SimplePostCrew:
    """简单文章创作"""

    def __init__(self, input):
        # self.agents_config = json.loads(
        #     open("mtmai/teams/landing_page/config/agents.json").read()
        # )
        self.input = input
        self.__create_agents()

    async def run(self):
        # expand_idea_task = Task(
        #     description=TaskPrompts.blog_writer().format(input=self.input),
        #     agent=self.blog_post_writer,
        #     expected_output="any text content or json data",  # 需要正确设置
        # )

        # 研究任务
        research_task = Task(
            description=(
                "Identify the next big trend in the field of {topic}."
                "Focus on identifying the pros and cons, along with an overall narrative."
                "Your final report should clearly articulate the key points, market opportunities, and potential risks."
            ),
            expected_output="A comprehensive 3-paragraph report on the latest trends in artificial intelligence.",
            tools=[
                # SearchTools.search_internet,
            ],
            agent=self.researcher,
        )

        # 具有语言模型配置的写作任务
        write_task = Task(
            description=(
                "Write an insightful article about {topic}."
                "Focus on the latest trends and their impact on the industry."
                "The article should be easy to understand, engaging, and positive."
            ),
            expected_output="A 4-paragraph article on the developments in {topic}, formatted in markdown.",
            tools=[
                # SearchTools.search_internet,
            ],
            agent=self.writer,
            async_execution=False,
            output_file="new-blog-post.md",  # 输出定制的示例
        )

        crew = Crew(
            agents=[
                self.researcher,
                self.writer,
                # self.blog_post_writer,
            ],
            process=Process.sequential,
            tasks=[research_task, write_task],
            verbose=True,
            memory=False,
            cache=False,
            max_rpm=20,
            share_crew=True,
        )
        expanded_idea = await crew.kickoff_async()
        return expanded_idea

    def __create_agents(self):
        # idea_analyst_config = self.agents_config["senior_idea_analyst"]
        # strategist_config = self.agents_config["senior_strategist"]
        # developer_config = self.agents_config["senior_react_engineer"]
        # editor_config = self.agents_config["senior_content_editor"]

        # toolkit = FileManagementToolkit(
        #     root_dir="workdir", selected_tools=["read_file", "list_directory"]
        # )

        llm2 = lcllm_openai_chat()

        # llm = HuggingFaceEndpoint(
        #     repo_id="microsoft/Phi-3-mini-4k-instruct",
        #     task="text-generation",
        #     max_new_tokens=512,
        #     do_sample=False,
        #     repetition_penalty=1.03,
        # )

        self.blog_post_writer = Agent(
            # **idea_analyst_config,
            role="Professional Social Media Blog Writer",
            goal="Understand and expand upon the essence of ideas, Create professional blog articles suitable for SEO based on user input.",
            backstory="You work with data and AI",
            allow_delegation=True,
            verbose=True,
            # max_iter=5,
            llm=llm2,
            # function_calling_llm=llm,
            full_output=True,
            # tools=[
            #     # SearchTools.search_internet,
            #     # BrowserTools.scrape_and_summarize_website,
            # ],
        )

        self.researcher = Agent(
            role="Senior Researcher",
            goal="Discover breakthrough technologies in the field of {topic}",
            verbose=True,
            memory=False,
            max_iter=3,
            backstory=(
                "Driven by curiosity, you are at the forefront of innovation, eager to explore and share knowledge that may change the world."
            ),
            llm=llm2,
            # function_calling_llm=custom_model_factory,
            allow_delegation=False,
            tools=[
                SearchTools.search_internet,
                # BrowserTools.scrape_and_summarize_website,
            ],
        )

        # 创建一个作家代理人,具有自定义工具和委派能力
        self.writer = Agent(
            role="Writer",
            goal="讲述关于 {topic} 的引人入胜的科技故事",
            verbose=True,
            memory=False,
            max_iter=3,
            llm=llm2,
            # function_calling_llm=custom_model_factory,
            backstory=(
                "擅长简化复杂话题, 您撰写引人入胜的叙述, 吸引人并教育他人, 在易于理解的方式中揭示新的发现。"
            ),
            tools=[
                SearchTools.search_internet,
            ],
            allow_delegation=False,
        )


def custom_model_factory():
    # model_name = os.environ.get("CUSTOM_MODEL_NAME", "default-model")
    # return CustomModel(model_name=model_name)
    llm2 = lcllm_openai_chat()
    return llm2
