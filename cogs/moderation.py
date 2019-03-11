import traceback
import sys
from discord.ext import commands
import discord
import asyncio


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member):
        await ctx.send(f"<@{user.id}> you will be kicked in 15 seconds. Any last words?")
        await asyncio.sleep(15)
        await bot.kick(user)
        await ctx.send(f"{ctx.message.author} kicked {user}. See ya later!")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member):
        await ctx.send(f"<@{user.id}> you will be banned in 15 seconds. Any last words?")
        await asyncio.sleep(15)
        await bot.ban(user)
        await ctx.send(f"{ctx.message.author} banned {user}, never to be seen again!")
    
    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, aliases=["delete","clean","clear"])
    async def delet(self, ctx, amount=99):
        if ctx.message.author.bot:
            return
        channel = ctx.message.channel
        messages = []
        async for message in bot.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await bot.delete_messages(messages)
        await ctx.send("Yup, deleted a whopping **{}** messages for ya!".format(amount))

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def prune(self, ctx, time=30):
        if ctx.message.author.bot:
            return
        y = "\U0001F1FE"
        n = "\U0001F1F3"
        est = await bot.estimate_pruned_members(server=ctx.message.server, days=30)
        est_msg = await ctx.send("This will get rid of an estimated **{}** people. Are you sure you want to prune?\nY for yes / N for no".format(est))
        await bot.add_reaction(est_msg, y) # emoji Y
        await bot.add_reaction(est_msg, n) # emoji N
        react = await bot.wait_for_reaction(emoji=[y,n], user=ctx.message.author, timeout=30)
        if react.reaction.emoji == y:
            number = await bot.prune_members(server=ctx.message.server, days=time)
            await ctx.send("That should have gotten rid of **{}** inactive users. Check any log channels and contact Chippy#7628 if something went wrong.".format(number))
        elif react.reaction.emoji == n:
            await ctx.send("Operation cancelled.")
            return
        else:
            ctx.send("something went wrong")

def setup(bot):
    bot.add_cog(moderation(bot))
