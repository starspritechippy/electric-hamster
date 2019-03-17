import io
import textwrap
import traceback
import shlex
import os
from subprocess import Popen, PIPE
from contextlib import redirect_stdout
from discord.ext import commands


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.admins = [262133866062413825, 127452209070735361]

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # Remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

    def run_shell(command):
        with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as proc:
            return [std.decode("utf-8") for std in proc.communicate()]

    @commands.command(hidden=True)
    async def load(self, ctx, extension_name: str):
        """Loads an extension."""
        if ctx.author.id not in self.admins:
            return
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await bot.say("cog **{}** successfully loaded.".format(extension_name))


    @commands.command(hidden=True)
    async def unload(self, ctx, extension_name: str):
        """Unloads an extension."""
        if ctx.author.id not in self.admins:
            return
        bot.unload_extension(extension_name)
        await bot.say("cog **{}** successfully unloaded.".format(extension_name))


    @commands.command(hidden=True)
    async def reboot(self, ctx):
        """ Reboot the bot """
        if ctx.author.id not in self.admins:
            return
        await ctx.send("Rebooting now...")
        time.sleep(1)
        await self.bot.logout()


    @commands.command(hidden=True, aliases=["pull"])
    async def update(self, ctx, silently: bool = False):
        """ Gets latest commits and applies them from git """
        if ctx.author.id not in self.admins:
            return
        await ctx.message.add_reaction("a:loading:528744937794043934")

        def run_shell(command):
            with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as proc:
                return [std.decode("utf-8") for std in proc.communicate()]

        pull = await self.bot.loop.run_in_executor(
            None, run_shell, "git pull origin master"
        )
        msg = await ctx.send(f"```css\n{pull}\n```", delete_after=6)
        await ctx.message.remove_reaction("a:loading:528744937794043934", member=ctx.me)
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                self.bot.unload_extension(f"cogs.{name}")
                self.bot.load_extension(f"cogs.{name}")
        await ctx.message.add_reaction(":done:513831607262511124")


def setup(bot):
    bot.add_cog(admin(bot))
