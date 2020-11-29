import configparser
import datetime
import sys
from PixelBotData.supportingFunctions import SupportingFunctions
import discord
from discord.ext import commands


class userCommands(commands.Cog):
    def __init__(self, client):
        self.mySupport = SupportingFunctions()

        self.client = client

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.commandPrefix = config['pixelBotConfig']['prefix']

        self.statusChangeCommand = config['pixelBotConfig']['statusChangeCommand']
        self.statusChangeCommand = self.statusChangeCommand.lower()

        if self.statusChangeCommand != "true" and self.statusChangeCommand != "false":
            print('Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            sys.exit()

        self.statusChangeRequiresRole = config['pixelBotConfig']['statusChangeRequiresRole']
        self.statusChangeRequiresRole = self.statusChangeRequiresRole.lower()

        if self.statusChangeRequiresRole != "true" and self.statusChangeRequiresRole != "false":
            print('Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            sys.exit()

    # User controlled events
    @commands.command()
    async def ping(self, ctx):
        print("Pong!")
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["changestatus", "updatestatus", "status", "playing"])
    async def changeStatus(self, ctx, *, statusInput=""):
        if self.statusChangeCommand == "true":
            runCommand = False
            if self.statusChangeRequiresRole == "false":
                runCommand = True
            else:
                for role in ctx.author.roles:
                        role = str(role)
                        if role == "Bot Admin":
                            runCommand = True
            
            if runCommand == True:
                if statusInput == "":
                    await ctx.send("Please enter a status for the bot")
                else:
                    lowerStatusInput = statusInput.lower()
                    if lowerStatusInput.startswith("playing "):
                        statusOutput = statusInput.split(" ", 1)
                        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusOutput[1]))
                        await ctx.send(
                            f'Status updated to "Playing {statusOutput[1]}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                        currentDT = self.mySupport.getTime()
                        print(f"[{currentDT}] Status updated to playing '{statusOutput[1]}''")
                    else:
                        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusInput))
                        await ctx.send(
                            f'Status updated to "Playing {statusInput}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                        currentDT = self.mySupport.getTime()
                        print(f"[{currentDT}] Status updated to 'playing {statusInput}''")
            else:
                await ctx.send("This command requires the 'Bot Admin' role to run. Please make sure you have this role, and try again.")
        else:
            await ctx.send("This command is currently disabled. Please contact your bot admin if you believe this to be a mistake")

    @commands.command(aliases=["creator", "info"])
    async def about(self, ctx):
        embed = discord.Embed(title="**PixelBot v0.4.2**", description="This bot is running PixelBot v0.4.2. "
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

    @commands.command()
    async def dmSpam(self, ctx, member : discord.Member, amount, *, message):
        #authorId = ctx.message.author.id
        #authorObject = self.client.get_user(authorId)

        try:
            amount = int(amount)
        except ValueError:
            await ctx.send(f"Unknown amount: {amount}. Please check your command formatting by using '{self.commandPrefix}help dmSpam'")
        
        if amount >= 31:
            await ctx.send("You can't spam more than 30 times so you don't overload the bot. Try again with a smaller number!")
        else:
            counter = 0
            while counter < amount:
                await member.send(message)
                counter = counter + 1


def setup(client):
    client.add_cog(userCommands(client))
