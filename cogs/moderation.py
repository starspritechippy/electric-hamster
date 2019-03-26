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
    async def kick(self, ctx, user: discord.Member, *, reason: str):
        await ctx.send(f"{user.mention} you will be kicked in 15 seconds. Any last words?")
        await asyncio.sleep(15)
        await user.send(f"You've been kicked from {ctx.guild.name}. Reason: {reason}")
        await user.kick()
        await ctx.send(f"{ctx.message.author} kicked {user}. See ya later!")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member):
        await ctx.send(f"{user.mention} you will be banned in 15 seconds. Any last words?")
        await asyncio.sleep(15)
        await user.send(f"You've been banned from {ctx.guild.name}. Reason: {reason}")
        await user.ban()
        await ctx.send(f"{ctx.message.author} banned {user}, never to be seen again!")
    
    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, aliases=["delete","clean","clear"])
    async def delet(self, ctx, amount=20):
        if ctx.message.author.bot:
            return
        if amount <= 0 or amount >= 100:
            await ctx.send("cannot delete less than 0 or more than 100 messages", delete_after=4)
            return
        try:     
            await ctx.purge(limit=amount)
        except:
            await ctx.send(f"`{amount}` isn't a number", delete_after=4)
            return
        await ctx.send("Yup, deleted a whopping **{}** messages for ya!".format(amount))

    @commands.has_permissions(kick_members=True)
    @commands.group(pass_context=True, invoke_without_command=True)
    async def prune(self, ctx):
        if ctx.message.author.bot:
            return
        guild = ctx.guild
        est = await guild.estimate_pruned_members(days=30)
        est_msg = await ctx.send(f"This will get rid of an estimated **{est}** people. Are you sure you want to prune?\ntype `.prune confirm` to confirm.")
        
    @commands.has_permissions(kick_members=True)    
    @prune.command(pass_context=True)
    async def confirm(self, ctx):
        number = await guild.prune_members(days=30)
        await ctx.send(f"That should have gotten rid of **{number}** inactive users. Check the audit log and contact Chippy#7628 or Paws#0001 if something went wrong.")


def setup(bot):
    bot.add_cog(moderation(bot))
