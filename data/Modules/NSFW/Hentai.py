import discord
from discord.ext import commands
from credentials import Owners as owner
from credentials import EmbedColor as embed_color
import sqlite3
import aiohttp
import random
from random import randint

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

class Hen():
	def __init__(self, client):
		self.client = client


	@commands.command(pass_context = True, no_pm = True)
	async def hentai(self, ctx):

		def hentairead(sq):
			c.execute(sq)
			conn.commit()
			global hendata
			hendata = c.fetchall()

		
		server_id = ctx.message.server.id
		sq = "SELECT nsfw_is_enabled FROM Permissions WHERE server_id = '" + server_id + "'"
		hentairead(sq)
		if hendata[0][0] != 1:
			embed = discord.Embed(description = "NSFW is disabled!", color = 0xFF0000)
			await self.client.say(embed = embed)
		if hendata[0][0] == 1:
			nr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
			async with aiohttp.get("https://konachan.com/post.json?limit=500") as r:
				if r.status == 200:
					js = await r.json()
					writejs = open("api.txt", "w")
					writejs.write(str(js))
					writejs.close()
					embed = discord.Embed(description = "Here's your hentai, " + ctx.message.author.mention + "!", color = embed_color)
					embed.set_image(url = js[random.randint(0, 499)]["file_url"])
					await self.client.say(embed = embed)
				elif r.status == 401:
					await self.client.say("Exception at \n**Unauthorized**!")

def setup(client):
	client.add_cog(Hen(client))