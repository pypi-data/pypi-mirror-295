import json
import os
import pprint

from fastapi import APIRouter
from langsmith import traceable
from tavily import TavilyClient

from mtmai.mtlibs.aiutils import get_default_openai_client

router = APIRouter()

# 定义使用的模型名称
MODEL = "llama3-groq-70b-8192-tool-use-preview"


def tavily_search(query):
    """执行Tavily搜索."""
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
    except Exception as e:  # noqa: BLE001
        return json.dumps({"error": str(e)})


def run_conversation(user_prompt):
    client = get_default_openai_client()

    messages = [
        {
            "role": "system",
            "content": "你是一个智能助手，能够进行在线搜索以回答问题。使用tavily_search函数来获取最新、最相关的信息。请基于搜索结果提供详细、准确的回答，并在适当的时候引用信息来源。",
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
                "name": "tavily_search",
                "description": "执行在线搜索查询, 获取最新信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ]

    print("初始消息:\n")
    pprint.pprint(messages)
    print("\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096,
    )

    print("Groq API 响应:\n")
    pprint.pprint(response)
    print("\n")

    response_message = response.choices[0].message
    print("AI 初始响应:\n")
    pprint.pprint(response_message)
    print("\n")

    tool_calls = response_message.tool_calls
    if tool_calls:
        print("工具调用信息:\n")
        pprint.pprint(tool_calls)
        print("\n")

        messages.append(response_message)

        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            function_response = tavily_search(**function_args)
            print(f"\nTavily 搜索响应:\n{function_response}\n")
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "tavily_search",
                    "content": function_response,
                }
            )

        print("更新后的消息:\n")
        pprint.pprint(messages)
        print("\n")

        second_response = client.chat.completions.create(model=MODEL, messages=messages)
        return second_response.choices[0].message.content
    else:
        return response_message.content


@router.get("/demos/tavily_demo")
@traceable
async def demoTavily():
    # 用户提示示例
    user_prompt = "今天有哪些新闻?"
    return {
        "result": run_conversation(user_prompt),
    }
