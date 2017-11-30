import discord
from discord.ext import commands
import sqlite3
import os
import json
import aiohttp
import asyncio
from credentials import EmbedColor as embed_color
from credentials import Owners as owner
from credentials import Prefix as prefix

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

class GiXP():
    def __init__(self, client):
        self.client = client


    async def on_message(self, message):
        
        def givexp(givexpstr):
            c.execute(givexpstr)
            conn.commit()

        def getcrntxp(getcrnt):
            c.execute(getcrnt)
            conn.commit()
            global crntxp
            crntxp = c.fetchall()

        def levelup(levelupstr):
            c.execute(levelupstr)
            conn.commit()

        def resetxp(resetxpstr):
            c.execute(resetxpstr)
            conn.commit()

        def hasxp(hsxp):
            c.execute(hsxp)
            conn.commit()
            global xpdata
            xpdata = c.fetchall()

        def allxpstats(asxp):
            c.execute(asxp)
            conn.commit()
            global xpstats
            xpstats = c.fetchall()


        hsxp = "SELECT COUNT(*) FROM UserData WHERE user_id = '" + message.author.id + "'"
        hasxp(hsxp)
        if xpdata[0][0] > 0:
            asxp = "SELECT * FROM UserData WHERE user_id = '" + message.author.id + "'"
            allxpstats(asxp)
            if int(xpstats[0][3]) == 100:
                lvlup = int(xpstats[0][2]) + 1
                levelupstr = "UPDATE UserData SET level = '" + str(lvlup) + "' WHERE user_id = '" + message.author.id + "'"
                levelup(levelupstr)
                resetxpstr = "UPDATE UserData SET exp = '" + "0" + "' WHERE user_id = '" + message.author.id + "'"
                resetxp(resetxpstr)
                embed = discord.Embed(description = message.author.mention + " you are now level " + str(lvlup) + "!", color = embed_color)
                await self.client.send_message(message.channel, embed = embed)
            elif int(xpstats[0][3]) != 100:
                newxp = int(xpstats[0][3]) + 2
                givexpstr = "UPDATE UserData SET exp = '" + str(newxp) + "' WHERE user_id = '" + message.author.id + "'"
                await asyncio.sleep(2)
                givexp(givexpstr)
                print("Awarded 2 EXP to " + message.author.name + "!")
        elif xpdata[0][0] < 1:
            print("This user does not have EXP stats!")

def setup(client):
    client.add_cog(GiXP(client))