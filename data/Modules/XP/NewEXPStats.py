import discord
from discord.ext import commands
from credentials import Owners as owner
from credentials import EmbedColor as embed_color
import sqlite3
import asyncio

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

class NewEXPStats():
	def __init__(self, client):
		self.client = client

	async def on_message(self, message):
		def mkifno(mk):
			c.execute(mk)
			conn.commit()

		def hsxpstts(xpsts):
			c.execute(xpsts)
			conn.commit()
			global hsx
			hsx = c.fetchall()

		def changedname(namechn):
			c.execute(namechn)
			conn.commit()
			global namechanged
			namechanged = c.fetchall()

		def idcheck(checkid):
			c.execute(checkid)
			conn.commit()
			global checkedid
			checkedid = c.fetchall()

		def updatename(nameupdate):
			c.excute(nameupdate)
			conn.commit()

		user_id = message.author.id
		user_name = message.author.name
		level = "0"
		description = "A very empty description :^)"
		reputation = "0"
		currency = "100"
		exp = "0"
		xpsts = "SELECT COUNT(*) FROM UserData WHERE user_id = '" + message.author.id + "'"
		namechn = "SELECT user_name FROM UserData WHERE user_id = '" + message.author.id + "'"
		checkid = "SELECT user_id FROM UserData WHERE user_id = '" + message.author.id + "'"
		mk = "INSERT INTO UserData (user_id, user_name, level, exp, description, reputation, currency) VALUES ('" + user_id + "', '" + user_name + "', '" + level + "', '" + exp + "', '" + description + "', '" + reputation + "', '" + currency + "')"
		hsxpstts(xpsts)
		if hsx[0][0] != 0:
			changedname(namechn)
			idcheck(checkid)
			if namechanged[0][0] != message.author.name and message.author.name == checkedid[0][0]:
				nameupdate = "UPDATE UserData SET user_name = '" + message.author.name + "'"
				updatename(nameupdate)
		elif hsx[0][0] == 0:
			mkifno(mk)

def setup(client):
	client.add_cog(NewEXPStats(client))