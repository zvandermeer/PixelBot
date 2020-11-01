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
        
        if self.manageAtEveryone != "true" and self.manageAtEveryone != "false":
            print('Please enter either true or false under the "manageAtEveryone" field in botProperties.ini')
            sys.exit()

        self.deleteUnwantedPings = self.config["Options"]["deleteUnwantedPings"]
        self.deleteUnwantedPings = self.deleteUnwantedPings.lower()
        
        if self.deleteUnwantedPings != "true" and self.deleteUnwantedPings != "false":
            print('Please enter either true or false under the "deleteUnwantedPings" field in botProperties.ini')
            sys.exit()

        self.allowedChannels = self.config["Options"]["allowedChannelNames"]

        if self.allowedChannels == "null" and self.manageAtEveryone == "true":
            print('Please enter channel name(s) under the "allowedChannelNames" field in botProperties.ini. Check botProperties.ini for examples')
            sys.exit()

        if " " in self.allowedChannels:
            self.allowedChannels = self.allowedChannels.replace(" ", "")

        self.allowedChannels = self.allowedChannels.split(",")

        self.allowedChannelIDs = ""

        #for channel in self.allowedChannels:
        #    channelObject = discord.utils.get(client.guild.channels, name=channel)
        #    allowedChannelIDs = allowedChannelIDs.append(channelObject.id)
            

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
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Version 0.4.1"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.manageAtEveryone == "true":
            if '@everyone' in message.content:
                currentDT = SupportingFunctions.getTime()
                ctx = await self.client.get_context(message)
                print(f'[{currentDT}] @everyone was pinged. Message contents:\n{message.author}: "{message.content}"')

                if(ctx.message.channel.name not in self.allowedChannels):
                    if self.deleteUnwantedPings == "true":
                        await ctx.channel.purge(limit=1)

                    allowedChannelIDs = []

                    for channel in self.allowedChannels:
                        tempChannelObject = discord.utils.get(ctx.guild.channels, name=channel)
                        allowedChannelIDs.append(tempChannelObject.id)
                
                    allowedChannelsList = ["<#" + str(channel) for channel in allowedChannelIDs]
                    allowedChannelMessage = [str(channel) + ">, " for channel in allowedChannelsList]
                    allowedChannelMessage = " ".join(str(x) for x in allowedChannelMessage)
                    allowedChannelMessage = allowedChannelMessage.replace("[", "")
                    allowedChannelMessage = allowedChannelMessage.replace("'", "")
                    allowedChannelMessage = allowedChannelMessage[:-2]

                    await ctx.send(f"Please only ping everyone in {allowedChannelMessage}")
                

def setup(client):
    client.add_cog(Events(client))