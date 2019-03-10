import traceback
import sys
from discord.ext import commands
import discord
import asyncio


class error:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error: Exception, ctx: commands.Context):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            m = await self.bot.send_message(ctx.message.channel, "I don't have a command like this.\nIf this was triggered by accident, please ignore.")
            await asyncio.sleep(3)
            await self.bot.delete_message(m)
            return

        elif isinstance(error, commands.DisabledCommand):
            await self.bot.send_message(ctx.message.channel, '{} has been disabled.'.format(ctx.command))
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await self.bot.send_message(ctx.message.author, '{} can not be used in Private Messages.'.format(ctx.command))
                return
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await self.bot.send_message(ctx.message.channel, 'I could not find that member. Please try again.')
                return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(error(bot))
