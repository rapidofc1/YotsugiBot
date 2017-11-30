import discord
from discord.ext.commands import bot
import asyncio
from credentials import Owners as owner
from credentials import EmbedColor as embed_color
import sqlite3

conn = sqlite3.connect('YotsugiBot.db')
c = conn.cursor()

class Perms():
	def __init__(self, client):
		self.client = client


	async def on_server_join(self, server):


		def check_if_has_perms(chkperms):
			c.execute(chkperms)
			conn.commit()
			global hasperms
			hasperms = c.fetchall()

		def create_perms(cperms):
			c.execute(cperms)
			conn.commit()


		chkperms = "SELECT COUNT(*) FROM Permissions WHERE server_id = '" + server.id + "'"
		cperms = "INSERT INTO Permissions (nsfw_is_enabled, server_id) VALUES ('" + str("0") + "', '" + server.id + "')"

		check_if_has_perms(chkperms)
		if hasperms[0][0] > 0:
			return
		elif hasperms[0][0] < 0:
			create_perms(cperms)



	async def on_message(self, message):

		
		def check_if_message_server_has_perms(msghasperms):
			c.execute(msghasperms)
			conn.commit()
			global msgperms
			msgperms = c.fetchall()

		def if_no_perms_make_perms(msgnoperms):
			c.execute(msgnoperms)
			conn.commit()

		msghasperms = "SELECT COUNT(*) FROM Permissions WHERE server_id = '" + message.server.id + "'"
		msgnoperms = "INSERT INTO Permissions (nsfw_is_enabled, server_id) VALUES ('" + str("0") + "', '" + message.server.id + "')"

		check_if_message_server_has_perms(msghasperms)
		if msgperms[0][0] == 0:
			if_no_perms_make_perms(msgnoperms)
		elif msgnoperms[0][0] != 0:
			return

def setup(client):
	client.add_cog(Perms(client))