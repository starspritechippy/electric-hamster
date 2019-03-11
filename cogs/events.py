import traceback
import sys
from discord.ext import commands
from discord.ext.commands import errors
import discord
import asyncio


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            'logged in as "{}#{}". \nIn case you need it, my ID is {}'.format(
                self.bot.user.name, self.bot.user.discriminator, self.bot.user.id
            )
        )
        await self.bot.change_presence(
            activity=discord.Game(type=0, name=f".help"), status=discord.Status.online
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, (errors.BadArgument, errors.MissingRequiredArgument)):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = "".join(_traceback)
            error = "```py\n{2}{0}: {3}\n```".format(
                type(err).__name__, ctx.message.content, _traceback, err
            )
            print(error)

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(
                f"You're being rate limited... Try again in {err.retry_after:.0f} seconds.",
                delete_after=4,
            )

        elif isinstance(err, errors.CommandNotFound):
            pass


def setup(bot):
    bot.add_cog(events(bot))
