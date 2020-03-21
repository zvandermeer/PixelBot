import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined a server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot sucessfully connected to discord servers")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Version 0.1"))

def setup(client):
    client.add_cog(Events(client))