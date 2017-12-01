import discord
import asyncio
import random
from random import randint
import time
import datetime
import pickle
import glob, os, io, sys
import requests
import json
from pprint import pprint
import aiohttp
from lxml import html
import sqlite3
import colorama
from colorama import init
init(autoreset = True)
from colorama import Fore, Back, Style
from discord.ext.commands import Bot
from discord.ext import commands
from credentials import Prefix as prefix
from credentials import BotToken
from credentials import Owners as owner
from credentials import EmbedColor as embed_color
from credentials import LoggingChannel as loggingchannel
from credentials import LoggingServer as logserver

###
bot_version = 'v1.2'
bot_author = 'Kyousei#8357'
bot_author_id = '145878866429345792'
###
bot_prefix= prefix
client = commands.Bot(command_prefix=bot_prefix)
start_time = time.time()

## DATABASE ##

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Hackbans(user_id TEXT, server_id TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Permissions(nsfw_is_enabled INT, server_id TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS UserData(user_id TEXT, user_name TEXT, level TEXT, exp TEXT, description TEXT, reputation TEXT, currency TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Bounties(user TEXT, username TEXT, reward TEXT)')

create_table()

## DATABASE ##
@client.event
async def on_ready():
    print("Logging In...")
    time.sleep(2)
    print("Checking files..")
    if not os.path.isfile("credentials.py"):
        print(Back.RED + "credentials.py not found! Please add it then try again!")
        await client.logout()
    elif not os.path.isfile("data/images/coin/heads.png"):
        print(Back.RED + "heads.png not found! Please add it then try again!")
        await client.logout()
    elif not os.path.isfile("data/images/coin/tails.png"):
        await client.logout()
        print(Back.RED + "tails.png not found! Please add it then try again!")
        await client.logout()
    time.sleep(2)
    print("Logged In | Client Credentials")
    print("\n       Client Name: {}".format(client.user.name) +"\n       Client ID: {}".format(client.user.id) + "\n       Prefix: {}".format(prefix) + "\n       Embed Color: {}".format(embed_color) + "\n       Version: {}".format(bot_version) + "\n       Owner ID: {}".format(owner))
    await client.change_presence(game=discord.Game(name=''))

startup_extensions = ["data.Modules.Bounty.Bounties", "data.Modules.XP.EXP", "data.Modules.XP.GiXP", "data.Modules.XP.NewEXPStats", "data.Modules.Permissions.Permissions"]

for cog in startup_extensions:
	try:
		client.load_extension(cog)
	except Exception as error:
		print(str(error))
    

@client.command(pass_context = True, no_pm = True)
async def send(ctx, member : discord.Member, *, message):
        if ctx.message.author.server_permissions.ban_members:
            return await client.send_message(member, embed=discord.Embed(description="Message from **" + ctx.message.author.mention + "**: " + message, color = embed_color))
            print("Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
        else:
            return await client.say(":x: Insufficient permissions!")
            print("Command Failed To |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\nReason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Ban Members permission!")

@client.command(pass_context = True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong:  The ping time is `%dms`" % ping)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True)
async def invite(ctx):
    embed = discord.Embed(title = "Here are invite links:", description = "Invite me to your server with this link: https://discordapp.com/oauth2/authorize?client_id=331766751765331969&scope=bot&permissions=66186303", color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = True)
async def banlist(ctx):
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of Banned Members", description = x, color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context=True, no_pm = True)
async def connect(ctx):
    if client.is_voice_connected(ctx.message.server):
        return await client.say("I am already connected to a voice channel. Do not disconnect me if I am in use!")
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = True)
async def disconnect(ctx):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()
            print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

@client.command(pass_context=True, no_pm = True, aliases=['prune', 'purge'])
async def clear(ctx, number):
    embed = discord.Embed(description = ":x: Insufficient permissions! You require **Manage Messages** permission in order to clear messages!", color = 0xF00000)
    if not ctx.message.author.server_permissions.manage_messages:
        return await client.say(embed = embed)
        print(Fore.CYAN + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW  + "Insufficient Permissions! Both user and bot need Manage Messages permission!")
    mgs = []
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = True)
async def author(ctx):
    embed = discord.Embed(title = "Yotsugi Bot Author:", description = "Name: **" + bot_author + "**  \nJoined Discord: **07.02.2016  1:10 PM**  \n  **ID**: 145878866429345792  \n**Email**: yotsugibot@gmail.com  \nSay **;h** for commands.", color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = True, aliases=['b'])
async def ban(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.ban_members:
        return

    if not member:
        embed = discord.Embed(description = ctx.message.author.mention + ", you did not specify a user to ban! :x:", color = 0xF00000)
        return await client.say(embed = embed)
    try:
        await client.ban(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            embed = discord.Embed(description = "Privilege is too low. :x:", color = 0xF00000)
            return await client.say(embed = embed)
            print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Ban Members permission!")

    embed = discord.Embed(description = "**%s** has been banned."%member.name, color = 0xF00000)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")



@client.command(pass_context = True, no_pm = True, aliases=['k'])
async def kick(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.kick_members:
        return

    if not member:
        return await client.say(ctx.message.author.mention + "Specify a user to kick!")
    try:
        await client.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            embed = discord.Embed(description = "Privilege is too low. :x:", color = 0xF00000)
            return await client.say(embed = embed)
            print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Inusfficient Permissions! Both user and bot need Kick Members permission!")

    embed = discord.Embed(description = "**%s** has been kicked."%member.name, color = 0xF00000)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = True)
async def mute(ctx, *, member : discord.Member):
    if not ctx.message.author.server_permissions.mute_members:
        return print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and member need Mute Members permission!")
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been muted!"%member.mention)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, description='Unmutes the muted members.', no_pm = True)
async def unmute(ctx, *, member : discord.Member):
    if not ctx.message.author.server_permissions.mute_members:
        return print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Mute Members permission!")
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been unmuted!"%member.mention)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


answers = ["My source say no.", "I completely disagree.", "No way in hell!", "Sure! :D", "Why not?", "Why would you say that?", "When life gives you lemons, throw them at people!", "HA, You wish!", "Keep dreaming!", "Does a green light mean go?", "Red is supposed to stop you, but your magic is TOO strong! :sweat:", "Power outage!??! WHAT ABOUT MY WIFI!??!!", "Hmmm.. this is hard", "lol, just lol.", "Cleverbot is no match for me! Haahahaha", "The chances of that happening are equal to the chances of shivaco getting a girlfriend. Null!", "There's an admin watching :scream:", "Ask me tomorrow :zzz:", "No... I mean yes... Well... Ask again later"]

@client.command(description='Decides for you.', aliases=['8ball'])
async def eightball(*choices):
    if len(choices) == 0:
        return await client.say("Ask me a yes or no question.")
    embed = discord.Embed(description = random.choice(answers), color = embed_color)
    await client.say(embed = embed)


@client.command(pass_context = True)
async def now(ctx):
    date = datetime.datetime.now().strftime("**Date: **%A, %B %d, %Y\n**Time: **%I:%M %p")
    embed = discord.Embed(color = embed_color)
    embed.add_field(name="Bot's System Date & Time", value=date, inline=False)
    await client.say(embed=embed)



@client.command()
async def roll(dice : str):
    """--- Rolled with NdN format. Example: 5d3"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        embed = discord.Embed(description = ":x: Format has to be in NdN! (**Example:** `;roll 5d50`)", color = 0xFF0000)
        await client.say(embed = embed)
        return
    if (rolls > 100) or (limit > 100):
        embed = discord.Embed(description = ":x: You can't roll more than 100!", color = 0xFF0000)
        await client.say(embed = embed)
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    embed = discord.Embed(description = result, color = embed_color)
    await client.say(embed = embed)



@client.command(pass_context = True)
async def github(ctx):
    """  ---Link to Github"""
    embed = discord.Embed(description = "Yotsugi Github can be found here: https://github.com/YotsugiBot", color = embed_color)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True)
async def license(ctx):
	embed = discord.Embed(description = "Read the License [here](https://github.com/Kyousei/YotsugiBot/blob/master/LICENSE.md)", color = embed_color)
	await client.say(embed = embed)
	print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")



@client.command(pass_context = True)
async def servers(ctx):
    x = ', '.join([str(server) for server in client.servers])
    y = len(client.servers)
    print(x)
    if y > 40:
        embed = discord.Embed(title = "Servers: " + str(y), description = "```json\nRetracted because there's more than 40 servers!```", color = 0xFFFFF)
        return await client.say(embed = embed)
    elif y < 40:
        embed = discord.Embed(title = "Servers: " + str(y), description = "```json\n" + x + "```", color = 0xFFFFF)
        return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, no_pm = False)
async def stats(ctx):
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    embed = discord.Embed(title = "Yotsugi **" + bot_version + "**", color = embed_color)
    embed.add_field(name='Author', value=bot_author, inline=True)
    embed.add_field(name='Uptime', value="**%d** weeks, \n**%d** days, \n**%d** hours, \n**%d** minutes, \n**%d** seconds"% (week, day, hour, minute, second), inline=True)
    embed.add_field(name='Owner IDs', value=owner, inline=True)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context=True, no_pm=True, aliases=['die'])
async def shutdown(ctx):
    if owner == ctx.message.author.id:
        embed = discord.Embed(description = "Shutting Down...", color = embed_color)
        await client.say(embed = embed)
        print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran: " + prefix + "\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
        await client.logout()


@client.command(pass_context = True, no_pm = True, aliases=['serid'])
async def serverid(ctx, *, member = discord.Member):
    embed = discord.Embed(description = ctx.message.author.mention + ", ID of this server is:** " + ctx.message.channel.server.id + "**", color = embed_color)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

@client.command(pass_context = True, no_pm = True, aliases=['chnlid'])
async def channelid(ctx):
    embed = discord.Embed(description = ctx.message.author.mention + ", ID of this channel is:** " + ctx.message.channel.id + "**", color = embed_color)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context=True, no_pm=True, aliases=['remrl'])
async def removerole(ctx, user: discord.Member, *, role):
    if ctx.message.author.server_permissions.manage_roles:
        await client.remove_roles(user, discord.utils.get(ctx.message.server.roles, name=role))
        embed = discord.Embed(description = ("Removed %s from **%s**" % (user.mention, role)), color = embed_color)
        await client.say(embed = embed)
        print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
    else:
        embed = discord.Embed(description = ":x: Insufficient permissions!", color = 0xFF0000)
        return await client.say(embed = embed)
        print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Manage Roles permission!")


@client.command(pass_context=True, no_pm=True, aliases=['setrl'])
async def setrole(ctx, user: discord.Member, *, role):
    if ctx.message.author.server_permissions.manage_roles:
        await client.add_roles(user, discord.utils.get(ctx.message.server.roles, name=role))
        embed = discord.Embed(description = ("Added %s to  **%s** " % (user.mention, role)), color = embed_color)
        await client.say(embed = embed)
        print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
    else:
        embed = discord.Embed(description = ":x: Insufficient permissions!", color = 0xFF0000)
        return await client.say(embed = embed)
        print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Manage Roles permission!")

@client.command(pass_context = True, no_pm = True)
async def warn(ctx, member : discord.Member, *, message):
        if ctx.message.author.server_permissions.kick_members:
                embed = discord.Embed(description = "You've been warned for: **" + message + "**\nResponsible Moderator: **" + ctx.message.author.mention + "**\nServer: **" + ctx.message.server.name + "**", color = 0xFF0000)
                return await client.send_message(member, embed = embed)
        else:
                embed = discord.Embed(description = ":x: Insufficient Permissions", color = 0xFF0000)
                return await client.say(embed = embed)


@client.command()
async def ud(*msg):
    word = ' '.join(msg)
    api = "http://api.urbandictionary.com/v0/define"
    response = requests.get(api, params=[("term", word)]).json()
    embed = discord.Embed(description = "No results found!", color = 0xFF0000)
    if len(response["list"]) == 0: return await client.say(embed = embed)

    embed = discord.Embed(title = "Word", description = word, color = embed_color)
    embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
    embed.add_field(name = "Examples:", value = response['list'][0]["example"])
    embed.set_footer(text = "Tags: " + ', '.join(response['tags']))

    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")



@client.command(pass_context = True)
async def setgame(ctx, *, game : str):
        if owner != ctx.message.author.id:
            return await client.say(embed=embeds.permission_denied("You aren't the bot owner!"), color = 0xFF0000)
        else:
            try:
                await client.change_presence(game=discord.Game(name=game), status=ctx.message.server.me.status)
                logging.info("Set game to " + str(game))
                print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
            except Exception as e:
                print("Failed to set game: {}".format(str(e)) + "\nIgnore this error. It's Python who's being an ass.")
                print(Fore.RED + "Command Error Raised, But The Command Was Still Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Ignore this error!")


heads = "data/images/coin/heads.png"
tails = "data/images/coin/tails.png"
@client.command(pass_context=True, aliases=['flip'])
async def flipcoin(ctx):
    choice = random.randint(1,2)
    if choice == 1:
        await client.send_file(ctx.message.channel, heads, content=ctx.message.author.mention + ", you flipped **Heads**!", tts=False)
    if choice == 2:
        await client.send_file(ctx.message.channel, tails, content=ctx.message.author.mention + ", you flipped **Tails**!", tts=False)


@client.command()
async def h(command = None):
    global response
    response = json.load(open('responses.json'))
    embed = discord.Embed(color = embed_color)
    embed.add_field(name="Hosting Guides", value="[Click Here](https://yotsugibot.readthedocs.io/en/latest/)", inline=False)
    embed.add_field(name="Commands List", value="[Click Here](https://yotsugibot.readthedocs.io/en/latest/Commands%20List)", inline=False)
    embed.add_field(name="Website", value="[Click Here](https://yotsugi.tk)", inline=False)
    if not command:
            await client.say(embed = embed)
            return

        #some code to check if the command is an actual command (depends on how you make commands)
    if command == prefix+'b':
        embed = discord.Embed(title = response["Ban"][0]["Title"], description = response["Ban"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Ban"][0]["Usage"], value=response["Ban"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Ban"][0]["UPerms"], value=response["Ban"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Ban"][0]["BPerms"], value=response["Ban"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ban':
        embed = discord.Embed(title = response["Ban"][0]["Title"], description = response["Ban"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Ban"][0]["Usage"], value=response["Ban"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Ban"][0]["UPerms"], value=response["Ban"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Ban"][0]["BPerms"], value=response["Ban"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return


    if command == prefix+'kick':
        embed = discord.Embed(title = response["Kick"][0]["Title"], description = response["Kick"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Kick"][0]["Usage"], value=response["Kick"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Kick"][0]["UPerms"], value=response["Kick"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Kick"][0]["BPerms"], value=response["Kick"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'k':
        embed = discord.Embed(title = response["Kick"][0]["Title"], description = response["Kick"][0]["Description"], color = embed_color)
        embed.add_field(name=response[""][0]["Usage"], value=response[""][0]["Usage1"], inline=True)
        embed.add_field(name=response[""][0]["UPerms"], value=response[""][0]["UPerms1"], inline=True)
        embed.add_field(name=response[""][0]["BPerms"], value=response[""][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serverid':
        embed = discord.Embed(title = response["Server_ID"][0]["Title"], description = response["Server_ID"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Server_ID"][0]["Usage"], value=response["Server_ID"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Server_ID"][0]["UPerms"], value=response["Server_ID"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Server_ID"][0]["BPerms"], value=response["Server_ID"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serid':
        embed = discord.Embed(title = response["Server_ID"][0]["Title"], description = response["Server_ID"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Server_ID"][0]["Usage"], value=response["Server_ID"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Server_ID"][0]["UPerms"], value=response["Server_ID"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Server_ID"][0]["BPerms"], value=response["Server_ID"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ud':
        embed = discord.Embed(title = response["Ud"][0]["Title"], description = response["Ud"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Ud"][0]["Usage"], value=response["Ud"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Ud"][0]["UPerms"], value=response["Ud"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Ud"][0]["BPerms"], value=response["Ud"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'8ball':
        embed = discord.Embed(title = response["Eightball"][0]["Title"], description = response["Eightball"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Eightball"][0]["Usage"], value=response["Eightball"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Eightball"][0]["UPerms"], value=response["Eightball"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Eightball"][0]["BPerms"], value=response["Eightball"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'eightball':
        embed = discord.Embed(title = response["Eightball"][0]["Title"], description = response["Eightball"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Eightball"][0]["Usage"], value=response["Eightball"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Eightball"][0]["UPerms"], value=response["Eightball"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Eightball"][0]["BPerms"], value=response["Eightball"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return


    if command == prefix+'clear':
        embed = discord.Embed(title = response["Prune"][0]["Title"], description = response["Prune"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Prune"][0]["Usage"], value=response["Prune"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Prune"][0]["UPerms"], value=response["Prune"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Prune"][0]["BPerms"], value=response["Prune"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'prune':
        embed = discord.Embed(title = response["Prune"][0]["Title"], description = response["Prune"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Prune"][0]["Usage"], value=response["Prune"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Prune"][0]["UPerms"], value=response["Prune"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Prune"][0]["BPerms"], value=response["Prune"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'purge':
        embed = discord.Embed(title = response["Prune"][0]["Title"], description = response["Prune"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Prune"][0]["Usage"], value=response["Prune"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Prune"][0]["UPerms"], value=response["Prune"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Prune"][0]["BPerms"], value=response["Prune"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'mute':
        embed = discord.Embed(title = response["Mute"][0]["Title"], description = response["Mute"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Mute"][0]["Usage"], value=response["Mute"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Mute"][0]["UPerms"], value=response["Mute"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Mute"][0]["BPerms"], value=response["Mute"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'unmute':
        embed = discord.Embed(title = response["Unmute"][0]["Title"], description = response["Unmute"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Unmute"][0]["Usage"], value=response["Unmute"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Unmute"][0]["UPerms"], value=response["Unmute"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Unmute"][0]["BPerms"], value=response["Unmute"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'stats':
        embed = discord.Embed(title = response["Stats"][0]["Title"], description = response["Stats"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Stats"][0]["Usage"], value=response["Stats"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Stats"][0]["UPerms"], value=response["Stats"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Stats"][0]["BPerms"], value=response["Stats"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'author':
        embed = discord.Embed(title = response["Author"][0]["Title"], description = response["Author"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Author"][0]["Usage"], value=response["Author"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Author"][0]["UPerms"], value=response["Author"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Author"][0]["BPerms"], value=response["Author"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'banlist':
        embed = discord.Embed(title = response["Banlist"][0]["Title"], description = response["Banlist"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Banlist"][0]["Usage"], value=response["Banlist"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Banlist"][0]["UPerms"], value=response["Banlist"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Banlist"][0]["BPerms"], value=response["Banlist"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ping':
        embed = discord.Embed(title = response["Ping"][0]["Title"], description = response["Ping"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Ping"][0]["Usage"], value=response["Ping"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Ping"][0]["UPerms"], value=response["Ping"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Ping"][0]["BPerms"], value=response["Ping"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'channelid':
        embed = discord.Embed(title = response["Channel_ID"][0]["Title"], description = response["Channel_ID"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Channel_ID"][0]["Usage"], value=response["Channel_ID"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Channel_ID"][0]["UPerms"], value=response["Channel_ID"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Channel_ID"][0]["BPerms"], value=response["Channel_ID"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'chnlid':
        embed = discord.Embed(title = response["Channel_ID"][0]["Title"], description = response["Channel_ID"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Channel_ID"][0]["Usage"], value=response["Channel_ID"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Channel_ID"][0]["UPerms"], value=response["Channel_ID"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Channel_ID"][0]["BPerms"], value=response["Channel_ID"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'github':
        embed = discord.Embed(title = response["Github"][0]["Title"], description = response["Github"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Github"][0]["Usage"], value=response["Github"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Github"][0]["UPerms"], value=response["Github"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Github"][0]["BPerms"], value=response["Github"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'send':
        embed = discord.Embed(title = response["Send"][0]["Title"], description = response["Send"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Send"][0]["Usage"], value=response["Send"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Send"][0]["UPerms"], value=response["Send"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Send"][0]["BPerms"], value=response["Send"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'shutdown':
        embed = discord.Embed(title = response["Shutdown"][0]["Title"], description = response["Shutdown"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Shutdown"][0]["Usage"], value=response["Shutdown"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Shutdown"][0]["UPerms"], value=response["Shutdown"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Shutdown"][0]["BPerms"], value=response["Shutdown"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'die':
        embed = discord.Embed(title = response["Shutdown"][0]["Title"], description = response["Shutdown"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Shutdown"][0]["Usage"], value=response["Shutdown"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Shutdown"][0]["UPerms"], value=response["Shutdown"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Shutdown"][0]["BPerms"], value=response["Shutdown"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setrole':
        embed = discord.Embed(title = response["Set_Role"][0]["Title"], description = response["Set_Role"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Set_Role"][0]["Usage"], value=response["Set_Role"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Set_Role"][0]["UPerms"], value=response["Set_Role"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Set_Role"][0]["BPerms"], value=response["Set_Role"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setrl':
        embed = discord.Embed(title = response["Set_Role"][0]["Title"], description = response["Set_Role"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Set_Role"][0]["Usage"], value=response["Set_Role"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Set_Role"][0]["UPerms"], value=response["Set_Role"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Set_Role"][0]["BPerms"], value=response["Set_Role"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'removerole':
        embed = discord.Embed(title = response["Remove_Role"][0]["Title"], description = response["Remove_Role"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Remove_Role"][0]["Usage"], value=response["Remove_Role"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Remove_Role"][0]["UPerms"], value=response["Remove_Role"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Remove_Role"][0]["BPerms"], value=response["Remove_Role"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'remrl':
        embed = discord.Embed(title = response["Remove_Role"][0]["Title"], description = response["Remove_Role"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Remove_Role"][0]["Usage"], value=response["Remove_Role"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Remove_Role"][0]["UPerms"], value=response["Remove_Role"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Remove_Role"][0]["BPerms"], value=response["Remove_Role"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'flip':
        embed = discord.Embed(title = response["Flip"][0]["Title"], description = response["Flip"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Flip"][0]["Usage"], value=response["Flip"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Flip"][0]["UPerms"], value=response["Flip"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Flip"][0]["BPerms"], value=response["Flip"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'roll':
        embed = discord.Embed(title = response["Roll"][0]["Title"], description = response["Roll"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Roll"][0]["Usage"], value=response["Roll"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Roll"][0]["UPerms"], value=response["Roll"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Roll"][0]["BPerms"], value=response["Roll"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'servers':
        embed = discord.Embed(title = response["Servers"][0]["Title"], description = response["Servers"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Servers"][0]["Usage"], value=response["Servers"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Servers"][0]["UPerms"], value=response["Servers"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Servers"][0]["BPerms"], value=response["Servers"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'server':
        embed = discord.Embed(title = response["Server"][0]["Title"], description = response["Server"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Server"][0]["Usage"], value=response["Server"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Server"][0]["UPerms"], value=response["Server"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Server"][0]["BPerms"], value=response["Server"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'warn':
        embed = discord.Embed(title = response["Warn"][0]["Title"], description = response["Warn"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Warn"][0]["Usage"], value=response["Warn"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Warn"][0]["UPerms"], value=response["Warn"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Warn"][0]["BPerms"], value=response["Warn"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'h':
        embed = discord.Embed(title = response["Help"][0]["Title"], description = response["Help"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Help"][0]["Usage"], value=response["Help"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Help"][0]["UPerms"], value=response["Help"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Help"][0]["BPerms"], value=response["Help"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'hentai':
        embed = discord.Embed(title = response["Hentai"][0]["Title"], description = response["Hentai"][0]["Description"], color = embed_color)
        embed.add_field(name='Usage', value=response["Hentai"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Hentai"][0]["UPerms"], value=response["Hentai"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Hentai"][0]["BPerms"], value=response["Hentai"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'now':
        embed = discord.Embed(title = prefix +"now", description = "Shows the date, time where bot is located.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"now`", inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'warn':
        embed = discord.Embed(title = response["Warn"][0]["Title"], description = response["Warn"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Warn"][0]["Usage"], value=response["Warn"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Warn"][0]["UPerms"], value=response["Warn"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Warn"][0]["BPerms"], value=response["Warn"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'h':
        embed = discord.Embed(title = response["Help"][0]["Title"], description = response["Help"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Help"][0]["Usage"], value=response["Help"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Help"][0]["UPerms"], value=response["Help"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Help"][0]["BPerms"], value=response["Help"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'hentai':
        embed = discord.Embed(title = response["Hentai"][0]["Title"], description = response["Hentai"][0]["Description"], color = embed_color)
        embed.add_field(name='Usage', value=response["Hentai"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Hentai"][0]["UPerms"], value=response["Hentai"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Hentai"][0]["BPerms"], value=response["Hentai"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'prof':
        embed = discord.Embed(title = response["Profile"][0]["Title"], description = response["Profile"][0]["Title"], color = embed_color)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'profile':
        embed = discord.Embed(title = response["Profile"][0]["Title"], description = response["Profile"][0]["Title"], color = embed_color)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        embed.add_field(name=response["Profile"][0]["Title"], value=response["Profile"][0]["Title"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setdesc':
        embed = discord.Embed(title = response["SetDesc"][0]["Title"], description = response["SetDesc"][0]["Description"], color = embed_color)
        embed.add_field(name=response["SetDesc"][0]["Usage"], value=response["SetDesc"][0]["Usage1"], inline=True)
        embed.add_field(name=response["SetDesc"][0]["UPerms"], value=response["SetDesc"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["SetDesc"][0]["BPerms"], value=response["SetDesc"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setdescription':
        embed = discord.Embed(title = response["SetDesc"][0]["Title"], description = response["SetDesc"][0]["Description"], color = embed_color)
        embed.add_field(name=response["SetDesc"][0]["Usage"], value=response["SetDesc"][0]["Usage1"], inline=True)
        embed.add_field(name=response["SetDesc"][0]["UPerms"], value=response["SetDesc"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["SetDesc"][0]["BPerms"], value=response["SetDesc"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'hackban':
        embed = discord.Embed(title = response["Hackban"][0]["Title"], description = response["Hackban"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Hackban"][0]["Usage"], value=response["Hackban"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Hackban"][0]["UPerms"], value=response["Hackban"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Hackban"][0]["BPerms"], value=response["Hackban"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'hb':
        embed = discord.Embed(title = response["Hackban"][0]["Title"], description = response["Hackban"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Hackban"][0]["Usage"], value=response["Hackban"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Hackban"][0]["UPerms"], value=response["Hackban"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Hackban"][0]["BPerms"], value=response["Hackban"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serperm':
        embed = discord.Embed(title = response["Server_Permission"][0]["Title"], description = response["Server_Permission"][0]["Description"], color = embed_color)
        embed.add_field(name=response["Server_Permission"][0]["Usage"], value = response["Server_Permission"][0]["Usage1"], inline = True)
        embed.add_field(name=response["Server_Permission"][0]["UPerms"], value = response["Server_Permission"][0]["UPerms1"], inline = True)
        embed.add_field(name=response["Server_Permission"][0]["BPerms"], value = response["Server_Permission"][0]["BPerms1"], inline = True)
        
    if command == prefix+'bounty':
        embed = discord.Embed(title = response["Bounty"][0]["Title"], description = response["Bounty"][0]["Description"], color = embed_color)        
        embed.add_field(name=response["Bounty"][0]["Usage"], value=response["Bounty"][0]["Usage1"], inline=True)
        embed.add_field(name=response["Bounty"][0]["UPerms"], value=response["Bounty"][0]["UPerms1"], inline=True)
        embed.add_field(name=response["Bounty"][0]["BPerms"], value=response["Bounty"][0]["BPerms1"], inline=True)
        await client.say(embed = embed)
        return

##### LOGGING #####


@client.event
async def on_server_role_create(role, channel = loggingchannel):
    if logserver == message.server.id:
    	embed = discord.Embed(title = "New Role Created!", color = embed_color)
    	embed.add_field(name="Role Name: ", value=role.name, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    await client.process_commands()


@client.event
async def on_server_role_delete(role, channel = loggingchannel):
    if logserver == message.server.id:
    	embed = discord.Embed(title = "Role Deleted", color = 0xF00000)
    	embed.add_field(name="Role Name: ", value=role.name, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    await client.process_commands()


@client.event
async def on_member_ban(member, channel = loggingchannel):
    if logserver == message.server.id:
    	embed = discord.Embed(title = "User Banned!", color = 0xF00000)
    	embed.set_author(name=member.name, url=member.avatar_url, icon_url=member.avatar_url)
    	embed.add_field(name="User: ", value=member.name + "#" + member.discriminator, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    await client.process_commands()


@client.event
async def on_message_edit(message, after, channel = loggingchannel):
    if logserver == message.server.id:
    	embed = discord.Embed(title = "Message Edited!", description = "In channel: <#" + message.channel.id + ">", color = embed_color)
    	embed.add_field(name="New Content: ", value=after.content, inline=True)
    	embed.add_field(name="Old Content: ", value=message.content, inline=False)
    	embed.add_field(name="User: ", value=message.author.name + "#" + message.author.discriminator, inline=False)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed = embed)
    await client.process_commands(message)
##### LOGGING #####


### MODULES ###
@client.command(pass_context = True)
async def modules(ctx):
    embed = discord.Embed(title = "Available Modules", description = "-Fun\n-Logging(Requires You to input a channel for logging in `credentials.py`)", color = embed_color)


@client.command(pass_context = True, aliases=['module-fun'])
async def modulefn(ctx):
    embed = discord.Embed(title = "Commands In Module: Fun", description = ";slotroll\n;flip\n;8ball\n;roll", color = embed_color)
    embed.set_footer(text="To see the usage of a command, do `;h ;command-name`, example: `;h ;8ball`")
    await client.say(embed = embed)

### MODULES ###


@client.command(pass_context = True, aliases=['ser'])
async def server(ctx):
    embed = discord.Embed(color = embed_color)
    embed.add_field(name="Owner:", value=ctx.message.server.owner, inline=True)
    embed.add_field(name="AFK Channel:", value=ctx.message.server.afk_channel, inline=True)
    embed.add_field(name="Server Region:", value=ctx.message.server.region, inline=True)
    embed.add_field(name="Features:", value=ctx.message.server.features, inline=True)
    embed.add_field(name="Verification Level:", value=ctx.message.server.verification_level, inline=True)
    embed.add_field(name="Member Count:", value=ctx.message.server.member_count, inline=True)
    embed.add_field(name="Creation:", value=ctx.message.server.created_at, inline=True)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


@client.command(pass_context = True, aliases=['userinfo'])
async def user(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
        embed = discord.Embed(color = embed_color)
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name="User ID:", value=member.id, inline=True)
        embed.add_field(name="User Name:", value=member, inline=True)
        embed.add_field(name="Is Bot?:", value=member.bot, inline=True)
        embed.add_field(name="Join Date:", value=member.created_at, inline=True)
        embed.add_field(name="Nickname:", value=member.display_name, inline=True)
        await client.say(embed = embed)
    else:
        embed = discord.Embed(color = embed_color)
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name="User ID:", value=member.id, inline=True)
        embed.add_field(name="User Name:", value=member, inline=True)
        embed.add_field(name="Is Bot?:", value=member.bot, inline=True)
        embed.add_field(name="Join Date:", value=member.created_at, inline=True)
        embed.add_field(name="Nickname:", value=member.display_name, inline=True)
        await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")



'''---------------------------------------------------------------------'''

@client.command(pass_context = True, aliases=['updatelinux'])
async def updatelin(ctx):
    updatefile = "linuxUPDATE.sh"
    if ctx.message.author.id != owner:
        embed = discord.Embed(description = "You're not the owner!", color = 0xFF0000)
        await client.say(embed = embed)
    else:
        embed = discord.Embed(description = "Updating...", color = embed_color)
        await client.say(embed = embed)
        os.startfile(updatefile)
        await client.logout()

@client.command(pass_context = True)
async def reboot(ctx):
    rebootf = "reboot.sh"
    await client.say("Restarting...")
    os.startfile(rebootf)
    print(Fore.GREEN + "Reboot initiated")
    await client.logout()


## HACKBAN ##
def data_entry(hkban):
    c.execute(hkban)
    conn.commit()
    global data
    data = c.fetchall()

@client.command(pass_context = True, aliases=['hb'])
async def hackban(ctx, *, id: str):
    server_id = ctx.message.server.id
    hkban = "INSERT INTO Hackbans (user_id, server_id) VALUES ('" + id + "', '" + server_id + "')"
    data_entry(hkban)
    embed = discord.Embed(description = "Successfully Hackbanned: " + id, color = embed_color)
    await client.say("Hackbanned: " + id)


def read_from_db(banonjoin):
    c.execute(banonjoin)
    conn.commit()
    global datta
    datta = c.fetchall()

@client.event
async def on_member_join(member):
    server_id = member.server.id
    user_id = member.id
    banonjoin = "SELECT COUNT(*) FROM Hackbans WHERE user_id = '" + user_id + "' AND server_id = '" + server_id + "'"
    read_from_db(banonjoin)
    if datta[0][0] < 1:
        print(Fore.BLUE + "A non-hackbanned user joined, they were not bananaed! :D")
    elif datta[0][0] > 0:
        print("user is hackbananaed")
        print(Fore.RED + "A hackbanned user joined but was bananaed! :D")
        await client.ban(member)
    print(Fore.BLUE + str(datta))

## HACKBAN ##


######################## Permissions ########################

@client.group(pass_context = True, invoke_without_command = True)
async def serperm(ctx):
    if ctx.message.author.server_permissions.administrator:
        embed = discord.Embed(title = "Permissions", description = "nsfw", color = embed_color)
        await client.say(embed = embed)
    else:
        embed = discord.Embed(description = "Insufficient Permissions!", color = 0xF00000)
        await client.say(embed = embed)

def serpermhen(sqlstr):
    c.execute(sqlstr)
    conn.commit()

def redred(sqlstr):
    c.execute(sqlstr)
    conn.commit()
    global data
    data = c.fetchall()

@serperm.command(pass_context = True)
async def nsfw(ctx, *, toggle: str):
    if toggle is None:
        await client.say("Specify whether it should be disabled or enabled. `1` to enable, `0` to disable")
    val = "0"
    server_id = ctx.message.server.id
    sqlstr = "SELECT CASE WHEN nsfw_is_enabled = '1' THEN '0' WHEN nsfw_is_enabled = '0' THEN '1' END FROM Permissions WHERE server_id = '" + server_id + "'"
    sql2 = "UPDATE Permissions SET nsfw_is_enabled = '" + toggle + "' WHERE server_id = '" + server_id + "'"
    redred(sqlstr)
    if data[0][0] == "0":
        if ctx.message.author.server_permissions.administrator == True:
            serpermhen(sql2)
            embed = discord.Embed(description = "NSFW is now disabled!", color = embed_color)
            await client.say(embed = embed)
        else:
            embed = discord.Embed(description = "Insufficient Permissions!", color = 0xFF0000)
            await client.say(embed = embed)
    elif data[0][0] == "1":
        if ctx.message.author.server_permissions.administrator == True:
            serpermhen(sql2)
            embed = discord.Embed(description = "NSFW is now enabled!", color = embed_color)
            await client.say(embed = embed)
        else:
            embed = discord.Embed(description = "Insufficient Permissions!", color = 0xFF0000)
            await client.say(embed = embed)


######################## Permissions ########################

client.run(BotToken)
