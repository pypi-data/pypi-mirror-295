import asyncio
import json
import logging
from collections.abc import AsyncGenerator, Callable

import fastapi
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from mtmai.core.config import settings

router = APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)


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
