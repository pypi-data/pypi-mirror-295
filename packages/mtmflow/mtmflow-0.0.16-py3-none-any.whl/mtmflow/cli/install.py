import asyncio
import threading

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates



class CliInstall():
    """安装 自定义的 langflow 服务器及运行环境"""

    def run(self, *args, **kwargs) -> None:
        print(" todo install langflow")

