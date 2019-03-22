import os
import asyncio
import asyncpg

from data import Bot
from utils import default

config = default.get("config.json")


async def run():
    help_attrs = dict(hidden=True)
    credentials = {
        "user": config.dbname,
        "password": config.dbpass,
        "database": config.database,
        "host": "127.0.0.1",
    }
    db = await asyncpg.create_pool(**credentials)

    await db.execute("CREATE TABLE IF NOT EXISTS afk(userid bigint, reason varchar);")

    bot = Bot(command_prefix=config.prefix, pm_help=True, help_attrs=help_attrs, db=db)
    bot.remove_command("help")
    try:
        print("Logging in...")
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                bot.load_extension(f"cogs.{name}")
        await bot.start(config.token)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
