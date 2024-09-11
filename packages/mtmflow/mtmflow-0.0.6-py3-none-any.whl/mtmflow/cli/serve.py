import asyncio
import threading

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates

from mtmflow.core.config import settings

import logging


# logger = get_logger()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    if len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    return f"{route.name}"


# openapi_tags = [
#     {
#         "name": "admin",
#         "description": "这部分API与管理员操作相关, 包括用户管理和权限控制等功能. ",
#     },
# ]


app = FastAPI(
    # docs_url=None,
    # redoc_url=None,
    # title=settings.PROJECT_NAME,
    description="mtmflow description(group)",
    # version=version,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "syntaxHighlight.theme": "obsidian",
    },
    # openapi_tags=openapi_tags,
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
    # from mtmai.api.main import api_router
    # from mtmai.api.routes import home

    # app.include_router(home.router)
    from mtmflow.api.main import api_router
    # app.include_router(api_router, prefix=settings.API_V1_STR)


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
    host = (
        "127.0.0.1"
        if settings.SERVE_IP == "0.0.0.0"
        else settings.server_host.split("://")[-1]
    )
    server_url = f"{settings.server_host.split('://')[0]}://{host}:{settings.PORT}"

    config = uvicorn.Config(
        app,
        host=settings.SERVE_IP,
        port=settings.PORT,
        log_level="info",
        reload=not settings.is_production,
    )
    logger.info("🚀 mtmflow api serve on : %s", server_url)
    server = uvicorn.Server(config)
    await server.serve()


class CliServe():
    """启动http 服务器"""

    def run(self, *args, **kwargs) -> None:
        print("hello mtmflow server")

