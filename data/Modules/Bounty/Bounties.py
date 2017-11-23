import discord
from discord.ext import commands
import sqlite3
import asyncio
from credentials import EmbedColor as embed_color
from credentials import Owners as owner

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

class Bount:
	def __init__(self, client):
		self.client = client



	@commands.group(pass_context = True, invoke_without_command = True)
	async def bounty(self, ctx, user: str = None):

		def read(sa2):
		    c.execute(sa2)
		    conn.commit()
		    global bn
		    bn = c.fetchall()

		def read_from_db(sp):
		    c.execute(sp)
		    conn.commit()
		    global bnts
		    bnts = c.fetchall()

		def allbounties(allbnts):
		    c.execute(allbnts)
		    conn.commit()
		    global allbounty
		    allbounty = c.fetchall()

		if user is None:
			try:
				allbnts = "SELECT * FROM Bounties"
				allbounties(allbnts)
				embed = discord.Embed(description = str(allbounty), color = embed_color)
				await self.client.say(embed = embed)
			except IndexError as e:
				embed = discord.Embed(description = "There's no bounties found!", color = 0xFF0000)
				await self.client.say(embed = embed)
		else:
			sp = "SELECT COUNT(*) FROM Bounties WHERE user = '" + user + "'"
			read_from_db(sp)
			if bnts[0][0] != 0:
				sa2 = "SELECT * FROM Bounties WHERE user = '" + user + "'"
				read(sa2)
				embed = discord.Embed(title = "WANTED", color = embed_color)
				embed.add_field(name="Name", value=bn[0][1], inline=True)
				embed.add_field(name="Reward", value=bn[0][2], inline=True)
				await self.client.say(embed = embed)
			else:
				embed = discord.Embed(description = "`" + user + "` is not wanted, does not have a bounty or has already been caught!", color = 0xFF0000)
				await self.client.say(embed = embed)


	@bounty.command(pass_context = True)
	async def add(self, ctx, user: str, rwrd: str):
		def bntyadd(sq):
		    c.execute(sq)
		    conn.commit()
		    global data
		    data = c.fetchall()

		def nghcash(ngcash):
			c.execute(ngcash)
			conn.commit()
			global enghcash
			enghcash = c.fetchall()

		sq = "INSERT INTO Bounties (user, username, reward) VALUES ('" + user + "', '" + user + "', '" + rwrd + "')"
		ngcash = "SELECT currency FROM UserData WHERE user_id = '" + ctx.message.author.id + "'"
		nghcash(ngcash)
		if int(enghcash[0][0]) > int(rwrd) or int(enghcash[0][0]) == int(rwrd):
			bntyadd(sq)
			embed = discord.Embed(description = "`" + user + "` now has a bounty with price of `" + rwrd + "`!\nCatch them and win the `" + rwrd + "`**$**!", color = embed_color)
			await self.client.say(embed = embed)
		elif int(enghcash[0][0]) < int(rwrd):
			embed = discord.Embed(description = "You don't have enough currency!\nYour currency: `" + str(enghcash[0][0]) + "`!", color = 0xFF0000)
			await self.client.say(embed = embed)

	@bounty.command(pass_context = True)
	async def remove(self, ctx, user: str):
		def bntyrem(sf):
		    c.execute(sf)
		    conn.commit()
		    global ent
		    ent = c.fetchall()

		sf = "DELETE FROM Bounties WHERE user = '" + user + "'"
		if ctx.message.author.id == owner:
			bntyrem(sf)
			embed = discord.Embed(description = "Successfully deleted `" + user + "`'s bounty!", color = embed_color)
			await self.client.say(embed = embed)
		else:
			embed = discord.Embed(description = "You are not the bot owner!", color = 0xFF0000)
			await self.client.say(embed = embed)



	@bounty.command(pass_context = True)
	async def catch(self, ctx, user: str, cash: int):
		def catchuser(catch):
		    c.execute(catch)
		    conn.commit()

		def userhasbnty(hasbnty):
		    c.execute(hasbnty)
		    conn.commit()
		    global hasbnt
		    hasbnt = c.fetchall()

		def hscsh(hascash):
		    c.execute(hascash)
		    conn.commit()
		    global bntycash
		    bntycash = c.fetchall()

		def rmvcur(rmv):
		    c.execute(rmv)
		    conn.commit()
		
		catch = "DELETE FROM Bounties WHERE user = '" + user + "'"
		hasbnty = "SELECT * FROM Bounties WHERE user = '" + user + "'"
		hascash = "SELECT * FROM UserData WHERE user_id = '" + ctx.message.author.id + "'"
		hscsh(hascash)
		alltgt = int(bntycash[0][6]) - cash
		rmv = "UPDATE UserData SET currency = '" + str(alltgt) + "' WHERE user_id = '" + ctx.message.author.id + "'"
		userhasbnty(hasbnty)
		if hasbnt[0][0] == 0:
			embed = discord.Embed(description = "There's no one named `" + user + "` to capture!", color = 0xFF0000)
			await self.client.say(embed = embed)
		elif hasbnt[0][0] != 0:
			catchuser(catch)
			rmvcur(rmv)
			embed = discord.Embed(description = "You successfully captured `" + user + "` for their bounty of `" + hasbnt[0][2] + "`!", color = embed_color)
			await self.client.say(embed = embed)

def setup(client):
	client.add_cog(Bount(client))