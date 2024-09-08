import logging

from fastapi import APIRouter, Header, Response
from fastapi.responses import StreamingResponse
from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

from mtmai.agents.site_crew.crew import post_generate
from mtmai.api.deps import GraphAppDep, OptionalUserDep, SessionDep
from mtmai.core.config import settings
from mtmai.curd.curd_blog import PostCreate, create_blog_post
from mtmai.models.agent import (
    AgentBootstrap,
    AgentMeta,
    AgentTask,
    ChatBotUiState,
    UiMessage,
)

# from mtmai.models.blog import PostCreate
from mtmai.models.form import CommonFormData, CommonFormField
from mtmai.models.models import Agent
from mtmai.mtlibs import aisdk, mtutils

router = APIRouter()

logger = logging.getLogger()
graphs: dict[str, CompiledStateGraph] = {}


async def get_agent_from_headers(chat_agent: str = Header(None)):
    return chat_agent


def get_agent_by_id(db: Session, agent_id: str):
    return db.exec(select(Agent).where(Agent.id == agent_id)).one()


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


async def agent_event_stream(
    *, graph: CompiledStateGraph, inputs, config: RunnableConfig, session: Session
):
    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=config,
    ):
        thread_id = config.get("configurable").get("thread_id")
        user_id = config.get("configurable").get("user_id")
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        # logger.info("%s:node: %s", kind, node_name)
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
                            thread_id=thread_id,
                            user_id=user_id,
                            component=uim.component,
                            props=uim.props,
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


class CompletinRequest(BaseModel):
    thread_id: str | None = None
    prompt: str
    option: str | None = None
    task: dict | None = None


@router.post("/completions")
async def completions(
    user: OptionalUserDep, db: SessionDep, graphapp: GraphAppDep, req: CompletinRequest
):
    if req.task:
        # 如果是任务请求，就直接根据请求和后台的相关配置直接完成任务
        task_name = req.task.get("name")
        logger.info("task_name: %s", task_name)
        return {"task_name": task_name}

    thread_id = req.thread_id
    if not thread_id:
        thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {"thread_id": thread_id, "user_id": user.id}
    }

    state = await graphapp.aget_state(thread)
    pre_messages = state.values.get("messages", [])
    new_user_message = ChatMessage(role="user", content=req.prompt)
    inputs = {
        "user_id": user.id,
        "user_input": req.prompt,
        "user_option": req.option,
        "messages": [*pre_messages, new_user_message],
        "artifacts": [],
    }

    if state.created_at is not None:
        await graphapp.aupdate_state(
            thread,
            inputs,
            as_node="human_node",
            # as_node="supervisor",
        )
        inputs = None

    response = StreamingResponse(
        agent_event_stream(
            graph=graphapp,
            inputs=inputs,
            config=thread,
            session=db,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


@router.post("/uistate", response_model=ChatBotUiState)
async def uistate(
    user: OptionalUserDep, db: SessionDep, graphapp: GraphAppDep, req: CompletinRequest
):
    """目前仅作占位符, 让前端可以通过 openapi 跟获取到ChatBotUiState 类型"""
    return ChatBotUiState()


class AgentTaskRequest(BaseModel):
    task_name: str


class AgentTaskResponse(BaseModel):
    task_id: str
    result: str


@router.post("/run_agent_task", response_model=AgentTaskResponse)
async def run_agent_task(req: AgentTaskRequest, user: OptionalUserDep, db: SessionDep):
    """agent 任务调用请求"""
    task_req = AgentTaskRequest(
        task_name="post_generate",
    )
    result = await post_generate(task_req)
    create_post_result = await create_blog_post(
        session=db, blog_post_create=PostCreate(title="title1", content=result.raw)
    )
    logger.info("create_post_result: %s", create_post_result)
    return AgentTaskResponse(task_id=req.task_name, result=result.raw)


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
            title="请输入标题",
            fields=[
                CommonFormField(name="title", label="标题", type="text", required=True),
                CommonFormField(
                    name="content", label="内容", type="text", required=True
                ),
            ],
        )
    )

    return result
