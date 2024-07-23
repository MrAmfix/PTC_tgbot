import asyncio
from aiogram import Dispatcher
from bot.bot import rt, bot


async def main():
    print('Bot started')
    dp = Dispatcher()
    dp.include_routers(rt)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
