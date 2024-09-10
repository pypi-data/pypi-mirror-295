import logging
from pathlib import Path

from fastapi import APIRouter
from mtmai.core.config import settings
from mtmai.mtlibs.mtutils import command_exists

from mtmlib.httpUtils import download_file
from mtmlib.mtutils import bash

router = APIRouter()
logger = logging.getLogger()


def start_cloudflared():
    if not settings.CF_TUNNEL_TOKEN:
        logger.warning("missing env CF_TUNNEL_TOKEN")
        return
    install()
    bash("sudo pkill cloudflared || true")
    logger.info("----start up cloudflared tunnel----")
    bash(
        f"""cloudflared tunnel --no-autoupdate --http2-origin run --token {settings.CF_TUNNEL_TOKEN} & """
    )


# @router.get("/start", include_in_schema=False)
# def start():
#     threading.Thread(target=start_cloudflared).start()


# @router.get("/install", include_in_schema=False)
def install():
    if not command_exists("cloudflared"):
        logger.info("cloudflared 命令不存在现在安装")
        download_file(
            "https://github.com/cloudflare/cloudflared/releases/download/2024.1.5/cloudflared-linux-amd64",
            Path.home() / ".local/bin/cloudflared",
        )
    # return "installed"
