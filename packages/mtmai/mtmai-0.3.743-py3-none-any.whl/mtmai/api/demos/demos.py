import asyncio
import json
import logging
import threading

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

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
