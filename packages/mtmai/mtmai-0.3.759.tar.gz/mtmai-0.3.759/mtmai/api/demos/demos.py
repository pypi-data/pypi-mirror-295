import asyncio
import json
import logging
import os
import pprint
import random
import threading
from datetime import datetime, timedelta
from typing import AsyncGenerator, Callable

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.agents import (
    AgentExecutor,
    Tool,
    create_openai_tools_agent,
    create_tool_calling_agent,
)

# from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from requests import RequestException

# from tavily import TavilyClient
from mtmai.core.config import settings

# from mtmai.mtlibs.aiutils import chat_completions, lcllm_openai_chat

router = APIRouter()
logger = logging.getLogger()


counter = 0
stop_event = asyncio.Event()
counter_lock = threading.Lock()


async def increment_counter(limit: int):
    global counter
    print("increment_counter call")
    while counter <= limit:
        if stop_event.is_set():
            print("Counter stopped by user.")
            break
        await asyncio.sleep(1)
        with counter_lock:
            counter += 1
        print(f"Counter incremented to {counter}")


def start_increment_counter(limit):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(increment_counter(limit))


@router.get("/counter_start")
async def counter_start():
    global stop_event
    print("counter_start")
    stop_event.clear()  # Reset the stop event
    thread = threading.Thread(target=start_increment_counter, args=(100,))
    thread.start()
    return {"message": "Counter started in the background"}


@router.get("/counter_stop")
async def counter_stop():
    global stop_event
    stop_event.set()  # Signal the background task to stop
    return {"message": "Counter will stop soon"}


@router.get("/get_counter")
async def get_count():
    print("get_counter")
    global counter
    with counter_lock:
        current_counter = counter
    return {"counter": current_counter}


@router.get("/hello_stream")
async def hello_stream():
    def hello_stream_iter():
        data = {"aaa": "bbb"}
        yield f"0:{json.dumps(data)}"

    return StreamingResponse(
        hello_stream_iter(),
        media_type="text/event-stream",
    )


class DemoTaskRunner:
    def __init__(self, streamer: Callable[[str], None]):
        self.streamer = streamer

    async def run(self):
        for i in range(1, 15):
            await asyncio.sleep(0.5)
            if self.streamer:
                self.streamer(f"0:{json.dumps({'task_id': i})}\n")


@router.get(settings.API_V1_STR + "/test_stream1")
async def multi_tasks_stream_demo():
    """较底层的方式运行多任务，并且以http stream 的方式返回消息给客户端"""

    async def stream_generator(
        streamer: Callable[[], AsyncGenerator[str, None]],
    ) -> AsyncGenerator[str, None]:
        async for message in streamer():
            yield message
        # 所有任务完成
        yield f'0:{json.dumps({"finish_reason": "stop"})}\n'

    queue = asyncio.Queue()

    async def streamer() -> AsyncGenerator[str, None]:
        while True:
            message = await queue.get()
            if message is None:  # Stop signal
                break
            yield message

    async def producer():
        # Create and start tasks
        demo_task1 = DemoTaskRunner(lambda msg: queue.put_nowait(msg))
        demo_task2 = DemoTaskRunner(lambda msg: queue.put_nowait(msg))

        # Run tasks concurrently
        await asyncio.gather(demo_task1.run(), demo_task2.run())

    asyncio.create_task(producer())  # noqa: RUF006

    return StreamingResponse(stream_generator(streamer), media_type="text/event-stream")


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


dbFile = ".vol/demo_users.db"


async def test_groq_llama3_tool_use(user_input: str):
    """测试使用 groq llama3-groq-70b-8192-tool-use-preview 模型对于 Text2Sql 场景的情况"""
    import sqlite3

    initMysqlLiteDb()
    client = get_default_openai_client()

    # 数据库连接函数
    def get_db_connection():
        """创建并返回到SQLite数据库的连接"""
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_sql(sql_query):
        """执行SQL查询并返回结果"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql_query)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            return f"数据库错误: {e}"
        finally:
            conn.close()

    def generate_sql(table_info, conditions, select_fields="*"):
        """
        生成SQL查询
        :param table_info: 表信息
        :param conditions: WHERE子句的条件
        :param select_fields: 要选择的字段，默认为所有字段
        :return: 生成的SQL查询字符串
        """
        return f"SELECT {select_fields} FROM users WHERE {conditions}"

    def format_results(results, fields=None):
        """
        格式化查询结果
        :param results: 查询返回的结果列表
        :param fields: 要显示的字段列表，如果为None则显示所有字段
        :return: 格式化后的结果字符串
        """
        if isinstance(results, str):  # 如果结果是错误消息
            return results

        if not results:
            return "没有找到匹配的记录。"

        if fields:
            formatted = [
                ", ".join(str(row.get(field, "N/A")) for field in fields)
                for row in results
            ]
        else:
            formatted = [
                json.dumps(row, ensure_ascii=False, indent=2) for row in results
            ]

        return "\n".join(formatted)

    def run_text2sql_conversation(user_prompt):
        """
        运行text2sql对话
        :param user_prompt: 用户输入的查询
        :return: 查询结果
        """
        table_info = "users(id INTEGER, name TEXT, age INTEGER, email TEXT, registration_date DATE, last_login DATETIME)"

        messages = [
            {
                "role": "system",
                "content": f"你是一个SQL助手。使用generate_sql函数根据用户请求创建SQL查询。可用的表: {table_info}。准确理解用户需求，包括他们想要查询的具体字段。",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_sql",
                    "description": "根据用户请求生成SQL查询",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "table_info": {
                                "type": "string",
                                "description": "表结构信息",
                            },
                            "conditions": {
                                "type": "string",
                                "description": "WHERE子句的具体查询条件",
                            },
                            "select_fields": {
                                "type": "string",
                                "description": "要选择的字段，用逗号分隔",
                            },
                        },
                        "required": ["table_info", "conditions", "select_fields"],
                    },
                },
            }
        ]

        try:
            response = client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=4096,
            )

            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    if tool_call.function.name == "generate_sql":
                        function_args = json.loads(tool_call.function.arguments)
                        sql_query = generate_sql(
                            function_args["table_info"],
                            function_args["conditions"],
                            function_args["select_fields"],
                        )
                        results = execute_sql(sql_query)
                        formatted_results = format_results(
                            results,
                            function_args["select_fields"].split(", ")
                            if function_args["select_fields"] != "*"
                            else None,
                        )
                        return (
                            f"生成的SQL查询: {sql_query}\n\n结果:\n{formatted_results}"
                        )

            return "无法生成SQL查询。请尝试重新表述您的问题。"

        except Exception as e:
            return f"发生错误: {e!s}"

    return run_text2sql_conversation(user_input)


def initMysqlLiteDb():
    import sqlite3

    # 连接到SQLite数据库（如果不存在则创建）
    if os.path.exists(dbFile):
        print("删除旧数据库", dbFile)
        os.remove(dbFile)

    if not os.path.exists(".vol"):
        os.mkdir(".vol")
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE,
        registration_date DATE,
        last_login DATETIME
    )
    """)

    # 生成示例数据
    names = [
        "Alice",
        "Bob",
        "Charlie",
        "David",
        "Eva",
        "Frank",
        "Grace",
        "Henry",
        "Ivy",
        "Jack",
        "Liang",
        "Boci",
        "Zhang",
    ]
    domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "example.com",
        "example2.com",
        "example3.com",
    ]

    for i in range(20):  # 创建50个用户记录
        name = random.choice(names)
        age = random.randint(18, 70)
        email = f"{name.lower()}{random.randint(1, 100)}@{random.choice(domains)}"
        registration_date = datetime.now() - timedelta(days=random.randint(1, 1000))
        last_login = registration_date + timedelta(days=random.randint(1, 500))

        cursor.execute(
            """
        INSERT INTO users (name, age, email, registration_date, last_login)
        VALUES (?, ?, ?, ?, ?)
        """,
            (name, age, email, registration_date.date(), last_login),
        )

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

    print("Demo database 'demo_users.db' created successfully with sample data.")

    # 函数用于显示表格内容
    def display_table_contents():
        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users LIMIT 5")
        rows = cursor.fetchall()

        print("\nSample data from the users table:")
        for row in rows:
            print(row)

        conn.close()

    display_table_contents()


@router.get("/demos/tooluse_text2sql")
async def demoTooluseText2sql():
    user_input = "查询Frank的年龄"
    return {
        "question": "查询Frank的年龄",
        "result": await test_groq_llama3_tool_use(user_input),
    }


# 定义使用的模型名称
MODEL = "llama3-groq-70b-8192-tool-use-preview"


async def calculate(expression):
    """计算数学表达式"""
    try:
        # 使用eval函数评估表达式
        result = eval(expression)
        # 返回JSON格式的结果
        return json.dumps({"result": result})
    except Exception:
        # 如果计算出错，返回错误信息
        return json.dumps({"error": "Invalid expression"})


async def run_conversation(user_prompt):
    """
    tool use 本质是多轮对话，当上一轮 ai 返回了 tool_calls 答复，本地根据tool_calls 调用对应的函数，然后将结果附加到消息末尾，再次提交给ai，然后ai完成下一轮的答复。
    """
    aiClient = get_default_openai_client()
    # 定义对话的消息列表
    messages = [
        {
            "role": "system",
            "content": "你是一个计算器助手。使用计算函数执行数学运算并提供结果.",
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    # 定义可用的工具（函数）
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "计算数学表达式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "要评估的数学表达式",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    print("第一次信息输出: {messages}\n")
    # 作用和目的：
    # 初始化对话：将用户的问题发送给 AI 模型。
    # 提供工具信息：告诉模型可以使用哪些工具（在这里是 calculate 函数）。
    # 获取模型的初步响应：模型可能会直接回答，或者决定使用提供的工具。

    # 特点：
    # 包含了初始的对话历史（系统提示和用户问题）。
    # 提供了 tools 参数，定义了可用的函数。
    # 使用 tool_choice="auto"，允许模型自主决定是否使用工具。
    response = aiClient.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto", max_tokens=4096
    )
    print("输出response {response}\n")
    # 获取响应消息和工具调用
    response_message = response.choices[0].message
    print(f"第一次响应输出: {response_message} \n")
    tool_calls = response_message.tool_calls
    print("输出tool_calls信息: \n")
    pprint.pprint(tool_calls)
    print("\n")

    # 如果有工具调用
    if tool_calls:
        # 定义可用的函数字典
        available_functions = {
            "calculate": calculate,
        }
        # 将响应消息添加到对话历史
        messages.append(response_message)

        # 处理每个工具调用
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # 解析函数参数
            function_args = json.loads(tool_call.function.arguments)
            # 调用函数并获取响应
            function_response = await function_to_call(
                expression=function_args.get("expression")
            )
            print("\n输出function_response " + function_response + "\n")
            # 将函数调用结果添加到对话历史
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        print("第二次信息输出 : {messages} \n")
        second_response = aiClient.chat.completions.create(
            model=MODEL, messages=messages
        )
        # 返回最终响应内容
        return second_response.choices[0].message.content
