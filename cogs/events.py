from supportingFunctions import SupportingFuctions
import discord
from discord.ext import commands
import datetime

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        currentDT = SupportingFuctions.getTime()
        print(f'[{currentDT}] {member} has joined a server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        currentDT = SupportingFuctions.getTime()
        print(f'[{currentDT}] {member} has left a server')

    @commands.Cog.listener()
    async def on_ready(self):
        currentDT = SupportingFuctions.getTime()
        print(f"[{currentDT}] PixelBot sucessfully connected to Discord servers")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Version 0.3.1"))

def setup(client):
    client.add_cog(Events(client))