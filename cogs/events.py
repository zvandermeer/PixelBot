from itertools import cycle
import PixelBotData.supportingFunctions as supportingFunctions
import discord
from discord.ext import commands, tasks
import datetime
import configparser
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"debug-{supportingFunctions.getDate()}.log")]
)

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.manageAtEveryone = self.config["pixelBotConfig"]["manageAtEveryone"]
        self.manageAtEveryone = self.manageAtEveryone.lower()

        self.commandPrefix = self.config['pixelBotConfig']['prefix']
        
        if self.manageAtEveryone != "true" and self.manageAtEveryone != "false":
            logging.warning('Please enter either true or false under the "manageAtEveryone" field in config.ini')
            print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "manageAtEveryone" field in config.ini')
            sys.exit()

        self.deleteUnwantedPings = self.config["pixelBotConfig"]["deleteUnwantedPings"]
        self.deleteUnwantedPings = self.deleteUnwantedPings.lower()
        
        if self.deleteUnwantedPings != "true" and self.deleteUnwantedPings != "false":
            logging.warning('Please enter either true or false under the "deleteUnwantedPings" field in config.ini')
            print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "deleteUnwantedPings" field in config.ini')
            sys.exit()

        self.allowedChannels = self.config["pixelBotConfig"]["allowedChannelNames"]

        if self.allowedChannels == "null" and self.manageAtEveryone == "true":
            logging.warning('Please enter channel name(s) under the "allowedChannelNames" field in config.ini. Check config.ini for examples')
            print(f'[{supportingFunctions.getTime()}] Please enter channel name(s) under the "allowedChannelNames" field in config.ini. Check config.ini for examples')
            sys.exit()

        if " " in self.allowedChannels:
            self.allowedChannels = self.allowedChannels.replace(" ", "")

        self.allowedChannels = self.allowedChannels.split(",")

        self.allowedChannelIDs = ""

        self.botStatus = self.config["pixelBotConfig"]["botStatus"]

        if self.config["pixelBotConfig"]["DMnewUsers"].lower() == "true":
            self.dmWelcomeMessage = self.config["pixelBotConfig"]["newUserWelcome"]   

        self.streamingStatus = self.config["pixelBotConfig"]["streamingStatus"]
        self.streamingStatus = self.streamingStatus.lower()
        
        if self.streamingStatus != "true" and self.streamingStatus != "false":
            logging.warning('Please enter either true or false under the "deleteUnwantedPings" field in config.ini')
            print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "deleteUnwantedPings" field in config.ini')
            sys.exit()

        self.streamURL = self.config["pixelBotConfig"]["streamURL"]

        self.invites = {}
    
    # tasks
    # @tasks.loop(seconds=10)
    # async def change_status(self):
    #     await self.client.change_presence(activity=discord.Game(next(self.status)))
            

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logging.info(f'{member} has joined a server')
        print(f'[{supportingFunctions.getTime()}] {member} has joined a server')

        memberString = str(member)
        memberString = memberString.split("#")

        message = self.dmWelcomeMessage.replace("{member}", memberString[0])

        await member.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logging.info(f'{member} has left a server')
        print(f'[{supportingFunctions.getTime()}] {member} has left a server')

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("PixelBot successfully connected to Discord servers")
        print(f"[{supportingFunctions.getTime()}] PixelBot successfully connected to Discord servers")
        if self.streamingStatus == "true":
            await self.client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=self.botStatus, url=self.streamURL))
        else:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(self.botStatus))
        
        # self.change_status.start()
        

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.client.get_context(message)

        if '@everyone' in message.content:
            logging.info(f'@everyone was pinged. Message contents:\n{message.author}: "{message.content}"')
            print(f'[{supportingFunctions.getTime()}] @everyone was pinged. Message contents:\n{message.author}: "{message.content}"')
            if self.manageAtEveryone == "true":
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

        if f'<@!{self.client.user.id}>' in message.content:
            embed = discord.Embed(title="**PixelBot v0.4.3**", description="This bot is running PixelBot v0.4.3. "
                                                                       "Developed by "
                                                                       "NinjaPixels. Code is hosted at "
                                                                       "https://github.com/ovandermeer/PixelBot",
                              color=discord.Color.green())

            embed.set_author(name="", icon_url="https://cdn.discordapp.com/avatars/690639974772637826/dae6197fc28fdd6a6fb73a9909397556.webp?size=256")

            embed.add_field(name="Command help",
                            value=f"Type {self.commandPrefix}help for a list of commands and how to use them.",
                            inline=True)
            embed.add_field(name="Bugs? Issues?",
                            value="Report problems with the bot at:\n https://github.com/ovandermeer/PixelBot/issues",
                            inline=False)
            embed.add_field(name="Documentation",
                            value="Documentation and more detailed command help can be found at: "
                                "https://ovandermeer.github.io/PixelBot/",
                            inline=False)

            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(f"[{supportingFunctions.getTime()}] message deleted")
        logging.info(f"Message deleted. Message content: '{message.content}' Message author: '{message.author}' Message channel: '{message.channel.name}' Message server: '{message.guild.name}'")
        print(f"[{supportingFunctions.getTime()}] Message deleted. Message content: '{message.content}' Message author: '{message.author}' Message channel: '{message.channel.name}' Message server: '{message.guild.name}'")
        if "@" in message.content:
            logging.debug("Message deleted w/ @")
            print(f"[{supportingFunctions.getTime()}] Message deleted w/ @")
        else:
            logging.debug("Message deleted w/o @")
            print(f"[{supportingFunctions.getTime()}] Message deleted w/o @")             

def setup(client):
    client.add_cog(Events(client))