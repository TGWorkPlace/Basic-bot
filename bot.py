import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN
from webserver import run_webserver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BroadcastBot(Client):
    def __init__(self):
        super().__init__(
            name="broadcast_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        me = await self.get_me()
        logger.info(f"Bot started: @{me.username}")

        self._web_runner = await run_webserver()

    async def stop(self, *args, **kwargs):
        if hasattr(self, "_web_runner"):
            await self._web_runner.cleanup()
        await super().stop(*args, **kwargs)
        logger.info("Bot stopped.")


app = BroadcastBot()


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply("Hi")


if __name__ == "__main__":
    app.run()
