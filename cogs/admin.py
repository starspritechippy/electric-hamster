import io
import textwrap
import traceback
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


    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body = ''):
        if ctx.author.id not in self.admins:
            return
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await self.bot.say(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await self.bot.say(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await self.bot.say(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await self.bot.say(f'```py\n{value}{ret}\n```')



    @commands.command(pass_context=True)
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


    @commands.command(pass_context=True)
    async def unload(self, ctx, extension_name: str):
        """Unloads an extension."""
        if ctx.author.id not in self.admins:
            return
        bot.unload_extension(extension_name)
        await bot.say("cog **{}** successfully unloaded.".format(extension_name))


def setup(bot):
    bot.add_cog(admin(bot))
