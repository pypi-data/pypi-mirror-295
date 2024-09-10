import logging

from fastapi import APIRouter, Header, HTTPException, Response
from fastapi.responses import StreamingResponse
from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, func, select

from mtmai.agents.graphchatdemo.graph import MtmAgent

# from mtmai.agents.site_crew.crew import SitePostGenerateInput, crew_post_generate
from mtmai.api.deps import (
    CheckPointerDep,
    GraphAppDep,
    HostDep,
    OptionalUserDep,
    SessionDep,
)
from mtmai.core.config import settings
from mtmai.models.agent import (
    AgentBootstrap,
    AgentMeta,
    AgentTask,
    Chatbot,
    UiMessage,
    UiMessageBase,
)

# from mtmai.models.blog import PostCreate
from mtmai.models.form import CommonFormData, CommonFormField

# from mtmai.models.models import Agent
from mtmai.models.models import User
from mtmai.mtlibs import aisdk, mtutils

router = APIRouter()

logger = logging.getLogger()
graphs: dict[str, CompiledStateGraph] = {}


async def get_agent_from_headers(chat_agent: str = Header(None)):
    return chat_agent


# def get_agent_by_id(db: Session, agent_id: str):
#     return db.exec(select(Agent).where(Agent.id == agent_id)).one()


agent_list = []


def register_agent(agent_obj):
    agent_list.append(agent_obj)


def get_agent_by_name_v2(agent_name: str):
    if agent_name == "graphchatdemo":
        from mtmai.agents.graphchatdemo.graph import MtmAgent

        return MtmAgent

    return None


agents = {}


def get_agent_by_name_v3(agent_name: str):
    global agents
    a = agents.get(agent_name)
    if not a:
        agents[agent_name] = get_agent_by_name_v2(agent_name)
    return agents.get(agent_name)


class AgentsPublic(SQLModel):
    data: list[AgentMeta]
    count: int


all_agents = [
    AgentMeta(
        id="mtmaibot",
        name="mtmaibot",
        label="AI聊天",
        base_url=settings.API_V1_STR + "/mtmaibot",
        description="基于 graph 的综合智能体(开发版)",
        # is_dev=True,
    ),
    # AgentMeta(
    #     id="mteditor",
    #     name="mteditor",
    #     label="AI所见即所得编辑器",
    #     base_url=settings.API_V1_STR + "/mteditor",
    #     description="演示版",
    #     # agent_type="mtmeditor",
    #     graph_image=settings.API_V1_STR + "/mteditor/image",
    # ),
]


@router.get("/agent_bootstrap", response_model=AgentBootstrap)
async def agent_bootstrap(user: OptionalUserDep, db: SessionDep):
    """
    获取 agent 的配置，用于前端加载agent的配置
    """
    logger.info("agent_bootstrap")
    return AgentBootstrap(is_show_fab=True)


@router.get(
    "",
    summary="获取 Agent 列表",
    description=(
        "此端点用于获取 agent 列表。支持分页功能"
        "可以通过 `skip` 和 `limit` 参数控制返回的 agent 数量。"
    ),
    response_description="返回包含所有 agent 的列表及总数。",
    response_model=AgentsPublic,
    responses={
        200: {
            "description": "成功返回 agent 列表",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"name": "agent1", "status": "active"},
                            {"name": "agent2", "status": "inactive"},
                        ],
                        "count": 2,
                    }
                }
            },
        },
        401: {"description": "未经授权的请求"},
        500: {"description": "服务器内部错误"},
    },
)
def items(
    user: OptionalUserDep,
    skip: int = 0,
    limit: int = 100,
):
    return AgentsPublic(data=all_agents, count=len(all_agents))


@router.get("/{agent_id}", response_model=AgentMeta | None)
def get_item(db: SessionDep, user: OptionalUserDep, agent_id: str):
    for agent in all_agents:
        if agent.id == agent_id:
            return agent
    return None


@router.get(
    "/image/{agent}",
    summary="获取工作流图像",
    description="此端点通过给定的 agent ID，生成工作流的图像并返回 PNG 格式的数据。",
    response_description="返回 PNG 格式的工作流图像。",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"description": "Agent 未找到"},
    },
)
async def image(user: OptionalUserDep, graphapp: GraphAppDep):
    image_data = graphapp.get_graph(xray=1).draw_mermaid_png()
    return Response(content=image_data, media_type="image/png")


class AgentStateRequest(BaseModel):
    agent_id: str | None = None
    thread_id: str


@router.post(
    "/state",
    summary="获取工作流状态",
    description="",
    response_description="返回工作流当前完整状态数据",
)
async def state(req: AgentStateRequest, user: OptionalUserDep, graphapp: GraphAppDep):
    thread: RunnableConfig = {
        "configurable": {"thread_id": req.thread_id},
        "recursion_limit": 200,
    }
    state = await graphapp.aget_state(thread)
    return state


class CompletinRequest(BaseModel):
    thread_id: str | None = None
    chat_id: str | None = None
    prompt: str
    option: str | None = None
    task: dict | None = None


async def agent_event_stream(
    *,
    session: Session,
    user: User,
    req: CompletinRequest,
    checkpointer: CheckPointerDep,
):
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    logger.info("database connecting ...")
    await pool.open()
    checkpointer2 = AsyncPostgresSaver(pool)
    agent_inst = MtmAgent()

    graph = agent_inst.build_flow().compile(
        checkpointer=checkpointer2,
        interrupt_after=["human_node"],
        debug=True,
    )
    chat_id = req.chat_id
    if not chat_id:
        # 如果没有提供 chat_id，创建新的 chat
        chatbot = Chatbot(
            name="New Chat",
            description="New Chat",
        )
        session.add(chatbot)
        session.commit()
        chat_id = chatbot.id
        # 通知前端创建了新的chat_id
        yield aisdk.data(
            {
                "chat_id": chatbot.id,
            }
        )
    else:
        # 确保提供的 chat_id 存在
        chatbot = session.exec(select(Chatbot).where(Chatbot.id == chat_id)).first()
        if not chatbot:
            # 如果提供的 chat_id 不存在，创建新的 chat
            chatbot = Chatbot(
                name="New Chat",
                description="New Chat",
            )
            session.add(chatbot)
            session.commit()
            chat_id = chatbot.id
            # 通知前端创建了新的chat_id
            yield aisdk.data(
                {
                    "chat_id": chatbot.id,
                }
            )

    new_message = UiMessage(
        component="UserMessage",
        content=req.prompt,
        props={"content": req.prompt},
        chatbot_id=chat_id,
        role="user",
    )
    session.add(new_message)
    session.commit()

    # 加载聊天消息历史
    # FIXME: 用户消息的加载有待优化
    chat_messages = session.exec(
        select(UiMessage)
        .where(UiMessage.chatbot_id == chat_id)
        .order_by(UiMessage.created_at)
    ).all()

    # 从数据库的聊天记录构造 langgraph 的聊天记录
    langgraph_messages = []
    for message in chat_messages:
        if message.content:
            langgraph_message = ChatMessage(
                role="user" if message.role == "user" else "assistant",
                content=message.content if message.role == "user" else message.response,
            )
            langgraph_messages.append(langgraph_message)

    thread_id = req.thread_id
    if not thread_id:
        thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {"thread_id": thread_id, "user_id": user.id}
    }

    inputs = {
        "user_id": user.id,
        "user_input": req.prompt,
        "user_option": req.option,
        "messages": [*langgraph_messages],
        # "artifacts": [],
    }
    state = await graph.aget_state(thread)

    if state.created_at is not None:
        # 是人机交互继续执行的情况
        await graph.aupdate_state(
            thread,
            inputs,
            as_node="human_node",
            # as_node="supervisor",
        )
        inputs = None

    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
    ):
        thread_id = thread.get("configurable").get("thread_id")
        user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        if kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    yield aisdk.text(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        if kind == "on_chain_stream":
            if data and node_name == "entry_node":
                chunk_data = data.get("chunk", {})
                picked_data = {
                    key: chunk_data[key]
                    for key in ["ui_messages", "uistate"]
                    if key in chunk_data
                }

                if picked_data:
                    yield aisdk.data(picked_data)
        if kind == "on_chain_end":
            chunk_data = data.get("chunk", {})

            if node_name == "human_node":
                output = data.get("output")
                if output:
                    artifacts = data.get("output").get("artifacts")
                    if artifacts:
                        yield aisdk.data({"artifacts": artifacts})

                ui_messages = output.get("ui_messages", [])
                if len(ui_messages) > 0:
                    for uim in ui_messages:
                        db_ui_message2 = UiMessage(
                            # thread_id=thread_id,
                            chatbot_id=chat_id,
                            user_id=user_id,
                            component=uim.component,
                            content=uim.content,
                            props=uim.props,
                            artifacts=uim.artifacts,
                        )
                        session.add(db_ui_message2)
                        session.commit()

                    # 跳过前端已经乐观更新的组件
                    skip_components = ["UserMessage", "AiCompletion"]
                    filterd_components = [
                        x for x in ui_messages if x.component not in skip_components
                    ]
                    yield aisdk.data(
                        {
                            "ui_messages": filterd_components,
                        }
                    )
                if output.get("uistate"):
                    yield aisdk.data(
                        {
                            "uistate": output.get("uistate"),
                        }
                    )

            if node_name == "entry_node":
                task_title = data.get("task_title", "no-title")
                item = AgentTask(thread_id=thread_id, user_id=user_id, title=task_title)
                session.add(item)
                session.commit()

            if node_name == "LangGraph":
                final_messages = event["data"]["output"]["messages"]
                for message in final_messages:
                    message.pretty_print()
                logger.info("中止节点")

        if kind == "on_tool_start":
            logger.info("(@stream)工具调用开始 %s", node_name)
        # if kind == "on_tool_end":
        #     output = data.get("output")
        #     if output and output.artifact:
        #         yield aisdk.data(output.artifact)

    yield aisdk.finish()


@router.post("/completions")
async def completions(
    user: OptionalUserDep,
    db: SessionDep,
    req: CompletinRequest,
    checkpointer: CheckPointerDep,
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    response = StreamingResponse(
        agent_event_stream(
            req=req,
            user=user,
            session=db,
            checkpointer=checkpointer,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


# @router.post("/uistate", response_model=ChatBotUiState)
# async def uistate(
#     user: OptionalUserDep, db: SessionDep, graphapp: GraphAppDep, req: CompletinRequest
# ):
#     """目前仅作占位符, 让前端可以通过 openapi 跟获取到ChatBotUiState 类型"""
#     return ChatBotUiState()


class AgentTaskRequest(BaseModel):
    task_name: str


class AgentTaskResponse(BaseModel):
    task_id: str
    result: str


@router.post("/run_agent_task", response_model=AgentTaskResponse)
async def run_agent_task(
    req: AgentTaskRequest,
    user: OptionalUserDep,
    db: SessionDep,
    host: HostDep,
):
    """agent 任务调用请求"""
    # task_req = AgentTaskRequest(
    #     task_name="post_generate",
    # )

    # site_data = await get_site(db, host)
    # # result = await crew_post_generate(
    # #     SitePostGenerateInput(title="Ai 最新咨询", site_data=site_data)
    # # )
    # # inputs = {
    # #     "company_domain": "careers.wbd.com",
    # #     "company_description": "Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world’s most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We're home to the world’s best storytellers, creating world-class products for consumers",
    # #     "hiring_needs": "Production Assistant, for a TV production set in Los Angeles in June 2025",
    # #     "specific_benefits": "Weekly Pay, Employee Meals, healthcare",
    # # }
    # # result = JobPostingCrew().crew().kickoff(inputs=inputs)
    # create_post_result = await create_blog_post(
    #     session=db, blog_post_create=PostCreate(title="title1", content=result.raw)
    # )
    # logger.info("create_post_result: %s", create_post_result)
    return AgentTaskResponse(task_id=req.task_name, result="todo123123")


class TaskFormRequest(BaseModel):
    task_name: str


class TaskFormResponse(BaseModel):
    form: CommonFormData


@router.post("/task_form", response_model=TaskFormResponse)
async def task_form(req: TaskFormRequest, user: OptionalUserDep, db: SessionDep):
    """根据任务请求，返回任务表单"""
    # 开发中，暂时返回固定的表单

    result = TaskFormResponse(
        form=CommonFormData(
            title="随机生成一篇文章",
            fields=[
                CommonFormField(name="title", label="标题", type="text", required=True),
                CommonFormField(
                    name="content", label="内容", type="text", required=True
                ),
            ],
        )
    )

    return result


class ChatMessagesItem(UiMessageBase):
    id: str


class ChatMessagesResponse(SQLModel):
    data: list[ChatMessagesItem]
    count: int


class AgentChatMessageRequest(SQLModel):
    chat_id: str
    skip: int = 0
    limit: int = 100


@router.post("/chat_messages", response_model=ChatMessagesResponse)
async def messages(session: SessionDep, req: AgentChatMessageRequest):
    """获取聊天消息"""
    count_statement = (
        select(func.count())
        .select_from(UiMessage)
        .where(UiMessage.chatbot_id == req.chat_id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(UiMessage)
        .where(UiMessage.chatbot_id == req.chat_id)
        .offset(req.skip)
        .limit(req.limit)
    )
    items = session.exec(statement).all()
    return ChatMessagesResponse(data=items, count=count)
