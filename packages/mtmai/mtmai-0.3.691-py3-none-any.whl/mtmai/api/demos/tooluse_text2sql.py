import json
import os
import random
import sqlite3
from datetime import datetime, timedelta

from fastapi import APIRouter
from langsmith import traceable

from mtmai.mtlibs.aiutils import get_default_openai_client

router = APIRouter()
dbFile = ".vol/demo_users.db"


@traceable
async def test_groq_llama3_tool_use(user_input: str):
    """测试使用 groq llama3-groq-70b-8192-tool-use-preview 模型对于 Text2Sql 场景的情况"""
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
