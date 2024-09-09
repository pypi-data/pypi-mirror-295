import logging

import httpx

from mtmai.core.config import settings

logger = logging.getLogger()


def embedding_workerai():
    stories = [
        "This is a story about an orange cloud",
        "This is a story about a llama",
        "This is a story about a hugging emoji",
    ]

    model_name = "@cf/baai/bge-base-en-v1.5"  # 维度 768
    response = httpx.post(
        f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/{model_name}",
        headers={"Authorization": f"Bearer {settings.CLOUDFLARE_AI_TOKEN}"},
        json={"text": stories},
    )
    result = response.json()
    return result


async def embedding_hf(
    *, model_name: str = None, inputs: list[str]
) -> list[list[float]]:
    """
    * 用原始的 fetch 方式调用 huggingface 上的embedding 模型
    *
    * 相关参考： 参考文档： https://github.com/huggingface/text-embeddings-inference
    * 常用模型参考：
    *  jinaai/jina-embeddings-v2-base-zh //维度 768
    *  mixedbread-ai/mxbai-embed-large-v1 //维度1024
    *  @cf/baai/bge-large-en-v1.5 //
    * infgrad/stella-large-zh-v2
    """
    if not settings.HUGGINGFACEHUB_API_TOKEN:
        raise Exception("missing HUGGINGFACEHUB_API_TOKEN")
    model = model_name or "mixedbread-ai/mxbai-embed-large-v1"
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACEHUB_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model_name,
        "embedding_type": "float",
        "inputs": inputs,
    }
    logger.info("调用 hf embedding %s", settings.HUGGINGFACEHUB_API_TOKEN)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()


async def call_embedding_1024(content: str):
    result = await embedding_hf(inputs=[content])
    return result
