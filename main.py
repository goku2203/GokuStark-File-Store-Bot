import asyncio
import logging
import os

import aiohttp
from aiohttp import web
from pyrogram import compose

from bot import Bot
from plugins import web_server
from config import (
    SESSION, WORKERS, DB_CHANNEL, FSUBS, TOKEN, ADMINS, MESSAGES, AUTO_DEL,
    DB_URI, DB_NAME, API_ID, API_HASH, PROTECT, DISABLE_BTN, PORT
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("main")


async def start_web() -> web.AppRunner:
    """Web server first start aagum, appo dhan Render ku port open nu theriyum."""
    runner = web.AppRunner(await web_server())
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()
    log.info(f"Web server started on port {PORT}")
    return runner


async def keep_alive():
    """Render free plan 15 min idle na sleep aagidum. Adhukku self-ping."""
    base_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("APP_URL")
    if not base_url:
        log.info("RENDER_EXTERNAL_URL illa - keep-alive skip.")
        return
    url = base_url.rstrip("/") + "/health"
    await asyncio.sleep(60)
    while True:
        try:
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    log.info(f"Keep-alive ping -> {resp.status}")
        except Exception as e:
            log.warning(f"Keep-alive ping failed: {e}")
        await asyncio.sleep(600)


async def run_bot():
    app = [
        Bot(SESSION, WORKERS, DB_CHANNEL, FSUBS, TOKEN, ADMINS, MESSAGES, AUTO_DEL,
            DB_URI, DB_NAME, API_ID, API_HASH, PROTECT, DISABLE_BTN)
    ]
    await compose(app)


async def runner():
    web_runner = await start_web()
    ping_task = asyncio.create_task(keep_alive())
    try:
        await run_bot()
    finally:
        ping_task.cancel()
        await web_runner.cleanup()


if __name__ == "__main__":
    asyncio.run(runner())
