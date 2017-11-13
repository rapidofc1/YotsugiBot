#Do NOT edit past this point, unless you know what you're doing!#
#---------------------------------------------------------------------------------------------------------------------#
import discord
import asyncio
import random
import time
import datetime
import requests
from discord.ext.commands import Bot
from discord.ext import commands
import pickle
import colorama
from colorama import Fore, Back, Style
import os
import sqlite3
from credentials import BotToken
from credentials import Owners as owner
from credentials import EmbedColor as embed_color
from credentials import Prefix as prefix
from credentials import LoggingChannel as loggingchannel
from credentials import LoggingServer as logser
###
bot_version = 'v0.6.3'
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


@client.command(pass_context = True, no_pm = True)
async def send(ctx, member : discord.Member, *, message):
        if ctx.message.author.server_permissions.ban_members:
            return await client.send_message(member, embed=discord.Embed(description="Message from **" + ctx.message.author.mention + "**: " + message, color = embed_color))
            print("Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
        else:
            return await client.say(":x: Insufficient permissions!")
            print("Command Failed To |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\nReason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Ban Members permission!")


@client.command
async def h(command = None):
    if not command:
        #do normal help command
        return

    #some code to check if the command is an actual command (depends on how you make commands)
    return

 
@client.command(pass_context = True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong:  The ping time is `%dms`" % ping)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
 
#command1
@client.command(pass_context = True)
async def invite(ctx):
    embed = discord.Embed(title = "Here are invite links:", description = "Invite me to your server with this link: https://discordapp.com/oauth2/authorize?client_id=331766751765331969&scope=bot&permissions=66186303", color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
 
#command2
@client.command(pass_context = True, no_pm = True)
async def banlist(ctx):
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of Banned Members", description = x, color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
 
#command3
@client.command(pass_context=True, no_pm = True)
async def connect(ctx):
    if client.is_voice_connected(ctx.message.server):
        return await client.say("I am already connected to a voice channel. Do not disconnect me if I am in use!")
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
 
#command4
@client.command(pass_context = True, no_pm = True)
async def disconnect(ctx):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()
            print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
        
#command6
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


#command8
@client.command(pass_context = True, no_pm = True)
async def author(ctx):
    embed = discord.Embed(title = "Yotsugi Bot Author:", description = "Name: **" + bot_author + "**  \nJoined Discord: **07.02.2016  1:10 PM**  \n  **ID**: 145878866429345792  \n**Email**: yotsugibot@gmail.com  \nSay **;h** for commands.", color = embed_color)
    return await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

#command9
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


#command10
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
	
#command12
@client.command(pass_context = True, no_pm = True)
async def mute(ctx, *, member : discord.Member):
    if not ctx.message.author.server_permissions.mute_members:
        return print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and member need Mute Members permission!")
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been muted!"%member.mention)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

#command13
@client.command(pass_context = True, description='Unmutes the muted members.', no_pm = True)
async def unmute(ctx, *, member : discord.Member):
    if not ctx.message.author.server_permissions.mute_members:
        return print(Fore.RED + "Command Failed To Execute |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]\n       Reason: " + Fore.YELLOW + "Insufficient Permissions! Both user and bot need Mute Members permission!")
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been unmuted!"%member.mention)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

#command14
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


#command20
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


#command17
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

	
#command18
@client.command(pass_context = True, no_pm = True)
async def servers(ctx):
    x = '`\n`'.join([str(server) for server in client.servers])
    y = len(client.servers)
    print(x)
    embed = discord.Embed(title = "Servers: " + str(y), description = x, color = embed_color)
    await client.say(embed = embed)
    print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")


#Stats Command
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
        print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran: " + prefix + aliases + "\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")
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
    embed = discord.Embed(color = embed_color)
    embed.add_field(name="Hosting Guides", value="[Click Here](https://yotsugibot.readthedocs.io/en/latest/)", inline=False)
    embed.add_field(name="Commands List", value="[Click Here](https://yotsugibot.readthedocs.io/en/latest/Commands%20List)", inline=True)
    if not command:
            await client.say(embed = embed)
            return

        #some code to check if the command is an actual command (depends on how you make commands)
    if command == prefix+'b':
        embed = discord.Embed(title = "`" + prefix + "ban` / `" + prefix + "b`", description = "Bans the user from the server", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"ban @User/ID` or `"+ prefix +"b @User/UserID`", inline=True)
        embed.add_field(name='User Permissions:', value='Ban Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Ban Members', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ban':
        embed = discord.Embed(title = "`" + prefix + "ban` / `" + prefix + "b`", description = "Bans the user from the server", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"ban @User/ID` or `"+ prefix +"b @User/UserID`", inline=True)
        embed.add_field(name='User Permissions:', value='Ban Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Ban Members', inline=True)
        await client.say(embed = embed)
        return


    if command == prefix+'k':
        embed = discord.Embed(title = "`"+ prefix +"kick` / `"+ prefix +"k`", description = "Kicks the user from the server", color = embed_color)
        embed.add_field(name='Usage', value="`" + prefix +"kick @User/ID` or `" + prefix +"k @User/UserID`", inline=True)
        embed.add_field(name='User Permissions:', value='Kick Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Kick Members', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'kick':
        embed = discord.Embed(title = "`"+ prefix +"kick` / `"+ prefix +"k`", description = "Kicks the user from the server", color = embed_color)
        embed.add_field(name='Usage', value="`" + prefix +"kick @User/ID` or `" + prefix +"k @User/UserID`", inline=True)
        embed.add_field(name='User Permissions:', value='Kick Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Kick Members', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serverid':
        embed = discord.Embed(title = "`"+ prefix +"serverid` / `"+ prefix +"serid`", description = "Show's the ID of the server.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"serverid` or `;serid`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ud':
        embed = discord.Embed(title = "`"+ prefix +"ud`", description = "Searches urban disctionary for the meaning of a word.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"ud lol`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'8ball':
        embed = discord.Embed(title = "`"+ prefix +"eightball` / `"+ prefix +"8ball`", description = "8balls your question.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"eightball to be or not to be` or `"+ prefix +"8ball to be or not to be`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'eightball':
        embed = discord.Embed(title = "`"+ prefix +"eightball` / `"+ prefix +"8ball`", description = "8balls your question.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"eightball to be or not to be` or `"+ prefix +"8ball to be or not to be`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serid':
        embed = discord.Embed(title = "`"+ prefix +"serverid` / `"+ prefix +"serid`", description = "Show's the ID of the server.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"serverid` or `"+ prefix +"serid`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'clear':
        embed = discord.Embed(title = "`"+ prefix +"clear` / `"+ prefix +"prune` / `"+ prefix +"purge`", description = "Deletes `x` amount of messages.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"clear 5` or `"+ prefix +"prune 5` or `"+ prefix +"purge 5`", inline=True)
        embed.add_field(name='User Permissions:', value='Manage Messages', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'prune':
        embed = discord.Embed(title = "`"+ prefix +"clear` / `"+ prefix +"prune` / `"+ prefix +"purge`", description = "Deletes `x` amount of messages.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"clear 5` or `"+ prefix +"prune 5` or `"+ prefix +"purge 5`", inline=True)
        embed.add_field(name='User Permissions:', value='Manage Messages', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'purge':
        embed = discord.Embed(title = "`"+ prefix +"clear` / `"+ prefix +"prune` / `"+ prefix +"purge`", description = "Deletes `x` amount of messages.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"clear 5` or `"+ prefix +"prune 5` or `"+ prefix +"purge 5`", inline=True)
        embed.add_field(name='User Permissions:', value='Manage Messages', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'mute':
        embed = discord.Embed(title = "`"+ prefix +"mute`", description = "Mutes the user in the channel where command was ran.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"mute @User`", inline=True)
        embed.add_field(name='User Permissions:', value='Mute Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Manage Channels', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'unmute':
        embed = discord.Embed(title = "`"+ prefix +"unmute`", description = "Mutes the user in the channel where command was ran.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"unmute @User`", inline=True)
        embed.add_field(name='User Permissions:', value='Mute Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Manage Channels', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'stats':
        embed = discord.Embed(title = "`"+ prefix +"stats`", description = "Shows bot's statistics.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"stats`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'author':
        embed = discord.Embed(title = "`"+ prefix +"author`", description = "Shows information about bot author.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"author`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'banlist':
        embed = discord.Embed(title = "`"+ prefix +"banlist`", description = "Shows list of banned users for that server..", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"banlist`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'ping':
        embed = discord.Embed(title = "`"+ prefix +"ping`", description = "Shows your ping to the bot..", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"ping`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'connect':
        embed = discord.Embed(title = "`"+ prefix +"connect`", description = "Joins the voice channel.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"connect`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Connect', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'disconnect':
        embed = discord.Embed(title = "`"+ prefix +"disconnect`", description = "Leaves the voice channel.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"disconnect`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Connect', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'channelid':
        embed = discord.Embed(title = "`"+ prefix +"channelid` / `"+ prefix +"chnlid``", description = "Shows the channel ID the command was ran in.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"channelid` or `"+ prefix +"chnlid`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'chnlid':
        embed = discord.Embed(title = "`"+ prefix +"channelid` / `"+ prefix +"chnlid``", description = "Shows the channel ID the command was ran in.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"channelid` or `"+ prefix +"chnlid`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'github':
        embed = discord.Embed(title = "`"+ prefix +"github`", description = "Gives the link to GitHub.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"github`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'send':
        embed = discord.Embed(title = "`"+ prefix +"send`", description = "Sends a message to a user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"send @User Hi`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'shutdown':
        embed = discord.Embed(title = "`"+ prefix +"die` / `"+ prefix +"shutdown`", description = "Boots the bot offline.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"shutdown` or `"+ prefix +"die`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'die':
        embed = discord.Embed(title = "`"+ prefix +"die` / `"+ prefix +"shutdown`", description = "Boots the bot offline.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"shutdown` or `"+ prefix +"die`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setrole':
        embed = discord.Embed(title = "`"+ prefix +"setrole` / `"+ prefix +"setrl`", description = "Gives a role to a user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"setrole @User Role-Name` or `"+ prefix +"setrl @User Role-Name`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'setrl':
        embed = discord.Embed(title = "`"+ prefix +"setrole` / `"+ prefix +"setrl`", description = "Gives a role to a user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"setrole @User Role-Name` or `"+ prefix +"setrl @User Role-Name`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'removerole':
        embed = discord.Embed(title = "`"+ prefix +"removerole` / `"+ prefix +"remrl`", description = "Removes a role from the user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"removerole @User Role-Name` or `"+ prefix +"remrl @User Role-Name`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'remrl':
        embed = discord.Embed(title = "`"+ prefix +"removerole` / `"+ prefix +"remrl`", description = "Removes a role from the user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"removerole @User Role-Name` or `"+ prefix +"remrl @User Role-Name`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'flip':
        embed = discord.Embed(title = "`"+ prefix +"flip` / `"+ prefix +"flipcoin`", description = "Flips the coin.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"flip` or `"+ prefix +"flipcoin`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages, Attach Files', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'roll':
        embed = discord.Embed(title = "`"+ prefix +"roll`", description = "Rolls the dice in NdN format.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"roll 5d5`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'servers':
        embed = discord.Embed(title = "`"+ prefix +"servers`", description = "Shows the list of servers the bot is in.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"servers`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'warn':
        embed = discord.Embed(title = "`"+ prefix +"warn`", description = "Warns the user.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"warn @ser Rude`", inline=True)
        embed.add_field(name='User Permissions:', value='Kick Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'h':
        embed = discord.Embed(title = "`"+ prefix +"h`", description = "Shows the info about a command.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"h "+ prefix +"ban`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'now':
        embed = discord.Embed(title = "`"+ prefix +"now`", description = "Shows the current day, date, time, year and hours/minutes.", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"now`", inline=True)
        embed.add_field(name='User Permissions:', value='`None`', inline=True)
        embed.add_field(name='Bot Permissions:', value='Send Messages, Attach Files, Embed Links', inline=True)
        await client.say(embed = embed)
        return
        
    if command == prefix+'hackban':
        embed = discord.Embed(title = "`"+ prefix +"hb` / `" + prefix + "hackban`", description = "Bans the user which is not in the server. **Must Be ID of the user**", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"hb 123123123123` or "+prefix+"`hackban 123123123123`", inline=True)
        embed.add_field(name='User Permissions:', value='Ban Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Ban Members', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'hb':
        embed = discord.Embed(title = "`"+ prefix +"hb` / `" + prefix + "hackban`", description = "Bans the user which is not in the server. **Must Be ID of the user**", color = embed_color)
        embed.add_field(name='Usage', value="`"+ prefix +"hb 123123123123` or "+prefix+"`hackban 123123123123`", inline=True)
        embed.add_field(name='User Permissions:', value='Ban Members', inline=True)
        embed.add_field(name='Bot Permissions:', value='Ban Members', inline=True)
        await client.say(embed = embed)
        return

    if command == prefix+'serperm':
        embed = discord.Embed(title = "`" + prefix + "serperm`", description = "Server permissions, provide no arguments to show the list of all permissions.", color = embed_color)
        embed.add_field(name='Usage', value = "`" + prefix + "serperm` or `" + prefix + "serperm nsfw 0`", inline = True)
        embed.add_field(name='User Permissions:', value = '**Administrator**', inline = True)
        embed.add_field(name='Bot Permissions:', value = '`None`', inline = True)
        await client.say(embed = embed)
        return

##### LOGGING #####


@client.event
async def on_server_role_create(role, channel = loggingchannel):
    if logser == message.server.id:
    	embed = discord.Embed(title = "New Role Created!", color = embed_color)
    	embed.add_field(name="Role Name: ", value=role.name, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    elif logser != message.server.id: print("")


@client.event
async def on_server_role_delete(role, channel = loggingchannel):
    if logser == message.server.id:
    	embed = discord.Embed(title = "Role Deleted", color = 0xF00000)
    	embed.add_field(name="Role Name: ", value=role.name, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    elif logser != message.server.id: print("")


@client.event
async def on_member_ban(member, channel = loggingchannel):
    if logser == message.server.id:
    	embed = discord.Embed(title = "User Banned!", color = 0xF00000)
    	embed.set_author(name=member.name, url=member.avatar_url, icon_url=member.avatar_url)
    	embed.add_field(name="User: ", value=member.name + "#" + member.discriminator, inline=True)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed=embed)
    elif logser != message.server.id: print("")


@client.event
async def on_message_edit(message, after, channel = loggingchannel):
    if logser == message.server.id:
    	embed = discord.Embed(title = "Message Edited!", description = "In channel: **" + str(message.channel) + "**", color = embed_color)
    	embed.add_field(name="New Content: ", value=after.content, inline=True)
    	embed.add_field(name="Old Content: ", value=message.content, inline=False)
    	embed.add_field(name="User: ", value=str(message.author), inline=False)
    	embed.add_field(name="Server:", value=message.server.name, inline=False)
    	embed.add_field(name="Server ID:", value=message.server.id, inline=False)
    	await client.send_message(discord.Object(id=loggingchannel), embed = embed)
    elif logser != message.server.id: print("")
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
    if ctx.message.author.server_permissions.administrator:
        data_entry(hkban)
        embed = discord.Embed(description = "Successfully Hackbanned: " + str(id), color = embed_color)
        await client.say(embed = embed)
    else:
        embed = discord.Embed(description = "Insufficient Permissions!", color = 0xFF0000)
        await client.say(embed = embed)


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



########################################################## N S F W ##########################################################

hentai_images = [
    'https://cdn.discordapp.com/attachments/331827935030018048/362015619991994368/DAX32vyXkAAvSVN.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015622319833098/DAXhM29W0AAHPwJ.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015626744692736/e4e9524f-a2dd-4083-b768-2aab8bdde78b.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015634571132940/ec4b81dd9a.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015632281305088/ea527770601c3a2a9f529d12bee97ac4.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015636983119872/eyJ1cmwiOiJodHRwczovL2Rpc2NvcmQuc3RvcmFnZS5nb29nbGVhcGlzLmNvbS9hdHRhY2htZW50cy8yODIzODU2ODAyODAxOTA5.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015639277142017/f54c8c6dcf622c707bb2be228de18f32.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015649742192640/image-59.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015651780624385/image-159.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015656675246081/jZx6pWTGcwE.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015665009328129/Konachan.com_-_177821_aisare_roommate_bow_brown_eyes_brown_hair_censored_game_cg_loli_nohara_karen_p.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015668356251648/Konachan.com_-_180438_bed_black_hair_blue_eyes_blush_game_cg_inagaki_sae_loli_masturbation_nonohara_.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015670030041091/Konachan.com_-_181291_alice_parade_anus_black_hair_blush_green_eyes_inemuri_yamane_itou_noiji_loli_l.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015683510272001/Konachan.com_-_186160_2girls_ass_bed_blush_breasts_cum_fang_garter_glasses_loli_navel_nipples_origin.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015701411823616/Konachan.com_-_192657_animal_ears_bell_catgirl_collar_fang_green_hair_loli_long_hair_mvv_navel_nude_.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362015704825987072/Konachan.com_-_193097_aqua_eyes_blush_flat_chest_gray_hair_konpaku_youmu_loli_namamo_nanase_navel_ni.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017919414042635/1eb61d80-2f2c-4adf-84e0-74a5298a35b4.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017921926430720/2ecf8d51-2ca2-461e-a266-0145f604eb74.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017929232908288/3a19b7c173d61998ca3a628cd3209a59.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017932106006548/4a4dde28b1e7915b5a0abcd279e7dd1d.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017935780478976/6fbdc8211503c43ee309738b0036eb73.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017946580811776/8da1020b2d0c6737dcced9b2112c4650.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017947637645323/8f72dc37-0a17-4b77-9166-dd03510bd73a.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017952322551808/9f1ee1c9bc557768218ae05de95b3500.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362017958781779968/30b1b22977b258e0a5eea49d2396deda.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019786483433473/tumblr_on5gf9L1ZT1sm2fjbo1_1280.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019790069563392/tumblr_oot3coeLu31sm2fjbo1_1280.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019798013575168/unknown.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019797812117514/tumblr_opvjpciSvp1sm2fjbo1_1280.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019810898477056/yande.re_378545_animal_ears_anus_ass_breast_grab_bunny_ears_censored_inaba_tewi_kitsunerider_loli_ni.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019811464839168/yande.re_371508_bug_system_censored_cunnilingus_game_cg_gothic_lolita_koushou_aika_lolita_fashion_ma.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019815692435466/yande.re_380386_aida_takanobu_game_cg_naked_nipples_onohara_hazuki_sono_hanabira_ni_kuchizuke_wo_suo.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019819559714826/yande.re_383918_anal_anus_bottomless_bra_breast_hold_breasts_dildo_kopianget_megane_naked_nipples_op.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019852468224000/yande.re_389847_game_cg_k-ko_loli_pantsu_pantyhose_pussy_juice_seguchi_mahiru_skirt_lift_tinkle_posi.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362019852027953153/yande.re_386873_ass_bondage_bug_system_fingering_game_cg_koushou_aika_marushin_mihama_yomi_naked_nip.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021088923746304/6529e06f81946d23ed7bf7775310dad0.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021093164187660/7279d52eecfcfca95b1f01394b3df0f4.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021099300454400/9877a3eb0eb4726cf7642cf1aaf2ad95.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021118334205952/2180256b-d859-4402-beae-eed99abab820.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021120368443394/781707f639299eaaa5b384c32478bb7e.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021124118413324/43495068_p0.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021130267131906/424033c8f5b6de18bb4f5461b040992c.png',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021134692122624/a63ca51e57765b3336a38f819a05272c.jpeg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021130049159178/47069417d93b8ed815f284afc6e2c23e.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362021138366464001/a434c297-a7df-4cfd-99e4-e98d698809d2.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362025063786217482/FB_IMG_1506090797599.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362025067414159361/FB_IMG_1506090806514.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362025068366397461/FB_IMG_1506090864607.jpg',
    'https://cdn.discordapp.com/attachments/331827935030018048/362025070526201867/FB_IMG_1506090890627.jpg',
    'https://images-ext-2.discordapp.net/external/QtKBxzXpzM8zqryRGsUtgz2zC7NU17jKy8z_hlsLagQ/https/konachan.com/image/44862a61b8e909157c9c0d8a57b4ca2d/Konachan.com%2520-%2520251956%2520ange_vierge%2520beach%2520bikini%2520censored%2520cum%2520green_eyes%2520kadokura_umekichi%2520long_hair%2520mayuka_sanagi%2520navel%2520penis%2520purple_hair%2520sex%2520swimsuit%2520water.png?width=598&height=449',
    'https://images-ext-1.discordapp.net/external/loaP3URcpSVsapHP7tjop8jOadgMLjvcG4-5zZEPCpA/https/files.yande.re/image/c50c0932493fed2b90338a87ca5fee5a/yande.re%2520414974%2520bottomless%2520breasts%2520fate_extra%2520fate_extra_ccc%2520fate_stay_night%2520meltlilith%2520nipples%2520no_bra%2520pussy%2520uncensored%2520yahiro_%2528666131415%2529.jpg?width=142&height=200',
    'https://images-ext-2.discordapp.net/external/jeOOXebKA1qPGxUfShH7-1f3J9qzQnbqAQ9NCwTNuqs/https/konachan.com/image/98f5ccd1ab6601a2059c4187e4721d94/Konachan.com%2520-%2520251249%2520blue_eyes%2520blush%2520book%2520breasts%2520brown_hair%2520cum%2520headband%2520idolmaster%2520necklace%2520nipples%2520no_bra%2520nopan%2520pussy%2520sayori%2520short_hair%2520uncensored%2520watermark.png?width=283&height=201',
    'https://images-ext-2.discordapp.net/external/Vmijc4QFQT8FNQZ1wOYNWTCq15tm8N-oohCIkGE8lGs/https/konachan.com/image/3775eadef4e2e0248d07add721dc21b9/Konachan.com%2520-%2520251709%2520barefoot%2520blush%2520breasts%2520censored%2520game_cg%2520handjob%2520navel%2520nipples%2520nude%2520onsen%2520penis%2520pink_eyes%2520pink_hair%2520tagme_%2528artist%2529%2520water%2520wet.png?width=321&height=181',
    'https://images-ext-1.discordapp.net/external/6I5JfZyLAgpheCYPEmU6DvtrqNUm7f5E317fS71oaRw/https/files.yande.re/image/06b1be9dd21a83b525d357fa80264386/yande.re%2520414648%2520breasts%2520fingering%2520leotard%2520mecha_musume%2520naked%2520nier_automata%2520nipples%2520no_bra%2520pussy%2520pussy_juice%2520tarakanovich%2520thighhighs%2520uncensored%2520yorha_no.2_type_b%2520yuri.jpg?width=154&height=201',
    'https://images-ext-2.discordapp.net/external/9f6hJ944BU8LiR-tUofsDNNbfDXpU8Yv2IiQHAp3lnc/https/danbooru.donmai.us/data/__grace_blackberry_greaseberries_drawn_by_shirou_masamune__57f20a41efdd8d1fd555ead9d6400ffb.jpg?width=294&height=200',
    'https://images-ext-2.discordapp.net/external/YIsBdzeWkdU9Rx4zhkNU1dYZuaLB10UBtIKwH-6k-RQ/https/files.yande.re/image/e8f7184b2cc2c8fa3558112003bd14f3/yande.re%2520413936%2520846gou%2520bikini%2520breast_grab%2520fate_grand_order%2520masturbation%2520minamoto_no_raikou_%2528fate_grand_order%2529%2520pussy_juice%2520swimsuits.jpg?width=116&height=201',
    'https://images-ext-1.discordapp.net/external/23evGjfDytIAoU9h2Sh2Ow01OoPqfN9jJlgTaAP3yUw/https/konachan.com/image/fc958257f4b0abf8c5a47847c73a56a2/Konachan.com%2520-%2520252682%2520ass%2520blue_eyes%2520breast_grab%2520breasts%2520dark_skin%2520kyonyuu_fantasy%2520long_hair%2520nipples%2520nude%2520paia%2520pink_hair%2520sex%2520tagme_%2528artist%2529%2520watermark%2520wet%2520yurinas.jpg?width=321&height=181',
    'https://images-ext-2.discordapp.net/external/ZLnPCknXHZoPBFC_782b8ViNoh4jupBAjE8H0YmQzn0/https/img.rule34.xxx/images/2328/c8820e01deee9014263d7c696f493f6b41a9fb45.jpg?width=147&height=200',
    'https://images-ext-1.discordapp.net/external/UHcvmLOKCrQraBHf3tUOwEuQA5LFj9mwKD3Qmkiz1fg/https/files.yande.re/image/c765c0b9917833fc29fef876ed6f2ecf/yande.re%2520414423%2520anus%2520bakemonogatari%2520feet%2520loli%2520naked%2520nipples%2520oshino_shinobu%2520pointy_ears%2520pussy%2520shiro_ringo%2520thighhighs.jpg?width=142&height=200',
    'https://images-ext-1.discordapp.net/external/2yFPrUiDkIeChI9PtwAO_m5WYsXQcnrwHdfRRDn2M94/https/simg3.gelbooru.com/images/f8/0f/f80f264aad485c676df1fccad80ce53d.jpeg?width=151&height=201',
    'https://images-ext-1.discordapp.net/external/76NGGsjF0853zpDpu7SZSLI7TV8OPiVm4x_8OJmW0ao/https/danbooru.donmai.us/data/__pkp_girls_frontline_drawn_by_463_jun__957f0855bca183e940d2ecf1fd3629d2.jpg?width=141&height=200',
    'https://images-ext-1.discordapp.net/external/VVcPy2u-FDMj005FkOhhLp6dJ2i7rUoyswEkn0cbOG0/https/konachan.com/image/dfaf95b9a60a25bc5676eb78d93b6c18/Konachan.com%2520-%2520252381%2520blush%2520breasts%2520brown_hair%2520censored%2520green_eyes%2520hewsack%2520long_hair%2520naked_shirt%2520navel%2520nipples%2520no_bra%2520nopan%2520penis%2520ponytail%2520sex%2520spread_legs%2520thighhighs.png?width=283&height=200',
    'https://images-ext-1.discordapp.net/external/nu0RZmj1S0_gpx5mKlaFLqUyYbKdjTlnsKE-40elRNM/https/konachan.com/image/545e91bf011e964c69522eb57f6ecf5c/Konachan.com%2520-%2520251486%2520black_hair%2520blush%2520breasts%2520fellatio%2520man_%2528man-room%2529%2520navel%2520nipples%2520nude%2520original%2520penis%2520pubic_hair%2520short_hair%2520uncensored.jpg?width=283&height=200',
    'https://images-ext-1.discordapp.net/external/vVnQcxAm-CqQ94KrnFqh_GWG1h_wE1c_8RDJO4YVVM8/https/files.yande.re/image/1572ce57283df1d8763154eb0bb1245b/yande.re%2520415214%2520areola%2520bilan_hangxian%2520breasts%2520cleavage%2520cum%2520dice_fuumi%2520nipple_slip%2520no_bra%2520open_shirt%2520paizuri%2520penis%2520south_dakota_%2528azurlane%2529%2520uncensored.jpg?width=143&height=201',
    'https://images-ext-2.discordapp.net/external/mhqBW2N_EuIN1UySaahnr-zDzYWCuWLEH4rCpy5hev8/https/danbooru.donmai.us/data/__atago_azur_lane_drawn_by_kisaragi_nana__542dca1eacd2a5701883fa5b4bc9e952.png?width=143&height=200',
    'https://images-ext-2.discordapp.net/external/VRGk9SRq2Vyje13j3m6oTihLQn-fZN090b3WJ8MlWpY/https/img.rule34.xxx/images/2328/ba7c5b64bfa70b3ba8c80bf5362992fbf15d22c2.jpeg?width=142&height=200',
    'https://images-ext-2.discordapp.net/external/Cg30TcDh65fzccky9QJhq5qBQQgcljr6febRnNJKwsQ/https/simg3.gelbooru.com/images/a5/75/a575305043226cdc8484af6393b79dec.gif',
    'https://images-ext-2.discordapp.net/external/9YVNLTKqfeBQyXCrVTtZF53GELVS6Q3co9Jb79buYIQ/https/konachan.com/image/ddcf6b17d44c3a39f211e07b73dc395b/Konachan.com%2520-%2520251728%25202girls%2520ass%2520bed%2520blush%2520bow%2520breasts%2520evuoaniramu%2520fingering%2520green_eyes%2520green_hair%2520long_hair%2520navel%2520nipples%2520nude%2520pink_hair%2520purple_eyes%2520pussy%2520spread_legs%2520yuri.png?width=300&height=200',
    'https://images-ext-2.discordapp.net/external/khurpKAAehOC5gV_rAJq50cs8fxEb-FRkq4UubAQtL0/https/img.rule34.xxx/images/2328/14f3e20522d6fe54601d3be81a2666c703580629.png?width=142&height=201',
    'https://images-ext-2.discordapp.net/external/97V8isP7aPyOL2thu7O1hYIxR2nJNMWAU4XJ-zY8-Cw/https/simg3.gelbooru.com/images/16/f7/16f7ec22e55e863d41d0766180a13b5f.png?width=153&height=200',
    'https://images-ext-1.discordapp.net/external/PiVzCvHi2lnoLVaYd5AEx50x1uZV1tVgFH5iisBqP1g/https/files.yande.re/image/4346069d8c4af4439732f3dd1a1ea7c5/yande.re%2520415213%2520bilan_hangxian%2520breasts%2520dice_fuumi%2520nipples%2520no_bra%2520open_shirt%2520pubic_hair%2520south_dakota_%2528azurlane%2529%2520tagme%2520thighhighs%2520torn_clothes%2520wet.jpg?width=143&height=201',
    'https://images-ext-1.discordapp.net/external/WSp7gsFfuuF4Yk2L6qP2cbFXQXjhUTNcuGgu_DloqbY/https/konachan.com/image/2ffc7bbf51003345dd23a3c814c3c1ca/Konachan.com%2520-%2520252686%25202girls%2520animal_ears%2520anthropomorphism%2520anus%2520ass%2520azur_lane%2520bed%2520blonde_hair%2520blue_eyes%2520blush%2520bow%2520censored%2520crown%2520long_hair%2520purple_eyes%2520pussy.jpg?width=321&height=181',
    'https://images-ext-2.discordapp.net/external/fGvrtbdGP3dz6lSipzyM2DFL6F4KROKf54HozmSNg6M/https/img.rule34.xxx/images/2328/8a6d3cf31a6e8df74b4b5eb88714ce31.jpeg?width=160&height=200',
    'https://images-ext-2.discordapp.net/external/siPXEzdN_pAT-jzUJUZjY0HIJgaspNejXbCR7qDQHS4/https/danbooru.donmai.us/data/__aira_fire_emblem_and_fire_emblem_seisen_no_keifu__57cf7a8296dce222bb5da53fb42ed85e.jpg?width=208&height=200',
    'https://simg3.gelbooru.com/images/c8/05/c80583f79666b8e0f39a90bbbd59e275.png',
    'https://danbooru.donmai.us/data/__carol_malus_dienheim_senki_zesshou_symphogear_drawn_by_shunzou__daa2c014402afd559a2263c86acd8ad5.jpg',
    'https://konachan.com/image/985f519c79c77505a212b8e1899ac5ac/Konachan.com%20-%20251363%20anus%20blonde_hair%20breasts%20game_cg%20green_eyes%20nipples%20no_bra%20nopan%20open_shirt%20pussy%20short_hair%20spread_legs%20spread_pussy%20uncensored%20yuuri_shachi.png',
    'https://files.yande.re/image/502831dc8f0869a8399b19709d0e3c35/yande.re%20415171%20fellatio%20hex_maniac_(pokemon)%20naked%20nipples%20penis%20pokemon%20uncensored%20yas_(35373).png',
    'https://konachan.com/image/d878b65fd874ce8e20a1ff21349ca55b/Konachan.com%20-%20252630%20anal%20blush%20braids%20breasts%20censored%20collar%20fellatio%20gloves%20group%20handjob%20long_hair%20male%20nipples%20no_bra%20nopan%20penis%20ponytail%20pussy%20rebe11%20sex%20wink.png',
    'https://files.yande.re/image/eb3f6cfa8ffd51330a75bfb8611e7feb/yande.re%20414721%20bikini_top%20bottomless%20breasts%20censored%20cum%20cunnilingus%20fate_grand_order%20fellatio%20nipples%20open_shirt%20penis%20pussy%20pussy_juice%20saber_extra%20uzuki_karasu.png',
    'https://images-ext-1.discordapp.net/external/o-g4LZT90Rqnyk-OUq6fewscdhC0eJnI99h2KNOY_kA/https/konachan.com/image/30a50cf6c0eb4e557cc696e16b38921a/Konachan.com%2520-%2520251264%2520blonde_hair%2520blush%2520bow%2520breast_grab%2520breasts%2520bunny_ears%2520censored%2520cum%2520game_cg%2520long_hair%2520naruse_nono%2520nipples%2520penis%2520ponytail%2520purple_eyes%2520pussy%2520sex.jpg?width=321&height=181',
    'https://images-ext-1.discordapp.net/external/axtogVfGAJgDgifKCqawBwE_n0xSZEHRkfouhKECnRI/https/img.rule34.xxx/images/2328/f2cd126b50cde7167231bc41a7c043bcea40375a.jpg?width=142&height=200',
    'https://danbooru.donmai.us/data/__jougasaki_mika_idolmaster_and_idolmaster_cinderella_girls_drawn_by_sumi_oyasumie__ebfe81017cb5d00b4c6273c77cf65863.png',
    'https://files.yande.re/image/2b35f1353e2d93cac2638324963acdd1/yande.re%20414109%20anus%20headphones%20heels%20nipples%20pantsu%20see_through%20sonico%20super_sonico%20thighhighs%20underboob%20v-mag%20wallpaper.jpg',
    'https://images-ext-2.discordapp.net/external/YgLuRzPDMw-hDzXRodnasnY8KH7S5xQ00TtLMWxNlqU/https/konachan.com/image/0a756c44f632b1ef066ff902dc3f42f0/Konachan.com%2520-%2520251210%2520animal_ears%2520blonde_hair%2520blue_eyes%2520breasts%2520fang%2520goban%2520japanese_clothes%2520kimono%2520nipples%2520photoshop%2520pussy%2520tail%2520thighhighs%2520uncensored%2520white.png?width=321&height=201',
    'https://images-ext-2.discordapp.net/external/bhNm6mOBwxhbPQ6cM4Xrxw3yrsNJVbmqXgPDBpCc-Rk/https/img.rule34.xxx/images/2328/304ff0908b5fe3713fb7eafd32be87aebc86ca3e.gif',
    'https://simg3.gelbooru.com/images/48/6c/486ce5243f91c044413423540ccdab87.png',
    'https://danbooru.donmai.us/data/__dmm_and_girls_symphony__da7861f68bf12391f1f34644e009e326.jpg',
    'https://konachan.com/image/ed2ca9118166f20e72d2d829aac17ca8/Konachan.com%20-%20251931%20ass%20atago_(kancolle)%20blonde_hair%20dantewontdie%20gloves%20hat%20long_hair%20masturbation%20military%20nopan%20pussy%20pussy_juice%20torn_clothes%20uncensored%20vibrator.jpg',
    'https://files.yande.re/image/9435c0344888ff5756df2a6ffa97bb69/yande.re%20414111%20breast_hold%20headphones%20naked%20pussy%20sonico%20super_sonico%20thighhighs%20uncensored%20v-mag.png',
    'https://images-ext-1.discordapp.net/external/dKLXrfE1m4Se2YGhihdn1THkMjOecmc0lzVXb_ZFpSs/https/konachan.com/image/335aafffa2f921484a1a08f249c14f0c/Konachan.com%2520-%2520252556%25202girls%2520barefoot%2520blonde_hair%2520bow%2520breasts%2520brown_hair%2520long_hair%2520matsukaze_rin%2520navel%2520nipples%2520nude%2520photoshop%2520pussy%2520red_eyes%2520scan%2520tsuruki_shizuka%2520uncensored.png?width=281&height=201',
    'https://simg3.gelbooru.com/images/39/58/39585c30d5a36e668ff0308f6e54cbad.png',
    'https://danbooru.donmai.us/data/__kimura_natsuki_idolmaster_and_idolmaster_cinderella_girls_drawn_by_tkhs__8d1588bb8f59e89de8efe2a86176bfd1.jpg',
    'https://files.yande.re/image/257c3e70feee5289df612531667a272d/yande.re%20414990%20cleavage%20cum%20hatakaze_(kancolle)%20japanese_clothes%20kantai_collection%20open_shirt%20zhou_yu_(van).jpg',
    'https://images-ext-1.discordapp.net/external/wVfR--crf-vkuM-C89T_pxZDOn_syHSxb9t7rjteYE8/https/konachan.com/image/14822e881bba739d805952915149d298/Konachan.com%2520-%2520251353%25202girls%2520ass%2520barefoot%2520cameltoe%2520cosplay%2520dress%2520fingering%2520gloves%2520headband%2520lasterk%2520nier%2520panties%2520pussy%2520red_eyes%2520thighhighs%2520uncensored%2520underwear%2520yuri.jpg?width=315&height=201',
    'https://danbooru.donmai.us/data/__himekaidou_hatate_and_shameimaru_aya_touhou_drawn_by_kondou_ryunosuke__65851d273eedb01807a09a181c4f5d45.jpg',
    'https://images-ext-1.discordapp.net/external/94bOOthCNKtAKFmef7_wlHDwa7qY4xs15kWQqOjbnmk/https/danbooru.donmai.us/data/__himekaidou_hatate_touhou_drawn_by_caburi_aki__8efd554e40fc0dbc41632ba6bc12ad3d.jpg?width=140&height=201',
    'https://danbooru.donmai.us/data/__suzukaze_aoba_new_game_drawn_by_hera_hara0742__f1189b3eeef14adae69151ee5fd42c5d.jpg',
    'https://konachan.com/image/74d9e54dd65e8b3730c1f799808ddfb1/Konachan.com%20-%20252176%20anus%20aqua_eyes%20aqua_hair%20ass%20censored%20hatsune_miku%20long_hair%20pussy%20signed%20spread_pussy%20sunglasses%20twintails%20vocaloid%20wink%20yubo.jpg',
    'https://files.yande.re/image/f92a3a104c0c690be55b44340f4f58af/yande.re%20414472%20cirno%20cum%20feet%20loli%20naked%20nipples%20touhou%20wings%20y.i._(lave2217).jpg',
    'https://images-ext-2.discordapp.net/external/fKNB2K6I8zmE4Dxv_ZP7o5swHSiYlak2PXDYmg7hjGE/https/simg3.gelbooru.com/images/59/26/5926cfbe2139eac1c8f9347a4aa17697.png?width=155&height=201',
    'https://konachan.com/image/842b522aaf7ca858c5192fd8bc9e7d9a/Konachan.com%20-%20252507%20blush%20breasts%20censored%20imo_bouya%20nipples%20no_bra%20open_shirt%20panties%20pantyhose%20pink_hair%20purple_eyes%20pussy%20short_hair%20tears%20tie%20underwear%20vibrator.jpg',
    'https://files.yande.re/image/b40b108017068ed0773fd4356463458d/yande.re%20414812%20animal_ears%20anus%20ass%20belldandy%20breast_grab%20crossover%20feet%20fingering%20holo%20naked%20nipples%20pussy%20pussy_juice%20robert_knight%20tail%20uncensored%20wet%20yuri.png',
    'https://danbooru.donmai.us/data/__caster_and_tamamo_cat_fate_grand_order_and_fate_series_drawn_by_afuro__667a3a7c962c21ae768d76444cc3d222.jpg',
    'https://files.yande.re/image/1acd33eb278be81fdc941592b638eec6/yande.re%20415118%20anus%20feet%20golden_darkness%20horns%20naked%20nipples%20photoshop%20pussy%20to_love_ru%20to_love_ru_darkness%20uncensored%20yabuki_kentarou.jpg',
    'https://images-ext-1.discordapp.net/external/3Nb-n___J4wAMFwTufbT1szGe--UfSIvRKNmHLI8mkk/https/konachan.com/image/9e77334c64cc0cc34deef39e035d873e/Konachan.com%2520-%2520251480%2520anus%2520ass%2520blush%2520brown_eyes%2520brown_hair%2520censored%2520game_cg%2520mochio%2520night%2520noe_noeru%2520pussy%2520pussy_juice%2520reflection%2520ribbons%2520seifuku%2520thighhighs%2520twintails.png?width=321&height=181',
    'https://images-ext-1.discordapp.net/external/Jzi-Lnaj4u-sWRqEGi-70VhCO1lpVT3tSVgJx1QcqsE/https/simg3.gelbooru.com/images/36/c5/36c5e83086326ca2226b2b956b0db110.png?width=264&height=201',
    'https://simg3.gelbooru.com/images/d3/83/d383ca57bdaea779bbb479ca0e30ed96.jpeg',
    'https://danbooru.donmai.us/data/__yakumo_yukari_touhou_drawn_by_mokkori9__4ce1447eff164f8c1550274cb5efc808.jpg',
    'https://konachan.com/image/66fd1ea4e068f3b24f3e1e2323c062f9/Konachan.com%20-%20253748%20anus%20ass%20blue_eyes%20blush%20breasts%20gloves%20group%20headdress%20janna%20lulu%20panties%20petals%20pink_hair%20pussy%20red_eyes%20red_hair%20skirt%20twintails%20underwear.png',
    'https://files.yande.re/image/2dcc1d69b458ea6f264cc998be3b6414/yande.re%20416598%20anal%20ass%20ayako_%28pokemon%29%20breasts%20junou%20nipples%20no_bra%20nopan%20open_shirt%20pantsu%20panty_pull%20penis%20pokemon_dppt%20pussy%20torn_clothes%20uncensored.png',
    'https://images-ext-2.discordapp.net/external/yPyZlq4rMM0vBcEo6V6hgbet83rFIZHBaL7R_j8PQ8s/https/simg3.gelbooru.com/images/c4/b9/c4b9b4b7bea684f11ec3dba55720fd26.jpg?width=133&height=188',
    'https://danbooru.donmai.us/data/__wa2000_girls_frontline_drawn_by_phandit_thirathon__77d3665feca800b17f5d28e712f5d3fd.jpg',
    'https://konachan.com/image/5d9d7aa460430a2515aa3b1555c9f05a/Konachan.com%20-%20253163%20baffu%20black_hair%20blue_eyes%20blush%20breasts%20censored%20cum%20game_cg%20long_hair%20navel%20nipples%20nude%20penis%20pussy%20pussy_juice%20wet%20wonder_fool%20yanagawa_yuuka.png',
    'https://files.yande.re/image/44d1ccc20fa18dd11d76f7bad70b89f9/yande.re%20417830%20animal_ears%20anus%20azur_lane%20bikini%20bottomless%20hammann_%28azurlane%29%20loli%20nedia_r%20nekomimi%20pussy%20swimsuits%20tail%20uncensored.jpg',
    'https://images-ext-1.discordapp.net/external/vQYIIhvlCSFAekUZNVSXI8CQpFQ9tY_rIaw-dQJSNjE/https/simg3.gelbooru.com/images/77/04/770462bc24bc931d41dae60ea7cd528f.jpg?width=144&height=188',
    'https://images-ext-1.discordapp.net/external/0xKSwaNT2bdyp2BCEVrrm2ZccwGsa_JbiehnAS6mxD0/https/konachan.com/image/fe088ea8b24ca09875c63a58ed9730ac/Konachan.com%2520-%2520253109%2520blush%2520breasts%2520brown_hair%2520bubuzuke%2520censored%2520game_cg%2520long_hair%2520navel%2520nipples%2520nude%2520penis%2520pussy%2520red_eyes%2520sex%2520silkys_sakura%2520spread_legs%2520wet%2520wristwear.png?width=300&height=169',
    'https://konachan.com/image/ebc69bc69c0e5c6d10da3274d39d6226/Konachan.com%20-%20253601%20blonde_hair%20blue_eyes%20blush%20breasts%20building%20censored%20cleavage%20clouds%20dark_skin%20long_hair%20penis%20seifuku%20skirt%20sky%20tagme_%28artist%29%20twintails.jpg',
    'https://files.yande.re/image/f6ce5406ce5624043ba5e32cc5d083bf/yande.re%20416961%20censored%20cum%20fate_grand_order%20horns%20lactation%20naked%20nipples%20penis%20pubic_hair%20pussy%20sessyoin_kiara%20sex%20silly%20tattoo%20thighhighs.png',
    'https://images-ext-2.discordapp.net/external/stJZ8Ke0CtQMzQ4NCyLSgPuZQKwK_qKkxWQujPqPEdk/https/files.yande.re/image/00179ed439c6541cce0f8b88fed6a6be/yande.re%2520416965%2520bra%2520lingerie%2520pantsu%2520pussy_juice%2520re_zero_kara_hajimeru_isekai_seikatsu%2520rem_%2528re_zero%2529%2520see_through%2520silly%2520wet.png?width=266&height=188',
    'https://images-ext-1.discordapp.net/external/1E3Fb7on2Q3I3ajcuXOA_knbZN7NaJPB5dJSnrQrfIs/https/konachan.com/image/ea67c2d9fac50851472c161538b2a8a6/Konachan.com%2520-%2520253162%2520animal_ears%2520baffu%2520blush%2520breasts%2520censored%2520game_cg%2520gray_hair%2520long_hair%2520nipples%2520open_shirt%2520penis%2520pussy%2520thighhighs%2520wet%2520wonder_fool%2520yellow_eyes.png?width=300&height=169',
    'https://simg3.gelbooru.com/images/63/0e/630e994c539bc53231627afaddf58656.png',
    'https://konachan.com/image/d3742ee44f457377e91fa5dc8d3b27b2/Konachan.com%20-%20253304%20aqua_eyes%20blush%20breasts%20brown_hair%20censored%20group%20navel%20nipples%20no_bra%20nopan%20pussy%20red_hair%20shinya%20shirobako%20skirt%20thighhighs%20twintails%20yano_erika.png',
    'https://files.yande.re/image/3b1b080d6d8738f8980aa6a4b28136f9/yande.re%20416931%20bikini%20cleavage%20erect_nipples%20open_shirt%20pussy_juice%20sakagami_umi%20seifuku%20skirt_lift%20swimsuits%20underboob%20wet.jpg',
    'https://images-ext-2.discordapp.net/external/ImkvZ4nbLPD6tzNE2AjkI8ZQh_DYsIYIR4zIlM6zY1c/https/danbooru.donmai.us/data/__drawn_by_ohisashiburi__7f329bb72a9306258152629cb65b71ce.jpg?width=208&height=188',
    'https://danbooru.donmai.us/data/__anna_nishikinomiya_kajou_ayame_and_saotome_otome_shimoneta_to_iu_gainen_ga_sonzai_shinai_taikutsu_na_sekai_drawn_by_born_to_die__dde7be573766a2bb05255131309034c5.jpg',
    'https://konachan.com/image/368c13c99b1e5881efca37459684e8aa/Konachan.com%20-%20253799%20ass%20bandage%20barefoot%20blush%20breasts%20cape%20demon%20eyepatch%20glasses%20gloves%20group%20hat%20headband%20horns%20navel%20nipples%20no_bra%20nude%20pumpkin%20pussy%20tail%20wings%20wink.png',
    'https://files.yande.re/image/2050751b6d12662c3425f84cfa234711/yande.re%20417370%20animal_ears%20bandages%20blood%20bondage%20fingering%20loli%20naked_ribbon%20pussy_juice%20tail%20wntame%20yuri.png',
    'https://images-ext-2.discordapp.net/external/1riaS7UrpLCNGo_Us979SF28RJSPZU7zWs4uVMxP60c/https/konachan.com/image/5ee7e1817dc85549a345a544c469f629/Konachan.com%2520-%2520253852%2520anus%2520ass%2520bed%2520breasts%2520ditto%2520fingering%2520long_hair%2520nipples%2520no_bra%2520panties%2520pokemon%2520ponytail%2520pussy%2520sideboob%2520socks%2520speh%2520underwear%2520watermark%2520wink%2520yuri.jpg?width=230&height=188',
    'https://simg3.gelbooru.com/images/0e/22/0e22cf89cab69c33433b6644cd4c36ab.jpg',
    'https://danbooru.donmai.us/data/__yakumo_yukari_touhou_drawn_by_mokkori9__75c3e55290c101c4a76aca2d99d031a9.jpg',
    'https://konachan.com/image/1aa4648d70b249364ecb10aeb7df69c7/Konachan.com%20-%20253447%20ass%20blush%20bow%20breasts%20fate_%28series%29%20fate_stay_night%20hera_%28hara0742%29%20long_hair%20matou_sakura%20nipples%20purple_hair%20sex%20wet.png',
    'https://files.yande.re/image/6fe1c171ee79b129a3927daa0f4edc58/yande.re%20416985%20anus%20ass%20bodysuit%20bondage%20breasts%20censored%20cum%20fate_grand_order%20lactation%20nipples%20no_bra%20nopan%20penis%20pussy%20pussy_juice%20sex%20silly%20torn_clothes.png',
    'https://konachan.com/image/729f3487e924775eb4700be3f574193a/Konachan.com%20-%20253225%20barefoot%20beach%20blonde_hair%20blush%20breasts%20brown_hair%20flowers%20game_cg%20handa_nora%20leaves%20long_hair%20nipples%20oozora_itsuki%20sex%20short_hair%20tree%20water%20wet.png',
    'https://files.yande.re/image/c1d893bf592a845e6d56b1da0b325512/yande.re%20418168%20animal_ears%20horns%20league_of_legends%20naked%20nipples%20pussy%20sakimichan%20soraka%20thighhighs%20uncensored%20weapon%20wings.jpg',
    'https://images-ext-2.discordapp.net/external/7VsrfCIffMPtNxvflDokQzgCa2jDVwdv4M2frHIjs9U/https/konachan.com/image/d4d556071d7cf2619b846a26ac95bb3e/Konachan.com%2520-%2520253594%2520ass%2520breasts%2520close%2520game_cg%2520jirou_%2528chekoro%2529%2520natsuiro_otome%2520nipples%2520pussy_juice%2520skirt%2520tagme_%2528character%2529%2520underwear%2520upskirt%2520vibrator%2520wet.jpg?width=250&height=188',
    'https://images-ext-1.discordapp.net/external/p8wX_3j4LRL823iRnXyHoIlK3D8zkF69b4Jxoyxgsxc/https/konachan.com/image/c48b156d5c0c1663c47b4723becd108a/Konachan.com%2520-%2520253288%2520anal%2520animal%2520ass%2520bat%2520black_hair%2520breasts%2520censored%2520halloween%2520horns%2520long_hair%2520mogu%2520moon%2520nipples%2520nude%2520original%2520pumpkin%2520purple_eyes%2520pussy%2520tail%2520thighhighs.png?width=273&height=188',
    'https://konachan.com/image/81887a167a92e2618ff875448b004543/Konachan.com%20-%20253342%20ass%20breasts%20brown_eyes%20chain%20cum%20gloves%20gray_hair%20green_eyes%20headband%20jack_dempa%20long_hair%20male%20military%20open_shirt%20twintails%20uniform%20white_hair.png',
    'https://files.yande.re/image/22369745d48d295329c87eaa2b30cc7a/yande.re%20416622%20bikini%20breast_grab%20breasts%20cum%20fate_grand_order%20garter%20hews%20maid%20nipples%20panty_pull%20saber%20saber_alter%20sex%20swimsuits.png',
    'https://images-ext-1.discordapp.net/external/Foy_hzvc-wTN5LeTpAxV1pcATmPvRYb8klAHMIMibMc/https/danbooru.donmai.us/data/__d_va_d_va_the_destroyer_mercy_and_witch_mercy_blizzard_company_heroes_of_the_storm_and_overwatch_drawn_by_sexgazer__370734ae89f5969d079d4b542365191f.jpg?width=277&height=188',
    'https://danbooru.donmai.us/data/__oyashio_kantai_collection_drawn_by_ebifurya__c77ff03f4afc71336a0099b45db6dd3d.jpg',
    'https://files.yande.re/image/ba3a5a7f692b5a358b0070e176db8de5/yande.re%20418173%20christmas%20lingerie%20nipples%20open_shirt%20pantsu%20pubic_hair%20pussy_juice%20seifuku%20shiokonbu%20thighhighs.jpg',
    'https://danbooru.donmai.us/data/__original_drawn_by_sasana__d03b638079072e0f1c14091cced742c1.jpg',
    'https://konachan.com/image/808197960004c7272780cf5c4bd535cc/Konachan.com%20-%20253229%20ass%20beach%20braids%20breasts%20clouds%20game_cg%20harukaze_soft%20long_hair%20nipples%20nude%20oozora_itsuki%20pussy_juice%20red_eyes%20sex%20sky%20twintails%20water%20white_hair.png',
    'https://files.yande.re/image/8433e742382262668b65d28fa976ecdf/yande.re%20416467%20acerola_(pokemon)%20breasts%20dress%20loli%20nipples%20no_bra%20nopan%20pokemon_sm%20pussy%20skirt_lift%20snowcanvas.png',
    'https://danbooru.donmai.us/data/__original_drawn_by_sasana__5ea9b67418d24f976d4dd743ec97916f.jpg',
    'https://konachan.com/image/01a6215b126a57010124727d413f7e5b/Konachan.com%20-%20253865%20animal_ears%20anus%20ass%20azur_lane%20bed%20blue_eyes%20long_hair%20niiyamuneko%20pussy%20ribbons%20skirt%20tagme_(character)%20thighhighs%20uncensored%20white_hair.png',
    'https://files.yande.re/image/da3b3dab3e060634bf81b73ef6be45a7/yande.re%20416792%20anal_beads%20breasts%20heels%20horns%20nipples%20no_bra%20tail%20thighhighs%20torn_clothes%20wings%20zombie-andy.png',
    'https://images-ext-2.discordapp.net/external/mAkPYYorqWGJj3cA1w9JS__RpTTRtuSn8vXXkxHcsNU/https/files.yande.re/image/f27b64be373aefc8f0fa17b201da4bd0/yande.re%2520417378%2520hiryuu_%2528kancolle%2529%2520kaga_%2528kancolle%2529%2520kantai_collection%2520kusaka_souji%2520naked%2520nipples%2520pubic_hair%2520shota%2520souryuu_%2528kancolle%2529%2520zuikaku_%2528kancolle%2529.jpg?width=264&height=188',
    'https://images-ext-1.discordapp.net/external/pHFEWUF0R4ctKbinS2o703a2Zume8HQD887AsKLP80E/https/files.yande.re/image/e21b788475e3e526f533e9e7b0ab0c3f/yande.re%2520418166%2520ahri%2520animal_ears%2520league_of_legends%2520naked%2520nipples%2520pussy%2520sakimichan%2520tail%2520thighhighs%2520uncensored.jpg?width=132&height=188',
    'https://danbooru.donmai.us/data/__ayase_eli_and_yazawa_nico_love_live_and_love_live_school_idol_project_drawn_by_maruze_circus__73b0538a620ba2120578923ade0be70e.png',
    'https://konachan.com/image/af63d1d1718c9a60fdea2dfe3777067f/Konachan.com%20-%20253085%20blush%20breasts%20brown_hair%20bubuzuke%20camera%20censored%20game_cg%20long_hair%20male%20navel%20nipples%20nude%20penis%20pubic_hair%20pussy%20red_eyes%20sex%20spread_legs%20wet.png',
    'https://files.yande.re/image/1eecbc7aa517cfaa1a1f4f750dbfc83e/yande.re%20416823%20arturia_pendragon_(lancer)%20censored%20cum%20fate_grand_order%20lactation%20naked%20nipples%20penis%20pubic_hair%20pussy%20sex%20silly%20wet.png',
    'https://simg3.gelbooru.com/images/33/6c/336cc297a7e5c0e427ffa3023b8067d4.jpg',
    'https://danbooru.donmai.us/data/__ruler_and_sieg_fate_apocrypha_and_fate_series_drawn_by_sanae_gomez__f814f83f1a738e60156d7bfe50645f08.png',
    'https://konachan.com/image/fc9b48a18c22d7705179f172c32f003f/Konachan.com%20-%20253298%20blush%20breast_grab%20breasts%20brown_hair%20censored%20hibike!_euphonium%20nipples%20oumae_kumiko%20penis%20seifuku%20sex%20shinya%20short_hair%20skirt%20yellow_eyes.jpg',
    'https://files.yande.re/image/e4e9dbc824483060abdde910dbac9ae9/yande.re%20417042%20bikini%20cleavage%20fate_grand_order%20handjob%20maid%20momio%20open_shirt%20penis%20saber%20saber_alter%20saber_extra%20skirt_lift%20swimsuits%20uncensored.jpg',
    'https://konachan.com/image/9362b3bbb111795546660d5dab6a114d/Konachan.com%20-%20253283%20[joosi]%20blue_hair%20blush%20breasts%20chain%20collar%20fenrir%20long_hair%20nipples%20nude%20penis%20pubic_hair%20pussy%20red_eyes%20sex%20signed%20tattoo%20uncensored%20wolfgirl.png',
    'https://images-ext-2.discordapp.net/external/cTpfcfaL3zI7n4v8DQ3sbwNfcY9Yo4CMAYa-NEAd28w/https/files.yande.re/image/c45a9ad1572e6aa3d049c915294943b2/yande.re%2520416820%2520areola%2520cameltoe%2520fate_grand_order%2520nipple_slip%2520nipples%2520pussy_juice%2520saber_extra%2520silly%2520sling_bikini%2520swimsuits%2520wet.png?width=133&height=188',
    'https://danbooru.donmai.us/data/__shielder_fate_grand_order_and_fate_series_drawn_by_yanochi__c1c415b23f441dbd6d65658b18984b6f.png',
    'https://konachan.com/image/aac423b78cea79c0965e7ffbc5f7f7de/Konachan.com%20-%20253083%20blush%20breasts%20brown_hair%20bubuzuke%20censored%20game_cg%20long_hair%20navel%20nipples%20nude%20penis%20pubic_hair%20pussy%20red_eyes%20sex%20silkys_sakura%20spread_legs.png',
    'https://files.yande.re/image/5702e730ac44fb02e14e5bc546b1c623/yande.re%20416943%20censored%20fate_grand_order%20ishtar_(fate_grand_order)%20naked%20nipples%20pussy%20silly%20toosaka_rin.png',
    'https://konachan.com/image/c645593be602fe46e23ac29b51c0aa79/Konachan.com%20-%20253078%20apron%20blush%20breast_grab%20breasts%20brown_hair%20bubuzuke%20censored%20game_cg%20long_hair%20naked_apron%20nipples%20nude%20pubic_hair%20pussy%20red_eyes%20sex%20spread_legs%20wet.png',
    'https://files.yande.re/image/66fd1ea4e068f3b24f3e1e2323c062f9/yande.re%20417048%20anus%20ass%20bottomless%20cameltoe%20heels%20jinx%20liang_xing%20nipples%20nopan%20pantsu%20panty_pull%20pussy%20pussy_juice%20seifuku%20thighhighs%20thong%20topless%20uncensored.png',
    'https://simg3.gelbooru.com/images/a8/32/a8322c33149263f589a48164d434a16b.jpg',
    'https://konachan.com/image/434ef9b3e7cd9e412207960edc48161b/Konachan.com%20-%20253881%20breasts%20fate_grand_order%20fate_(series)%20nipples%20sex%20tohsaka_rin%20twinameless.jpg',
    'https://files.yande.re/image/932a4a8f1d3c4aa62d0a86a81662f4a3/yande.re%20416556%20anus%20censored%20game_cg%20harukaze-soft%20kuroki_michi%20nipples%20nopan%20nora_to_oujo_to_noraneko_heart_2%20oozora_itsuki%20pussy%20pussy_juice%20thighhighs%20topless.png',
    'https://danbooru.donmai.us/data/__ruby_rose_rwby_drawn_by_cyber_cyber_knight__141e18c545922e7c9f749a7a9af36241.jpg',
    'https://konachan.com/image/7ce957f36ac1a855ab5487b1274adc23/Konachan.com%20-%20253209%20anthropomorphism%20blush%20breast_hold%20breasts%20brown_hair%20cum%20gloves%20kantai_collection%20lolicept%20noshiro_(kancolle)%20paizuri%20pubic_hair%20torn_clothes%20wink.jpg',
    'https://files.yande.re/image/012080c8b9ceb9cc7748e07e4702b7d7/yande.re%20418128%20bandages%20breasts%20censored%20fate_apocrypha%20fate_grand_order%20fate_stay_night%20horns%20nipples%20no_bra%20nopan%20open_shirt%20pussy%20see_through%20ten_no_hoshi.jpg',
    'https://simg3.gelbooru.com/images/8a/2b/8a2bffe4977913094a5de2d141b4a0b6.png',
    'https://danbooru.donmai.us/data/__kurano_ema_kurano_kun_chi_no_futago_jijou_drawn_by_kanekiyo_miwa__859de44d2e9b4bdf95a827072a78cd70.jpg',
    'https://konachan.com/image/ea1485780739de337b36b4e8cab0b5c9/Konachan.com%20-%20253069%20anal%20blush%20breasts%20dark_skin%20dildo%20game_cg%20gray_eyes%20long_hair%20masturbation%20nipples%20pussy%20red_hair%20thighhighs%20uncensored%20wanaca%20winged_cloud.png',
    'https://files.yande.re/image/ad5b60b403db0f7ef55fbc9d6509ebb7/yande.re%20418190%20bondage%20breasts%20censored%20ddism%20feet%20kawashiro_nitori%20mecha%20nipples%20no_bra%20pantsu%20panty_pull%20torn_clothes%20touhou%20undressing.jpg',
    'https://danbooru.donmai.us/data/__original_drawn_by_gen_genetrix__1a9a562371f6826097b498810a32842d.jpg',
    'https://konachan.com/image/78d0ec693c1be7e1350350e120c5cbf4/Konachan.com%20-%20253397%20blonde_hair%20blush%20bow%20breasts%20condom%20cum%20kawakami_mai%20kneehighs%20long_hair%20phone%20ponytail%20ribbons%20seifuku%20skirt%20takeda_hiromitsu.jpg',
    'https://files.yande.re/image/cf28b792ab76b41d56b17f26d4c96ba2/yande.re%20417769%20aoin%20bikini%20cameltoe%20cum%20erect_nipples%20fate_grand_order%20florence_nightingale_(fate_grand_order)%20heels%20stockings%20swimsuits%20thighhighs.jpg',
    'https://simg3.gelbooru.com/images/14/c5/14c588ee3dc4c4dee1fafa4bffcce527.jpg',
    'https://danbooru.donmai.us/data/__atago_azur_lane_drawn_by_ero_waifu__e079836b435a73f4bf78cb72be1356d3.png',
    'https://konachan.com/image/3d4e6028a59d0cffbcd5a6b2a263d179/Konachan.com%20-%20253297%20anal%20anus%20ass%20blush%20breast_grab%20breasts%20brown_eyes%20brown_hair%20censored%20nipples%20panties%20penis%20pussy%20seifuku%20sex%20shinya%20short_hair%20underwear.jpg',
    'https://files.yande.re/image/eae274879de653540e24539e9f19081b/yande.re%20416852%20azur_lane%20cum%20garter%20naked%20pantsu%20panty_pull%20prinz_eugen_(azur_lane)%20pussy%20string_panties%20tagme.jpg',
    'https://danbooru.donmai.us/data/__izumi_koushirou_tachikawa_mimi_and_yagami_taichi_digimon_and_digimon_adventure_tri_drawn_by_junou__c446d6570306e4754723dd138f965c1c.png',
    'https://konachan.com/image/fed33978d97bf796e9e0e89e73e459c1/Konachan.com%20-%20253689%20anus%20ass%20blue_eyes%20blush%20breasts%20fingering%20game_cg%20green_eyes%20halloween%20long_hair%20nipples%20nude%20pussy%20tail%20thighhighs%20uncensored%20wanaca%20white%20yuri.png',
    'https://files.yande.re/image/93f45d1156bc136f25fb6afe4eb8ad1d/yande.re%20416605%20cum%20nipples%20oroneko%20pantyhose%20seifuku%20skirt_lift%20tagme%20topless%20torn_clothes.jpg',
    'https://simg3.gelbooru.com/images/c3/91/c391af3df97d881548d0421c39dd8556.png',
    'https://danbooru.donmai.us/data/__ahri_league_of_legends_drawn_by_ero_waifu__14dfe5aaeb01cfc06477351e05ec70a1.png',
    'https://konachan.com/image/f63a5e329a9b4958c0e35d261281f30d/Konachan.com%20-%20253075%20bed%20black_hair%20blush%20breasts%20brown_eyes%20bubuzuke%20game_cg%20kiss%20long_hair%20male%20nipples%20no_bra%20nopan%20panties%20ponytail%20red_eyes%20sex%20underwear%20yuri.png',
    'https://files.yande.re/image/8f3da29410fe8cc27f9b0f752cb436b5/yande.re%20417060%20final_fantasy%20final_fantasy_vii%20liang_xing%20naked%20nipples%20pussy%20tifa_lockhart%20uncensored.png',
    'https://danbooru.donmai.us/data/__original_drawn_by_gen_genetrix__3d3bd7719a194e702a8b1e769d935ecd.jpg',
    'https://konachan.com/image/e6f5d13737b61a4c399e4adddd8add0e/Konachan.com%20-%20253100%20anus%20ass%20breasts%20bubuzuke%20censored%20cum%20game_cg%20gloves%20long_hair%20male%20nipples%20panties%20penis%20red_eyes%20sex%20sideboob%20thighhighs%20topless%20underwear.png',
    'https://files.yande.re/image/44c74e3455e938d46ae90f8851ba0521/yande.re%20416862%20anus%20breasts%20censored%20fate_extra%20fate_extra_ccc%20fate_stay_night%20feet%20nipples%20no_bra%20nopan%20open_shirt%20pussy%20see_through%20silly%20thighhighs.png',
    'https://danbooru.donmai.us/data/__saber_extra_fate_grand_order_and_fate_series_drawn_by_taku_user_nxgk7748__4aeec4feff06053492a5495678aa7fd1.png',
    'https://konachan.com/image/0f44de8e4ac0bb7a80d02944a91f4085/Konachan.com%20-%20253339%20azur_lane%20blush%20breasts%20brown_hair%20fang%20foxgirl%20gloves%20hakumare%20long_hair%20nipples%20pussy%20pussy_juice%20red_eyes%20skirt%20tail%20thighhighs%20uncensored.png',
    'https://files.yande.re/image/0bf382a179e7fefea4b1b30341c69cb6/yande.re%20416559%20animal_ears%20breasts%20bunny_ears%20cum%20fishnets%20heels%20lingerie%20nekomimi%20nipples%20pussy_juice%20see_through%20tail%20takeda_hiromitsu%20thighhighs%20thong.jpg',
    'https://simg3.gelbooru.com/images/64/40/6440ad23a9cbf5922b21a1e7efe6ccad.jpeg',
    'https://konachan.com/image/c6b694832582a02a37999da1fd812d36/Konachan.com%20-%20253066%20ass%20blush%20breasts%20dark_skin%20game_cg%20gray_eyes%20long_hair%20nipples%20pussy%20red_hair%20spread_legs%20thighhighs%20uncensored%20wanaca%20winged_cloud.png',
    'https://files.yande.re/image/3e6314116558ff934d86139b2cf92d52/yande.re%20416816%20bodysuit%20breast_grab%20censored%20cum%20fate_grand_order%20nipples%20no_bra%20nopan%20penis%20pubic_hair%20pussy%20pussy_juice%20silly%20thighhighs%20torn_clothes.png',
    'https://danbooru.donmai.us/data/__ebihara_naho_idolmaster_idolmaster_cinderella_girls_and_original_drawn_by_hisakawa_chin__2361de4406eeff5ca8cb839eed9429eb.jpg',
    'https://konachan.com/image/2eb8e07ee7d797494b10ee592760d547/Konachan.com%20-%20253272%20[joosi]%20anus%20ass%20blue_hair%20blush%20bondage%20breasts%20fenrir%20long_hair%20nipples%20nude%20pussy%20red_eyes%20shackles%20signed%20tail%20tattoo%20uncensored%20wolfgirl.png',
    'https://files.yande.re/image/6cfbb75c64dfc611eeaa96f90603c0e3/yande.re%20416715%20azur_lane%20censored%20cum%20feet%20footjob%20garter%20nipples%20panty_pull%20penis%20prinz_eugen_(azur_lane)%20swimsuits%20tagme%20topless.jpg',
    'https://danbooru.donmai.us/data/__rance_and_sill_plain_alicesoft_rance_series_and_sengoku_rance_drawn_by_orion_orionproject_and_sengoku__46a3dd4b906716c81b2a21abe1137a3b.jpg',
    'https://konachan.com/image/07516a621c62a03e019bbeb9400a4551/Konachan.com%20-%20253885%20animal_ears%20blonde_hair%20blush%20breasts%20game_cg%20long_hair%20nipples%20nude%20pussy%20pussy_juice%20red_eyes%20thighhighs%20uncensored%20vibrator%20wanaca%20winged_cloud.png',
    'https://files.yande.re/image/5393de0bb35fcfede67c7fb2352ce762/yande.re%20416964%20censored%20cum%20fellatio%20hamakaze_(kancolle)%20kantai_collection%20masturbation%20naked%20nipples%20penis%20silly.png',
    'https://danbooru.donmai.us/data/__shielder_fate_grand_order_and_fate_series_drawn_by_yanochi__059dda494b83281299bfdc5abfff6599.png',
    'https://konachan.com/image/e6b4d428d0623c65ecc75a68df9e94bf/Konachan.com%20-%20253873%20bed%20breasts%20brown_hair%20dark_skin%20demon%20green_eyes%20horns%20long_hair%20navel%20nipples%20nude%20pussy%20tagme_(artist)%20uncensored%20watermark%20white_hair%20yellow_eyes.png',
    'https://konachan.com/image/32620a77d27e3b3684b9e65c32e3c62b/Konachan.com%20-%20253876%20aqua_eyes%20aqua_hair%20blush%20breasts%20censored%20ddism%20kawashiro_nitori%20navel%20nipples%20panties%20short_hair%20torn_clothes%20touhou%20underwear%20white.jpg',
    'https://files.yande.re/image/8f0c5c6262b37dde2f91eb076369672b/yande.re%20416933%20anus%20ass%20cum%20fellatio%20monochrome%20pantsu%20pubic_hair%20pussy%20pussy_juice%20sakagami_umi%20seifuku%20skirt_lift%20thong%20topless%20uncensored.jpg',
    'https://files.yande.re/image/6a286644ec507d51dc0142d6f901ce52/yande.re%20418121%20halloween%20heels%20mercy_(overwatch)%20naked%20nipples%20overwatch%20sakimichan%20thighhighs%20wings.jpg',
    'https://simg3.gelbooru.com/images/14/df/14dfe5aaeb01cfc06477351e05ec70a1.png',
    'https://danbooru.donmai.us/data/__2917922__d1cede3527eb3b17a624c14926631a74.jpg',
    'https://konachan.com/image/2ff14de0a3f42f5fe2550a993aeb8f29/Konachan.com%20-%20253507%203-nin_iru!%20animal_ears%20anus%20aqua_eyes%20ass%20blonde_hair%20blush%20bunny_ears%20game_cg%20long_hair%20pantyhose%20photoshop%20pussy%20ribbons%20riffraff%20uncensored%20wet.png',
    'https://files.yande.re/image/90c0ee096da82521194c76bc675954bb/yande.re%20416811%20admiral_(kancolle)%20bosshi%20cum%20kantai_collection%20loli%20naked%20nipples%20penis%20pussy%20shimakaze_(kancolle)%20thighhighs.png',
    'https://danbooru.donmai.us/data/__osakabe_hime_fate_grand_order_and_fate_series_drawn_by_arsenal__de4957a63e4fd9340bb053730274514b.jpg',
    'https://konachan.com/image/15bfd25a5b8b2b52d335fd8ab0eac008/Konachan.com%20-%20253306%20ass%20blue_hair%20blush%20breast_hold%20breasts%20censored%20cum%20imai_midori%20long_hair%20nipples%20paizuri%20pantyhose%20penis%20ponytail%20pubic_hair%20shinya%20shirobako.png',
    'https://files.yande.re/image/eca0d12f487b47013db82c030ea39883/yande.re%20416678%20feet%20loli%20naked%20nipples%20pussy%20tagme%20uncensored.jpg',
    'https://simg3.gelbooru.com/images/fb/8e/fb8e04d5cc6b7cdb09c335e83828810d.png',
    'https://danbooru.donmai.us/data/__original_drawn_by_piston_ring__89e5b22a9d4a235d73e75945d3b16054.jpg',
    'https://konachan.com/image/ea662ee9db19d56d07a11e57d5a6986a/Konachan.com%20-%20253107%20anus%20black_hair%20bra%20breasts%20bubuzuke%20censored%20fingering%20game_cg%20male%20navel%20nipples%20panties%20ponytail%20pussy%20pussy_juice%20short_hair%20underwear.png',
    'https://files.yande.re/image/9d5f4523ba095a3aba5be03ef5cd12b4/yande.re%20416963%20breast_grab%20censored%20cum%20hamakaze_(kancolle)%20kantai_collection%20naked%20nipples%20paizuri%20penis%20silly.png',
    'https://konachan.com/image/b3930db7fa906b495d08cedde7337ea2/Konachan.com%20-%20253521%20barefoot%20beach%20blonde_hair%20breasts%20cait%20clouds%20cum%20green_eyes%20handjob%20long_hair%20nipples%20nude%20penis%20saber%20saber_extra%20sky%20twintails%20uncensored.png',
    'https://files.yande.re/image/eacd0ff9d7d8c0dbad412224c940f482/yande.re%20416821%20anus%20censored%20fate_grand_order%20naked%20nipples%20pussy%20saber_extra%20silly.png',
    'https://konachan.com/image/a9dee74b4ea55ae7d65370532afc876e/Konachan.com%20-%20253299%20anal%20anus%20ass%20blush%20breast_grab%20breasts%20brown_eyes%20brown_hair%20censored%20cum%20nipples%20panties%20penis%20pussy%20seifuku%20sex%20shinya%20short_hair%20underwear%20wink.jpg',
    'https://simg3.gelbooru.com/images/13/68/1368bb426067c0cd36f3bf92be3e328a.png',
    'https://danbooru.donmai.us/data/__kizuna_ai_a_i_channel_drawn_by_glo_s_s__75b713a01c7c1f76cd889a74154a293f.png',
    'https://konachan.com/image/27801ec2d5fc188713892af21c5c8689/Konachan.com%20-%20253351%20anal%20ass%20book%20bra%20breasts%20green_eyes%20kozue_akari%20masturbation%20nipples%20original%20pussy%20pussy_juice%20red_hair%20short_hair%20uncensored%20underwear%20waifu2x.png',
    'https://files.yande.re/image/422942562918061a6e1577f64825bae7/yande.re%20416947%20cum%20fate_grand_order%20horns%20kiyohime_(fate_grand_order)%20naked%20tagme%20thighhighs.jpg',
    'https://konachan.com/image/f46fb21aea2acb26431a6bdb4905b106/Konachan.com%20-%20253242%202girls%20aqua_eyes%20barefoot%20blush%20breasts%20fingering%20game_cg%20horns%20long_hair%20nipples%20phone%20pool%20pussy%20short_hair%20tattoo%20uncensored%20wanaca%20wink%20yuri.png',
    'https://files.yande.re/image/bb7865097a76d02e802850b57023d78b/yande.re%20416606%20bra%20breast_hold%20breasts%20cum%20dress%20halloween%20horns%20nipples%20open_shirt%20pantsu%20tagme%20tail%20thighhighs%20wings%20witch.jpg',
    'https://simg3.gelbooru.com/images/db/15/db153c1542197fd72ad15810a345a4dd.jpeg',
    'https://files.yande.re/image/2c5573dc184acc46f043fc720c43ebf3/yande.re%20416814%20bodysuit%20censored%20fate_grand_order%20nipples%20no_bra%20nopan%20pubic_hair%20pussy%20scathach_(fate_grand_order)%20silly%20thighhighs%20torn_clothes.png'
    ]

def hentairead(sq):
    c.execute(sq)
    conn.commit()
    global hendata
    hendata = c.fetchall()

def addhen(seq):
    c.execute(seq)
    conn.commit()

@client.command(pass_context = True)
async def hentai(ctx):
    server_id = ctx.message.server.id
    sq = "SELECT COUNT(*), nsfw_is_enabled, server_id FROM Permissions WHERE server_id = '" + server_id + "'"
    seq = "INSERT INTO Permissions(nsfw_is_enabled, server_id) VALUES (0, '" + server_id + "')"
    hentairead(sq)
    if hendata[0][0] < 1:
        embed = discord.Embed(description = "NSFW is disabled!", color = 0xFF0000)
        await client.say(embed = embed)
        addhen(seq)
    elif hendata[0][0] > 0:
        if hendata[0][1] < 1:
            embed = discord.Embed(description = "NSFW is disabled!", color = 0xFF0000)
            await client.say(embed = embed)
        elif hendata[0][1] > 0: 
            embed = discord.Embed(description = "Here's your hentai, " + ctx.message.author.mention + "!", color = embed_color)
            embed.set_image(url = random.choice(hentai_images))
            await client.say(embed = embed)
            print(Fore.CYAN + "Command Successfully Executed |\n       Command Ran In:[" + ctx.message.server.id + "]\n       User:[" + ctx.message.author.id + "]\n       Channel:[" + ctx.message.channel.id + "]")

########################################################## N S F W ##########################################################




client.run(BotToken)
