import asyncio
import threading

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates

from mtmai.core.__version__ import version
from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_vercel
from mtmai.core.logging import get_logger
from mtmlib.env import is_in_docker, is_in_huggingface, is_in_windows

from .cli import Cli

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    if len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    return f"{route.name}"


openapi_tags = [
    {
        "name": "admin",
        "description": "这部分API与管理员操作相关, 包括用户管理和权限控制等功能. ",
    },
]


app = FastAPI(
    # docs_url=None,
    # redoc_url=None,
    title=settings.PROJECT_NAME,
    description="mtmai description(group)",
    version=version,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "syntaxHighlight.theme": "obsidian",
    },
    openapi_tags=openapi_tags,
)
templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):  # noqa: ARG001
    return JSONResponse(status_code=500, content={"detail": str(exc)})


# 实验: 使用中间件的方式动态设置 cors
class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        response = await call_next(request)

        if origin and origin in settings.BACKEND_CORS_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Authorization, Content-Type, X-CSRF-Token"
        )

        return response


def setup_main_routes():
    from mtmai.api.main import api_router
    from mtmai.api.routes import home

    app.include_router(home.router)
    app.include_router(api_router, prefix=settings.API_V1_STR)


setup_main_routes()


def setup_mtmscreentocode_router():
    """实验: 集成 mtmscreentocode 的 router"""
    from mtmscreentocode.routes import evals, generate_code, home, screenshot

    app.include_router(generate_code.router)
    app.include_router(screenshot.router)
    app.include_router(home.router)
    app.include_router(evals.router)


setup_mtmscreentocode_router()


async def serve():
    import uvicorn

    if settings.OTEL_ENABLED:
        from mtmai.mtlibs import otel

        otel.setup_otel(app)

    app.add_middleware(DynamicCORSMiddleware)
    if settings.BACKEND_CORS_ORIGINS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            # allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    start_deamon_serve()

    if is_in_windows():
        settings.PORT = 8555

    config = uvicorn.Config(
        app,
        host=settings.SERVE_IP,
        port=settings.PORT,
        log_level="info",
        reload=not settings.is_production,
    )
    host = (
        "127.0.0.1"
        if settings.SERVE_IP == "0.0.0.0"
        else settings.server_host.split("://")[-1]
    )
    server_url = f"{settings.server_host.split('://')[0]}://{host}:{settings.PORT}"

    logger.info("🚀 mtmai api serve on : %s", server_url)
    server = uvicorn.Server(config)
    await server.serve()


class CliServe(Cli):
    """启动http 服务器"""

    def run(self, *args, **kwargs) -> None:
        """运行子命令"""
        logger.info("子命令： 启动http 服务器   ")
        logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
        asyncio.run(serve())


def start_deamon_serve():
    """
    启动后台独立服务
    根据具体环境自动启动
    """
    if (
        not settings.is_in_vercel
        and not settings.is_in_gitpod
        and settings.CF_TUNNEL_TOKEN
        and not is_in_huggingface()
        and not is_in_windows()
    ):
        import asyncio

        from mtmlib import tunnel

        threading.Thread(target=lambda: asyncio.run(tunnel.start_cloudflared())).start()

        if not is_in_vercel() and not settings.is_in_gitpod:
            from mtmai.api.routes.server import run_searxng_server

            threading.Thread(target=run_searxng_server).start()
        if (
            not settings.is_in_vercel
            and not settings.is_in_gitpod
            and not is_in_windows()
        ):
            from mtmai.api.routes.server import start_front_app

            threading.Thread(target=start_front_app).start()

        if not is_in_vercel() and not settings.is_in_gitpod and not is_in_windows():
            from mtmai.api.routes.server import run_kasmvnc

            threading.Thread(target=run_kasmvnc).start()

        if (
            not settings.is_in_vercel
            and not settings.is_in_gitpod
            and not is_in_windows()
        ):
            from mtmai.api.routes.server import start_code_server

            threading.Thread(target=start_code_server).start()

        if is_in_docker():
            from mtmai.mtlibs.server.easyspider import run_easy_spider_server

            threading.Thread(target=run_easy_spider_server).start()
