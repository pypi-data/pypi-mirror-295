from fastapi import APIRouter
from mtmlib.queue.queue import (
    MessageAckRequest,
    MessagePublic,
    MessagePullReq,
    MessagePullResponse,
    MessagePullResponseItem,
    MessageSendPublic,
)

from mtmai.api.deps import MqDep

router = APIRouter()

READ_THRESHOLD = 10  # 设置 read_ct 的删除阈值


@router.post("/pull", response_model=MessagePullResponse)
async def pull(queue: MqDep, req: MessagePullReq):
    resp = MessagePullResponse(data=[])
    for item in req.items:
        queue.create_queue(item.queue)

        messages = queue.read_batch(item.queue)
        # for m in messages:
        #     if m.read_ct > READ_THRESHOLD:
        #         queue.delete(queue=req.queue, msg_id=m.msg_id)
        #         # TODO: 删除的消息不要返回给客户端。
        # msgs = [
        #     MessagePublic(
        #         msg_id=m.msg_id,
        #         enqueued_at=m.enqueued_at,
        #         read_ct=m.read_ct,
        #         message=m.message,
        #         vt=m.vt,
        #     )
        #     for m in messages
        # ]
        msgs = [
            MessagePublic(
                msg_id=m.msg_id,
                enqueued_at=m.enqueued_at,
                read_ct=m.read_ct,
                message=m.message,
                vt=m.vt,
            )
            for m in messages
            if m.read_ct <= READ_THRESHOLD
            or not queue.delete(queue=req.queue, msg_id=m.msg_id)
        ]
        resp.data.append(MessagePullResponseItem(queue=item.queue, messages=msgs))
    return resp


@router.post("")
async def send(queue: MqDep, req: MessageSendPublic):
    queue.send_batch(queue=req.queue, messages=req.messages)


@router.post("/ack")
async def ack(queue: MqDep, req: MessageAckRequest):
    for msg_id in req.msg_ids:
        queue.delete(queue=req.queue, msg_id=int(msg_id))
