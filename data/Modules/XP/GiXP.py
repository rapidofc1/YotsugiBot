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
        def givexp(givxp):
            c.execute(givxp)
            conn.commit()

        def getcrntxp(getcrnt):
            c.execute(getcrnt)
            conn.commit()
            global crntxp
            crntxp = c.fetchall()

        def getcrntlvl(gclvl):
            c.execute(gclvl)
            conn.commit()
            global crntlvl
            crntlvl = c.fetchall()

        def levelup(lvl):
            c.execute(lvl)
            conn.commit()

        def resetxp(rxp):
            c.execute(rxp)
            conn.commit()


        getcrnt = "SELECT exp FROM UserData WHERE user_id = '" + message.author.id + "'"
        getcrntxp(getcrnt)
        if int(crntxp[0][0]) is 100:
            gclvl = "SELECT level FROM UserData WHERE user_id = '"  + message.author.id + "'"
            getcrntlvl(gclvl)
            zero = "0"
            lvlup = str(int(crntlvl[0][0]) + 1)
            lvl = "UPDATE UserData SET level = '" + lvlup + "' WHERE user_id = '" + message.author.id + "'"
            rxp = "UPDATE UserData SET exp = '" + zero + "' WHERE user_id = '" + message.author.id + "'"
            levelup(lvl)
            resetxp(rxp)
            print(str(message.author) + " leveled up! They are now: " + str(lvlup) + "!")
            embed = discord.Embed(description = message.author.mention + " you are now level `" + str(lvlup) + "`!\nCheck your XP with `" + prefix + "prof " + message.author.name + "`!", color = embed_color)
            await self.client.send_message(message.channel, embed = embed)
        else:
            await asyncio.sleep(600)
            wtfxp = crntxp[0][0]
            nrexp= int(wtfxp) + 1
            givxp = "UPDATE UserData SET exp = '" + str(nrexp) + "' WHERE user_id = '" + message.author.id + "'"
            givexp(givxp)
            print("Awarded XP to " + str(message.author) + "!")

def setup(client):
    client.add_cog(GiXP(client))