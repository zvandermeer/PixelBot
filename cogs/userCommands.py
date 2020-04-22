import discord
from discord.ext import commands
from bot import commandPrefix
import time

class userCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.commandPrefix = "!"
        print("nah fam")

    #User controlled events
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency *1000)}ms")

    @commands.command(aliases=["changestatus", "updatestatus", "status", "playing"])
    async def changeStatus(self, ctx, *, statusInput=""):
        if statusInput == "":
            await ctx.send("Please enter a status for the bot")
        else:
            lowerStatusInput = statusInput.lower
            if lowerStatusInput.startswith("playing "):
                statusOutput = statusInput.split(" ", 1)
                await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusOutput[1]))
                await ctx.send(f'Status updated to "Playing {statusOutput[1]}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                print(f"Status updated to playing {statusOutput[1]}")
            else:
                await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusInput))
                await ctx.send(f'Status updated to "Playing {statusInput}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                print(f"Status updated to playing {statusInput}")
    
    @commands.command(aliases=["prefix", "changeprefix"])
    async def changePrefix(self, ctx, newPrefix=""):
        if newPrefix == "":
            await ctx.send("Please enter a prefix.")
        elif newPrefix == self.commandPrefix:
            await ctx.send("That is the current prefix. Please enter a new prefix!")
        else:
            commandPrefix = ""
            commandPrefix = newPrefix
            client = commands.Bot(command_prefix = commandPrefix)
            time.sleep (.1)
            await ctx.send(commandPrefix)
            print(commandPrefix)

def setup(client):
    client.add_cog(userCommands(client))