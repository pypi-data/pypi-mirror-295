import json
import pprint

from fastapi import APIRouter
from langsmith import traceable

from mtmai.mtlibs.aiutils import get_default_openai_client

router = APIRouter()

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


@traceable
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


@router.get("/demos/hello_tool_use")
async def blogPage():
    user_prompt = "计算25.6602988 * 4/0.259484 + 5.69560456 -398.11287180等于多少?这个数字有什么特殊意义吗?用中文回答."
    return {
        "result": await run_conversation(user_prompt),
    }
