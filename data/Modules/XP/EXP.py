import discord
from discord.ext import commands
import sqlite3
from credentials import EmbedColor as embed_color
from credentials import Owners as owner
import asyncio
import time
import datetime

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()



class EXP():
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context =  True, aliases=['prof'])
    async def profile(self, ctx, *, user: str):
        def profs(getxps):
            c.execute(getxps)
            conn.commit()
            global data
            data = c.fetchall()

        def selfprofs(getselfprof):
            c.execute(getselfprof)
            conn.commit()
            global selfdata
            selfdata = c.fetchall()

        user_id = ctx.message.author.id
        user_name = ctx.message.author.name
        level = "0"
        description = "A very empty description :^)"
        reputation = "0"
        currency = "100"
        exp = "0"
        '''getxp = "SELECT * FROM UserData WHERE user_name = '" + user + "'"'''
        getxps = "SELECT COUNT(*), user_id, user_name, level, exp, description, reputation, currency FROM UserData WHERE user_name = '" + user + "'"
        getselfprof = "SELECT COUNT(*), user_id, user_name, level, exp, description, reputation, currency FROM UserData WHERE user_id = '" + ctx.message.author.id + "'"
        profs(getxps)
        if data[0][0] < 1:
            selfprofs(getselfprof)
            embed = discord.Embed(title = ctx.message.author.name+"'s EXP stats", description = "I did not find " + str(user) + "'s EXP stats.\nI will show yours instead.", color = embed_color)
            embed.add_field(name = "User ID", value=selfdata[0][1], inline=False)
            embed.add_field(name = "User Name", value=selfdata[0][2], inline=False)
            embed.add_field(name="Level", value=selfdata[0][3], inline=True)
            embed.add_field(name="EXP", value=selfdata[0][4], inline=True)
            embed.add_field(name="Description", value=selfdata[0][5], inline=True)
            embed.add_field(name="Reputation", value=selfdata[0][6], inline=True)
            embed.add_field(name="Currency", value=selfdata[0][7], inline=True)
            embed.set_footer(text=ctx.message.author)
            await self.client.say(embed = embed)
        elif data[0][0] > 0:
            embed = discord.Embed(title = user+"'s EXP stats", color = embed_color)
            embed.add_field(name = "User ID", value=data[0][1], inline=False)
            embed.add_field(name = "User Name", value=data[0][2], inline=False)
            embed.add_field(name="Level", value=data[0][3], inline=True)
            embed.add_field(name="EXP", value=data[0][4], inline=True)
            embed.add_field(name="Description", value=data[0][5], inline=True)
            embed.add_field(name="Reputation", value=data[0][6], inline=True)
            embed.add_field(name="Currency", value=data[0][7], inline=True)
            embed.set_footer(text=ctx.message.author)
            await self.client.say(embed = embed)

    @commands.command(pass_context = True, aliases=['givcur'])
    async def givecurrency(self, ctx, user: str, currency: str):
        def gibcur(sqll):
            c.execute(sqll)
            conn.commit()
            global data
            data = c.fetchall()

        if ctx.message.author.id != owner:
            embed = discord.Embed(desciption = "Not the owner!", color = 0xFF0000)
            await self.client.say(embed = embed)
        else:
            sqll = "UPDATE UserData SET currency = '" + currency + "' WHERE user_name = '" + user + "'"
            gibcur(sqll)
            embed = discord.Embed(description = "Gave " + user + ", **" + currency + "** currency!", color = embed_color)
            await self.client.say(embed = embed)


    @commands.command(pass_context = True, aliases=['rep'])
    async def giverep(self, ctx, user: str, rep: str):
        def gibrep(sqll):
            c.execute(sqll)
            conn.commit()
            global data
            data = c.fetchall()
        sqll = "UPDATE UserData SET reputation = '" + rep + "' WHERE user_name = '" + user + "'"
        if ctx.message.author.id != owner:
            embed = discord.Embed(description = "You are not the bot owner!", color = 0xFF0000)
            await self.client.say(embed = embed)
        else:
            gibrep(sqll)
            embed = discord.Embed(description = ctx.message.author.mention + ", you gave: " + user + ", \n**" + rep + "**, reputation!", color = embed_color)
            await self.client.say(embed = embed)



    @commands.command(pass_context = True, aliases=['setdesc'])
    async def setdescription(self, ctx, *, desc: str):

        def updatedesc(de):
            c.execute(de)
            conn.commit()

        def toolongdesc(de2):
            c.execute(de2)
            conn.commit()

        user_id = ctx.message.author.id
        tlngdesc = "Description too long."
        de = "UPDATE UserData SET description = '" + desc + "' WHERE user_id = '" + user_id + "'"
        de2 = "UPDATE UserData SET description = '" + tlngdesc + "' WHERE user_id = '" + user_id + "'"
        if len(desc) > 100:
            toolngdesc(de2)
            embed = discord.Embed(description = "Your description is too long!", color = 0xF00000)
            await self.client.say(embed = embed)
        elif len(desc) < 100:
            updatedesc(de)
            embed = discord.Embed(description = "Updated your description to: **" + desc + "**", color = embed_color)
            await self.client.say(embed = embed)

    @commands.command(pass_context = True)
    async def chrlngtcnter(self, ctx, *, chrs: str):
        embed = discord.Embed(title = "Calculate the character lenght of your sentence!", description = "The character lenght of: \n```" + chrs + "```is: ```" + str(len(chrs)) + "```", color = embed_color)
        await self.client.say(embed = embed)

def setup(client):
    client.add_cog(EXP(client))
