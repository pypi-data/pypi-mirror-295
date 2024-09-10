"""
doc: https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol
"""

import json

from fastapi.encoders import jsonable_encoder


def text(word: str):
    return f"0:{json.dumps(word)}\n"


def data(items):
    if isinstance(items, list):
        return f"2:{json.dumps(jsonable_encoder(items))}\n"
    else:
        return f"2:{json.dumps([jsonable_encoder(items)])}\n"


def error(error_message: str):
    return f"3:{json.dumps(error_message)}\n"


def finish(reason: str = "stop", prompt_tokens: int = 0, completion_tokens: int = 0):
    data = {
        "finishReason": reason,
        "usage": {"promptTokens": prompt_tokens, "completionTokens": completion_tokens},
    }
    return f"d:{json.dumps(data)}\n"
