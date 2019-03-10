import traceback
import sys
from discord.ext import commands
import discord
import asyncio


class _help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(ctx, page=1):
        page_one = discord.Embed(description=f"Hey, I'm electric Hamster!", color=0xFFFFFF)
        page_one.add_field(name="Page 2 - Meta commands:",      value=".changelog\n.server\n.invite\n.ping", inline=True)
        page_one.add_field(name="Page 3 - Regular commands:",   value=".poll\n.embed", inline=True)
        page_one.add_field(name="Page 4 - Fun commands:",       value=".dice\n.rps\n.repeat", inline=True)
        page_one.add_field(name="Page 5 - Modertion commands:", value=".kick\n.ban\n.prune\n.delete", inline=True)
        page_one.set_footer(text="You're on page 1")

        page_two = discord.Embed(title="", description="__Meta commands__", color=0x000000)                   
        page_two.add_field(name=".changelog", value="Shows the most recent changes to the bot.\nUsage: `.changelog`", inline=False)
        page_two.add_field(name=".server",    value="Invites you to my support/testing server.\nUsage: `.server`\nAliases: `support`", inline=False)
        page_two.add_field(name=".invite",    value="Gives you a link to invite me to your own server.\nUsage: `.invite`", inline=False)
        page_two.add_field(name=".ping",      value="", inline=False)
        page_two.set_footer(text="You're on page 2")

        page_three = discord.Embed(title="", description="__Regular commands__", color=0x000000)
        page_three.add_field(name=".embed", value='Allows you to create a rich embed that displays your message more beautifully.\nUsage: `.embed "title" "description"` (the quotation marks are necessary)', inline=False)
        page_three.add_field(name=".poll",  value="Creates a rich embed with the option to vote *yes, no* or *undecided*.\nUsage: `.poll \"title\" \"description\"` (the quotation marks are necessary)", inline=False)
        page_three.set_footer(text="You're on page 3")

        page_four = discord.Embed(title="", description="__Fun commands__", color=0x000000)
        page_four.add_field(name=".dice",   value="Roll a dice!\nUsage: `.dice [sides=6]`, so `.dice 12` rolls a twelve-sided dice.\nAliases: `die / roll`", inline=False)
        page_four.add_field(name=".rps",    value="Play a round of rock-paper-scissors against me :smile:\nUsage:`.rps`\nAliases: `rockpaperscissors / psr / paperscissorsrock`", inline=False)
        page_four.add_field(name=".repeat", value="Repeats something you want the bot to say. Can be used for epic bamboozles.\nUsage: `.repeat any text`\nAliases: `echo / say`", inline=False)
        page_four.set_footer(text="You're on page 4")

        page_five = discord.Embed(title="these can only be used with certain permissions", description="__Moderation commands__", color=0x000000)
        page_five.add_field(name=".kick",   value="Kicks the specified user from the server\nUsage: `.kick @user`\nPermissions needed: `kick_members`", inline=False)
        page_five.add_field(name=".ban",    value="Bans the specified user from the server\nUsage: `.ban @user`\nPermissions needed: `ban_members`", inline=False)
        page_five.add_field(name=".prune",  value="Prunes inactive members from the server. [What is pruning?](https://support.discordapp.com/hc/en-us/articles/213507137-What-is-Pruning-How-do-I-use-it-)\nUsage: `.prune [days=30]`\n`days` is the amount of days a user has to be inactive to get pruned.\nPermission needed: `kick_members`", inline=False)
        page_five.add_field(name=".delete", value="Deletes the last messages from the active channel.\nUsage: `.delete [amount=99]`\nYou can't delete more that 100 or less than 2 messages.\nPermissions needed: `manage_messages`", inline=False)
        page_five.set_footer(text="You're on page 5")

        if page == 1:
            helping = page_one
        elif page == 2:
            helping = page_two
        elif page == 3:
            helping = page_three
        elif page == 4:
            helping = page_four
        elif page == 5:
            helping = page_five

        m = await bot.say(ctx.message.channel, embed=helping)

        check = 1==1
        while check == True:
            await bot.add_reaction(message=m, emoji="1⃣")
            await bot.add_reaction(message=m, emoji="2⃣")
            await bot.add_reaction(message=m, emoji="3⃣")
            await bot.add_reaction(message=m, emoji="4⃣")
            await bot.add_reaction(message=m, emoji="5⃣")
                           
            react = await bot.wait_for_reaction(emoji=["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"], user=ctx.message.author, timeout=20, message=m)
            if "{0.reaction.emoji}".format(react) == "1⃣":
                await bot.delete_message(m)
                m = await bot.say(embed=page_one)
            elif "{0.reaction.emoji}".format(react) == "2⃣":
                await bot.delete_message(m)
                m = await bot.say(embed=page_two)
            elif "{0.reaction.emoji}".format(react) == "3⃣":
                await bot.delete_message(m)
                m = await bot.say(embed=page_three)
            elif "{0.reaction.emoji}".format(react) == "4⃣":
                await bot.delete_message(m)
                m = await bot.say(embed=page_four)
            elif "{0.reaction.emoji}".format(react) == "5⃣":
                await bot.delete_message(m)
                m = await bot.say(embed=page_five)
            else:
                pass

def setup(bot):
    bot.add_cog(_help(bot))
        
