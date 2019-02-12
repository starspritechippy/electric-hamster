import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import random
#import cycle

TOKEN = "NTEzMzU2NzI4MzY1MDg4Nzkx.D0CeLQ.NqaOS6PDTVtNrSgI-ONGqwQttM4"

Client = discord.Client()
bot = commands.Bot(command_prefix = ".")
status_info = ["Use me to make embeds!", "See `.help`!","Made by Chippy#7628",]

async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status_info)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status), status=discord.Status.idle)
        await asyncio.sleep(15)


@bot.event
async def on_ready():
    print("I'm ready")

bot.remove_command("help")

@bot.command(pass_context=True, aliases=["cl"])
async def changelog(ctx):
    clembed = discord.Embed(title="New version: beta 0.27", description="-messages containing insults toward other people (or bots), for example `fuck you` will now be punished severely", color=0xffffff)
    cl = await bot.say(embed=clembed)
    await bot.delete_message(ctx.message)

@bot.event
async def on_message(msg):
    echo = msg.content.split(" ")
    chippy = 262133866062413825
    if msg.content.startswith(("fuck you", "screw you", "bad bot", "frick you", "heck you", "shitty bot", "piece of shit")):
        await bot.send_message(msg.channel, "no u")
        
    #elif msg.content.upper.startswith(".SUGGEST"):
    #    await bot.send_message(chippy, "**{} suggested:**\n{}".format(message.author.name, "%s" % (" ".join(echo[1:]))))
    #    await bot.send_message(msg.channel, "sent")
    else:
        pass
    await bot.process_commands(msg)



@bot.command(pass_context=True, aliases=["rockpaperscissors", "psr", "paperscissorsrock"])
async def rps(ctx):
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


@bot.command(pass_context=True)
async def embed(ctx, title=None, description=None):
    embed = discord.Embed(title=title, description=description)
    fail = discord.Embed(title="This is a title", description="This is a description", color=0xff0000)
    if title == None and description == None:
        await bot.delete_message(ctx.message)
        await bot.say('intended format is `.embed "This is a title" "This is a description"`')
        await bot.say(embed=fail)
    else:
        await bot.delete_message(ctx.message)
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def poll(ctx, title=None, description=None):
    embed = discord.Embed(title=title, description=description)
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

@bot.command(aliases=["die", "roll"])
async def dice(n=6):
    number = random.randint(0,n)
    m = await bot.say("rolling...")
    await asyncio.sleep(3)
    await bot.delete_message(m)
    await bot.say("Your {}-sided die rolled a **{}**!".format(n, number))
        

@bot.command()
async def help():
    helping = discord.Embed(title="Hey, I'm an embed-making bot!", color=0xFFFFFF)
    helping.add_field(name="poll", value="create a custom poll embed, complete with reaction-votes\n`.poll \"title\" \"description\"`", inline=False)
    helping.add_field(name="embed", value="create a custom embed\n`.embed \"title\" \"description\"`", inline=False)
    helping.add_field(name="changelog", value="see the current version of me and see a list of wwhats new\n`.changelog`", inline=False)
    helping.add_field(name="dice", value="roll an n-sided dice!\n`.[dice|die|roll] [sides=6]`", inline=False)
    
    await bot.say(embed=helping)
    

bot.run(TOKEN)

#embed = discord.Embed(title="Title", description="desc", color=0xhexcol)
            #embed.add_field(name="Another field", value="text", inline=False)
            #embed.add_field(name="more field", value='lmao', inline=False)
            #await bot.say(embed=embed)



#else return
