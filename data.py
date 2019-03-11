import asyncio
import discord

from collections import Counter
from utils import default
from discord.ext.commands import AutoShardedBot

config = default.get("config.json")


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = kwargs.pop("db")

    async def on_message(self, message):
        query = "SELECT * FROM afk;"
        row = await self.db.fetch(query)
        for entry in row:
            if entry['userid'] == message.author.id:
                username = self.get_user(entry['userid'])
                await message.channel.send(f"Welcome back {username}!")
                query = "DELETE FROM afk WHERE userid=$1;"
                await self.db.execute(query, message.author.id)
        if message.mentions:
            for entry in row:
                if message.mentions[0].id == entry['userid']:
                    username = self.get_user(entry['userid'])
                    await message.channel.send(f"{username} isn't available: {entry['reason']}")
                    break
        await self.process_commands(message)
