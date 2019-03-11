from utils import pagenator
from discord.ext import commands
import discord
import random


class _help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def category_gen(self, ctx):
        categories = {}

        for command in set(self.bot.walk_commands()):
            try:
                if command.category not in categories:
                    categories.update({command.category: []})
            except AttributeError:
                cog = command.cog_name or "Bot"
                if command.cog_name not in categories:
                    categories.update({cog: []})

        for command in set(ctx.bot.walk_commands()):
            if not command.hidden:
                try:
                    if command.category:
                        categories[command.category].append(command)
                except AttributeError:
                    cog = command.cog_name or "Bot"
                    categories[cog].append(command)

        return categories

    async def commandMapper(self, ctx):
        pages = []

        for category, commands in (await self.category_gen(ctx)).items():
            if not commands:
                continue
            cog = ctx.bot.get_cog(category)
            if cog:
                category = f"**⚙️ {category}**"
            commands = ", ".join([c.qualified_name for c in commands])
            embed = (
                discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    title=f"{ctx.bot.user.display_name} Commands",
                    description=f"{category}",
                )
                .set_footer(
                    text=f"Type {ctx.prefix}help <command> for more help".replace(
                        ctx.me.mention, "@Pawbot "
                    ),
                    icon_url=ctx.author.avatar_url,
                )
                .add_field(name="**Commands:**", value=f"``{commands}``")
            )
            pages.append(embed)
        await pagenator.SimplePaginator(
            extras=sorted(pages, key=lambda d: d.description)
        ).paginate(ctx)

    async def cogMapper(self, ctx, entity, cogname: str):
        try:
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    title=f"{ctx.bot.user.display_name} Commands",
                    description=f"**⚙️ {cogname}**",
                )
                .add_field(
                    name="**Commands:**",
                    value=f"``{', '.join([c.qualified_name for c in set(ctx.bot.walk_commands()) if c.cog_name == cogname])}``",
                )
                .set_footer(
                    text=f"Type {ctx.prefix}help <command> for more help".replace(
                        ctx.me.mention, "@Pawbot "
                    ),
                    icon_url=ctx.author.avatar_url,
                )
            )
        except BaseException:
            await ctx.send(
                f":x: | **Command or category not found. Use {ctx.prefix}help**",
                delete_after=10,
            )

    @commands.command(aliases=["?"], hidden=True)
    async def help(self, ctx, *, command: str = None):
        """View Bot Help Menu"""
        if not command:
            await self.commandMapper(ctx)
        else:
            entity = self.bot.get_cog(command) or self.bot.get_command(command)
            if entity is None:
                return await ctx.send(
                    f":x: | **Command or category not found. Use {ctx.prefix}help**",
                    delete_after=10,
                )
            if isinstance(entity, commands.Command):
                await pagenator.SimplePaginator(
                    title=f"Command: {entity.name}",
                    entries=[
                        f"**:bulb: Command Help**\n```ini\n[{entity.help}]```",
                        f"**:video_game: Command Signature**\n```ini\n{entity.signature}```",
                    ],
                    length=1,
                    colour=random.randint(0x000000, 0xFFFFFF),
                ).paginate(ctx)
            else:
                await self.cogMapper(ctx, entity, command)


def setup(bot):
    bot.add_cog(_help(bot))
