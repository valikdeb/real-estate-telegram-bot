import asyncio
import os
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from handlers import questions, different_types


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    load_dotenv(".env")
    token = os.getenv("TOKEN_API")

    if not token:
        logger.error("TOKEN_API is not set in the environment variables.")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(questions.router, different_types.router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
    except Exception as e:
        logger.error(f"Bot stopped during exception {e}")
