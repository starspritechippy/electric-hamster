import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import random
import io
import inspect
import textwrap
import copy
from typing import Union
from contextlib import redirect_stdout
import traceback

startup_extensions = ["cogs.eval", "cogs.error", "cogs._help", "cogs.moderation"]

TOKEN = "[...]"

Client = discord.Client()
bot = commands.Bot(command_prefix = [".","What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo."])
status_info = ["Use me to make embeds!", "See `.help`!","Made by Chippy#7628",]

async def change_status():
    await bot.wait_until_ready()
    await bot.change_presence(game=discord.Game(name=".help"), status=discord.Status.idle)



@bot.event
async def on_ready():
    print("logged in as \"{}#{}\". \nIn case you need it, my ID is {}".format(bot.user.name, bot.user.discriminator, bot.user.id))

bot.remove_command("help")
bot.afk = []
bot.afk_msg = []

@bot.command(pass_context=True)
async def load(ctx,extension_name : str):
    """Loads an extension."""
    if ctx.message.author.bot:
        return
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("cog **{}** successfully loaded.".format(extension_name))

@bot.command(pass_context=True)
async def unload(ctx,extension_name : str):
    """Unloads an extension."""
    if ctx.message.author.bot:
        return
    bot.unload_extension(extension_name)
    await bot.say("cog **{}** successfully unloaded.".format(extension_name))

###help###
@bot.command(pass_context=True)
async def help(ctx, page=1):
    page_one = discord.Embed(description="Hey, I'm electric Hamster!", color=0xFFFFFF)
    page_one.add_field(name="Page 2 - Meta commands:",      value=".changelog\n.server\n.invite\n.ping", inline=True)
    page_one.add_field(name="Page 3 - Regular commands:",   value=".poll\n.embed", inline=True)
    page_one.add_field(name="Page 4 - Fun commands:",       value=".dice\n.rps\n.repeat", inline=True)
    page_one.add_field(name="Page 5 - Modertion commands:", value=".kick\n.ban\n.prune\n.delete", inline=True)
    page_one.set_footer(text="You're on page 1")

    page_two = discord.Embed(title="", description="__Meta commands__", color=0x000000)                   
    page_two.add_field(name=".changelog", value="Shows the most recent changes to the bot.\nUsage: `.changelog`", inline=False)
    page_two.add_field(name=".server",    value="Invites you to my support/testing server.\nUsage: `.server`\nAliases: `support`", inline=False)
    page_two.add_field(name=".invite",    value="Gives you a link to invite me to your own server.\nUsage: `.invite`", inline=False)
    page_two.add_field(name=".ping",      value="Checks the current ping!\nUsage: `.ping`", inline=False)
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

    m = await bot.send_message(ctx.message.channel, embed=page_one)

    await bot.add_reaction(message=m, emoji="1⃣")
    await bot.add_reaction(message=m, emoji="2⃣")
    await bot.add_reaction(message=m, emoji="3⃣")
    await bot.add_reaction(message=m, emoji="4⃣")
    await bot.add_reaction(message=m, emoji="5⃣")

    for x in range(0, 300):                       
        react = await bot.wait_for_reaction(emoji=["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"], user=ctx.message.author, timeout=20, message=m)
        if "{0.reaction.emoji}".format(react) == "1⃣":
            await bot.edit_message(m, embed=page_one)
        elif "{0.reaction.emoji}".format(react) == "2⃣":
            await bot.edit_message(m, embed=page_two)
        elif "{0.reaction.emoji}".format(react) == "3⃣":
            await bot.edit_message(m, embed=page_three)
        elif "{0.reaction.emoji}".format(react) == "4⃣":
            await bot.edit_message(m, embed=page_four)
        elif "{0.reaction.emoji}".format(react) == "5⃣":
            await bot.edit_message(m, embed=page_five)
        else:
            pass

@bot.command(pass_context=True)
async def afk(ctx, *, message):
    bot.afk.append(ctx.message.author)
    bot.afk_msg.append(message)
    await bot.say("Set you as AFK! I'll notify users who ping you.")

@bot.event
async def on_message(message):
    for user in bot.afk:
        if user.mentioned_in(message):
            index = bot.afk.index(user)
            await bot.send_message(message.channel, f"{user} isn't available: {bot.afk_msg[index]}")
        if user == message.author:
            index = bot.afk.index(user)
            bot.afk.pop(index)
            bot.afk_msg.pop(index)
            await bot.send_message(message.channel, "You're no longer set as AFK!")
    await bot.process_commands(message)

@bot.command(aliases=["server"])
async def support():
    await bot.say("Want to join Hamster HQ, our testing server? Here's the link, feel free to join!\n\n<https://discord.gg/JE6Mk3r>")

@bot.command()
async def invite():
    await bot.say("Oh? You think I'm ready to visit more servers? Wow, I appreciate that. Here's the link to invite me:\n\n__https://discordapp.com/api/oauth2/authorize?client_id=513356728365088791&permissions=201648198&scope=bot__")

###ping###
@bot.command(pass_context=True)
async def ping(ctx):
    start = time.perf_counter()
    message = await bot.say('Pinging...')
    end = time.perf_counter()
    duration = (end - start) * 1000
    await bot.edit_message(message, 'Pong! That\'s a krisp {:.2f}ms of latency.'.format(duration))

###changelog command###
@bot.command(pass_context=True, aliases=["cl"])
async def changelog(ctx):
    if ctx.message.author.bot:
        return
    clembed = discord.Embed(title="Beta 0.38", description="I now have a filled up `help` command that finally includes every command!", color=0xffffff)
    cl = await bot.say(embed=clembed)
    await bot.delete_message(ctx.message)

###repeat###
@bot.command(pass_context=True, aliases=["echo", "say"])
async def repeat(ctx):
    if ctx.message.author.bot:
        return
    args = ctx.message.content.split(" ")
    await bot.say("%s" % (" ".join(args[1:])))
    await bot.delete_message(ctx.message)

###feedback###
@bot.command(pass_context=True, aliases=["request"])
async def feedback(ctx):
    if ctx.message.author.bot:
        return
    dm = bot.get_channel("548151074369044488")
    args = ctx.message.content.split(" ")
    feedback_embed = discord.Embed(title="New feedback/request!", color=0x00ffff)
    feedback_embed.add_field(
        name="{}#{} requested the following in channel #{}:".format(
            ctx.message.author.name,
            ctx.message.author.discriminator,
            ctx.message.channel.name
            ),
        value=" ".join(args[1:]), inline=False)
    await bot.send_message(destination=dm, content="<@262133866062413825> / <#{}>".format(ctx.message.channel.id), embed=feedback_embed)
    await bot.send_message(ctx.message.channel, "feedback/request was sent, my creator will take a look at it ASAP.")

###RPS###
@bot.command(pass_context=True, aliases=["rockpaperscissors", "psr", "paperscissorsrock"])
async def rps(ctx):
    if ctx.message.author.bot:
        return
    rock = "\U0000270A"
    paper = "\U0000270B"
    scissors = "\U0000270C"
    rps_emb = discord.Embed(title="Your Choice!", description=":fist: / :raised_hand: / :v:\nRock, Paper, Scissors", color=0x00ff00)
    rps_msg = await bot.say(embed=rps_emb)
    bot_choice = random.choice([rock, paper, scissors])
    r = ["I won! :smile:","You won, congrats! :smile:","It's a draw!"]

    await bot.add_reaction(message=rps_msg, emoji=rock)
    await bot.add_reaction(message=rps_msg, emoji=paper)
    await bot.add_reaction(message=rps_msg, emoji=scissors)

    choice = await bot.wait_for_reaction(emoji=[rock, paper, scissors], user=ctx.message.author, timeout=20, message=rps_msg)

    await bot.say("You chose **{0.reaction.emoji}**\nI chose {1}...".format(choice, bot_choice))

    if choice.reaction.emoji == bot_choice:
        await bot.say("{}".format(r[2]))
    elif choice.reaction.emoji == rock and bot_choice == paper:
        await bot.say("{}".format(r[0]))
    elif choice.reaction.emoji == rock and bot_choice == scissors:
        await bot.say("{}".format(r[1]))
    elif choice.reaction.emoji == paper and bot_choice == rock:
        await bot.say("{}".format(r[1]))
    elif choice.reaction.emoji == paper and bot_choice == scissors:
        await bot.say("{}".format(r[0]))
    elif choice.reaction.emoji == scissors and bot_choice == paper:
        await bot.say("{}".format(r[1]))
    elif choice.reaction.emoji == scissors and bot_choice == rock:
        await bot.say("{}".format(r[0]))
    else:
        await bot.say("Something must've gone wrong in my code...")
        print("User's choice: {}".format(choice.reaction.emoji))
        print("Bot's  choice: {}".format(bot_choice))

###embed###
@bot.command(pass_context=True)
async def embed(ctx, title=None, description=None):
    if ctx.message.author.bot:
        return
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text="embed by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    fail = discord.Embed(title="This is a title", description="This is a description", color=0xff0000)
    if title == None or description == None:
        await bot.delete_message(ctx.message)
        await bot.say('intended format is `.embed "This is a title" "This is a description"`')
        await bot.say(embed=fail)
    else:
        await bot.delete_message(ctx.message)
        await bot.say(embed=embed)

###poll###
@bot.command(pass_context=True)
async def poll(ctx, title=None, description=None):
    if ctx.message.author.bot:
        return
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text="Poll by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
    fail = discord.Embed(title="This is the poll\'s title", description="This is the poll\'s description", color=0xff0000)
    if title == None and description == None:
        await bot.say('intended format is `.poll "This is the poll\'s title" "This is the poll\'s description"`')
        fail.add_field(name="votes", value=":+1: for **yes**\n:-1: for **no**\n:v: for **undecided**")
        await bot.delete_message(ctx.message)
        m = await bot.say(embed=fail)
        await bot.add_reaction(message=m, emoji="\U0001F44D")
        await bot.add_reaction(message=m, emoji="\U0001F44E")
        await bot.add_reaction(message=m, emoji="\U0000270C") #\U0000270C
    else:
        embed.add_field(name="votes", value=":+1: for **yes**\n:-1: for **no**\n:v: for **undecided**")
        await bot.delete_message(ctx.message)
        m = await bot.say(embed=embed)
        await bot.add_reaction(message=m, emoji="\U0001F44D") #\U000023ed
        await bot.add_reaction(message=m, emoji="\U0001F44E") #\U0000270C
        await bot.add_reaction(message=m, emoji="\U0000270C") #\U0000270C

###dice roll###
@bot.command(aliases=["die", "roll"])
async def dice(n=6):
    if ctx.message.author.bot:
        return
    number = random.randint(0,n)
    m = await bot.say("rolling...")
    await asyncio.sleep(3)
    await bot.delete_message(m)
    await bot.say("Your {}-sided die rolled a **{}**!".format(n, number))

###furry cmd###
@bot.command(pass_context=True)
async def fursona(ctx):
    if ctx.message.author.bot:
        return
    fur = discord.Embed(title="meet Mica!", description="Mica is a male Avian, originally from Starbound. Mica has been Chippy's fursona for about a month now", color=0xffffff)
    fur.add_field(name="Origin", value="Starbound character creation", inline=True)
    fur.add_field(name="Personality", value="Mica is always friendly and tries to make everyone happy.\nWhile not obvious from the outside, Mica is very self-concious about his appearence and what people might think of him and that he feels more like a she.")
    fur.set_image(url="https://cdn.discordapp.com/attachments/546674018577678363/550778991569666108/Mica.png")
    await bot.say(embed=fur)

@bot.command(hidden=True, name="..")
async def _dot():
    return

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')
            
    bot.run(TOKEN)
