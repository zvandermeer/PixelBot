import configparser
import random
import sys
import time

from discord import activity
import PixelBotData.supportingFunctions as supportingFunctions
import discord
from discord.ext import commands
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log")]
)

eightBallResponses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
                      "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                      "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                      "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                      "My sources say no." "Outlook not so good.", "Very doubtful."]

class basicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.commandPrefix = config['pixelBotConfig']['prefix']

        self.statusChangeCommand = config['pixelBotConfig']['statusChangeCommand']
        self.statusChangeCommand = self.statusChangeCommand.lower()

        if self.statusChangeCommand != "true" and self.statusChangeCommand != "false":
            logging.warning('Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            sys.exit()

        self.statusChangeOnlyAdmin = config['pixelBotConfig']['statusChangeOnlyAdmin']
        self.statusChangeOnlyAdmin = self.statusChangeOnlyAdmin.lower()

        if self.statusChangeOnlyAdmin != "true" and self.statusChangeOnlyAdmin != "false":
            ('Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            sys.exit()

        self.botAdmin = config['pixelBotConfig']['botAdmin']
        self.botAdmin = int(self.botAdmin)

        self.botStatus = config["pixelBotConfig"]["botStatus"]

    # User controlled events
    @commands.command()
    async def ping(self, ctx):
        logging.info(f"Bot ping latency: {round(self.client.latency * 1000)}ms")
        print(f"[{supportingFunctions.getTime()}] Bot ping latency: {round(self.client.latency * 1000)}ms")
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["changestatus", "updatestatus", "status", "playing"])
    async def changeStatus(self, ctx, *, statusInput=""):
        if self.statusChangeCommand == "true":
            runCommand = False
            if self.statusChangeOnlyAdmin == "false":
                runCommand = True
            else:

                if ctx.message.author == self.client.get_user(self.botAdmin):
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
                            f'Status updated to "Playing **{statusOutput[1]}**"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                        logging.info(f"Status updated to playing '{statusOutput[1]}''")
                        print(f"[{supportingFunctions.getTime()}] Status updated to playing '{statusOutput[1]}''")
                    else:
                        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusInput))
                        await ctx.send(
                            f'Status updated to "Playing **{statusInput}**". Please note this is not permenant, and will be reset when the bot is rebooted.')
                        logging.info(f"Status updated to 'Playing {statusInput}'")
                        print(f"[{supportingFunctions.getTime()}] Status updated to 'Playing {statusInput}'")
            else:
                await ctx.send("This command can only be run by the bot admin. Please contact your bot admin if you believe this to be a mistake.")
        else:
            await ctx.send("This command is currently disabled. Please contact your bot admin if you believe this to be a mistake.")

    @commands.command(aliases=["resetstatus"])
    async def resetStatus(self, ctx):
        if self.statusChangeCommand == "true":
            runCommand = False
            if self.statusChangeOnlyAdmin == "false":
                runCommand = True
            else:

                if ctx.message.author == self.client.get_user(self.botAdmin):
                    runCommand = True
            
            if runCommand == True:
                await self.client.change_presence(status=discord.Status.online, activity=discord.Game(self.botStatus))

                await ctx.send("Status has been reset!")


    @commands.command(aliases=["creator", "info"])
    async def about(self, ctx):
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
                counter += 1

    @commands.command(aliases=["8ball", "eightball", "EightBall", "8Ball"])
    async def eightBall(self, ctx, *, question=""):
        if question == "":
            await ctx.send("Please enter a question!")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(eightBallResponses)}")

    @commands.command(aliases=["rolldice"])
    async def dice(self, ctx, sides=6):
        await ctx.send(f"Rolling a {sides} sided dice!")
        time.sleep(.5)
        await ctx.send("The number is " + str(random.randint(1, sides)) + "!")

    @commands.command(aliases=["FlipACoin", "flipacoin", "coinflip", "flipcoin"])
    async def coinFlip(self, ctx):
        coinState = random.randint(0, 1)
        if coinState == 0:
            await ctx.send("The coin landed on heads!")
        elif coinState == 1:
            await ctx.send("The coin landed on tails!")
        else:
            await ctx.send("An internal error has occurred")

    @commands.command(aliases=["Hello", "hi", "Hi"])
    async def hello(self, ctx):
        await ctx.send("Hello! :smiley:")

    @commands.command(aliases=["hellothere", "HelloThere"])
    async def helloThere(self, ctx):
        await ctx.send("https://tenor.com/view/grevious-general-kenobi-star-wars-gif-11406339")

def setup(client):
    client.add_cog(basicCommands(client))
