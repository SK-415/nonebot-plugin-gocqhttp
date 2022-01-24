from typing import Dict

from nonebot import get_driver

from .log import logger
from .plugin_config import config
from .process import GoCQProcess
from .process.download import BINARY_PATH, download_gocq

PROCESSES: Dict[int, GoCQProcess] = {}


@get_driver().on_startup
async def startup():
    if config.FORCE_DOWNLOAD or not BINARY_PATH.is_file():
        await download_gocq()

    for account in config.ACCOUNTS:
        logger.info(f"Starting GoCQ process for <e>{account.uin}</e>")
        process = GoCQProcess(account)
        PROCESSES[account.uin] = process
        await process.start()

    return
