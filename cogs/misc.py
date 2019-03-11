import io
import csv
import textwrap
import traceback
import discord
import time
import asyncio
import random
from contextlib import redirect_stdout

from discord.ext import commands


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def afk(self, ctx, *, message: str):
        query = "INSERT INTO afk VALUES ($1, $2);"
        await self.bot.db.execute(query, ctx.author.id, message)
        await ctx.send("Set you as AFK! I'll notify users who ping you.")


    @commands.command(aliases=["server"])
    async def support(self, ctx):
        await ctx.send(
            "Want to join Hamster HQ, our testing server? Here's the link, feel free to join!\n\n<https://discord.gg/JE6Mk3r>"
        )


    @commands.command()
    async def invite(self, ctx):
        await ctx.send(
            "Oh? You think I'm ready to visit more servers? Wow, I appreciate that. Here's the link to invite me:\n\n__https://discordapp.com/api/oauth2/authorize?client_id=513356728365088791&permissions=201648198&scope=bot__"
        )


    ###ping###
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Pinging...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(
            content="Pong! That's a krisp {:.2f}ms of latency.".format(duration)
        )


    ###changelog command###
    @commands.command(pass_context=True, aliases=["cl"])
    async def changelog(self, ctx):
        if ctx.message.author.bot:
            return
        clembed = discord.Embed(
            title="Beta 0.38",
            description="I now have a filled up `help` command that finally includes every command!",
            color=0xFFFFFF,
        )
        cl = await ctx.send(embed=clembed)
        await ctx.message.delete()


    ###repeat###
    @commands.command(pass_context=True, aliases=["echo", "say"])
    async def repeat(self, ctx):
        if ctx.message.author.bot:
            return
        args = ctx.message.content.split(" ")
        await ctx.send("%s" % (" ".join(args[1:])))
        await ctx.message.delete()


    ###feedback###
    @commands.command(pass_context=True, aliases=["request"])
    async def feedback(self, ctx):
        if ctx.message.author.bot:
            return
        dm = bot.get_channel("548151074369044488")
        args = ctx.message.content.split(" ")
        feedback_embed = discord.Embed(title="New feedback/request!", color=0x00FFFF)
        feedback_embed.add_field(
            name="{}#{} requested the following in channel #{}:".format(
                ctx.message.author.name,
                ctx.message.author.discriminator,
                ctx.message.channel.name,
            ),
            value=" ".join(args[1:]),
            inline=False,
        )
        await bot.send_message(
            destination=dm,
            content="<@262133866062413825> / <#{}>".format(ctx.message.channel.id),
            embed=feedback_embed,
        )
        await bot.send_message(
            ctx.message.channel,
            "feedback/request was sent, my creator will take a look at it ASAP.",
        )


    ###embed###
    @commands.command(pass_context=True)
    async def embed(self, ctx, title=None, description=None):
        if ctx.message.author.bot:
            return
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(
            text="embed by {}".format(ctx.message.author),
            icon_url=ctx.message.author.avatar_url,
        )
        fail = discord.Embed(
            title="This is a title", description="This is a description", color=0xFF0000
        )
        if title == None or description == None:
            await ctx.message.delete()
            await ctx.send(
                'intended format is `.embed "This is a title" "This is a description"`'
            )
            await ctx.send(embed=fail)
        else:
            await ctx.message.delete()
            await ctx.send(embed=embed)


    ###poll###
    @commands.command(pass_context=True)
    async def poll(self, ctx, title=None, description=None):
        if ctx.message.author.bot:
            return
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(
            text="Poll by {}".format(ctx.message.author),
            icon_url=ctx.message.author.avatar_url,
        )
        fail = discord.Embed(
            title="This is the poll's title",
            description="This is the poll's description",
            color=0xFF0000,
        )
        if title == None and description == None:
            await ctx.send(
                'intended format is `.poll "This is the poll\'s title" "This is the poll\'s description"`'
            )
            fail.add_field(
                name="votes",
                value=":+1: for **yes**\n:-1: for **no**\n:v: for **undecided**",
            )
            await ctx.message.delete()
            m = await ctx.send(embed=fail)
            await m.add_reaction("\U0001F44D")
            await m.add_reaction("\U0001F44E")
            await m.add_reaction("\U0000270C")  # \U0000270C
        else:
            embed.add_field(
                name="votes",
                value=":+1: for **yes**\n:-1: for **no**\n:v: for **undecided**",
            )
            await ctx.message.delete()
            m = await ctx.send(embed=embed)
            await m.add_reaction("\U0001F44D")  # \U000023ed
            await m.add_reaction("\U0001F44E")  # \U0000270C
            await m.add_reaction("\U0000270C")  # \U0000270C


    ###dice roll###
    @commands.command(aliases=["die", "roll"])
    async def dice(self, ctx, n=6):
        if ctx.message.author.bot:
            return
        number = random.randint(0, n)
        m = await ctx.send("rolling...")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await ctx.send("Your {}-sided die rolled a **{}**!".format(n, number))


    ###furry cmd###
    @commands.command(pass_context=True)
    async def fursona(self, ctx):
        if ctx.message.author.bot:
            return
        fur = discord.Embed(
            title="meet Mica!",
            description="Mica is a male Avian, originally from Starbound. Mica has been Chippy's fursona for about a month now",
            color=0xFFFFFF,
        )
        fur.add_field(name="Origin", value="Starbound character creation", inline=True)
        fur.add_field(
            name="Personality",
            value="Mica is always friendly and tries to make everyone happy.\nWhile not obvious from the outside, Mica is very self-concious about his appearence and what people might think of him and that he feels more like a she.",
        )
        fur.set_image(
            url="https://cdn.discordapp.com/attachments/546674018577678363/550778991569666108/Mica.png"
        )
        await ctx.send(embed=fur)


    @commands.command(hidden=True, name="..")
    async def _dot(self, ctx):
        return


def setup(bot):
    bot.add_cog(misc(bot))
