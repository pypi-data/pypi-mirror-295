"""
安装 langflow 并配置
"""

import asyncio
import logging
from pathlib import Path

from mtmlib.mtutils import bash

logger = logging.getLogger()
langflow_repo = "https://github.com/langflow-ai/langflow"
langflow_targt_dir = str(Path("langflow"))


async def install_langflow():
    if not Path(langflow_targt_dir).exists():
        bash(f"git clone {langflow_repo} {langflow_targt_dir}")
    else:
        bash(f"cd {langflow_targt_dir} && git pull")

    # 安装后端
    bash(
        f"cd {langflow_targt_dir} && python -m venv venv && source venv/bin/activate && pip install ."
    )
    # bash(f"cd {langflow_targt_dir} && poetry install")


async def run_langflow():
    print(f"🚀 TODO: Running Langflow in {langflow_targt_dir}")
    if not Path(langflow_targt_dir).exists():
        await install_langflow()

    bash(f"cd {langflow_targt_dir} && source venv/bin/activate && python -m langflow")


def register_install_commands(cli):
    @cli.command()
    def mtmflow():
        from mtmai.mtlibs.server.mtmflow import run_langflow

        asyncio.run(run_langflow())
