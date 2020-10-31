from supportingFunctions import SupportingFunctions
import discord
from discord.ext import commands
import datetime
import configparser
import sys

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('botProperties.ini')
        self.manageAtEveryone = self.config["Options"]["manageAtEveryone"]
        self.manageAtEveryone = self.manageAtEveryone.lower()
        
        if self.manageAtEveryone != "true" or self.manageAtEveryone != "false":
            print('Please enter either true or false in the "manageAtEveryone" field in botProperties.ini')
            sys.exit()

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
        if self.manageAtEveryone == True:
            if '@everyone' in message.content:
                currentDT = SupportingFunctions.getTime()
                ctx = await self.client.get_context(message)
                print(f'[{currentDT}] @everyone was pinged')
                if(message.channel.name != "771126669058375701" or message.channel.id != "759236894327570494" or message.channel.id != "759236932285759518"):

                    await ctx.channel.purge(limit=1)
                    await ctx.send("Please only ping everyone in #announcements , #polls , or #among-us-pings . All are in the top of the channels list.")
                

def setup(client):
    client.add_cog(Events(client))