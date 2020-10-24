from supportingFunctions import SupportingFunctions
import discord
from discord.ext import commands
import datetime

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        currentDT = SupportingFunctions.getTime()
        print(f'[{currentDT}] {member} has joined a server')

        memberString = str(member)
        memberString = memberString.split("#")

        await member.send(f"Welcome {memberString[0]}, to the Epic 5head Server!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        currentDT = SupportingFunctions.getTime()
        print(f'[{currentDT}] {member} has left a server')

    @commands.Cog.listener()
    async def on_ready(self):
        currentDT = SupportingFunctions.getTime()
        print(f"[{currentDT}] PixelBot successfully connected to Discord servers")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Version 0.4.0"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if '@everyone' in message.content:
            print('Keyword found in message')
            # Do stuff here

def setup(client):
    client.add_cog(Events(client))