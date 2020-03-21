import discord
from discord.ext import commands

class userCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #User controlled events
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency *1000)}ms")

    @commands.command(aliases=["changestatus", "updatestatus", "status", "playing"])
    async def changeStatus(self, ctx, *, statusInput="blankInput"):
        if statusInput == "blankInput":
            await ctx.send("Please enter a status for the bot")
        elif statusInput.startswith("Playing "):
            statusOutput = statusInput.split(" ", 1)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusOutput[1]))
            await ctx.send(f'Status updated to "Playing {statusOutput[1]}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
            print(f"Status updated to playing {statusOutput[1]}")
        elif statusInput.startswith("playing "):
            statusOutput = statusInput.split(" ", 1)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusOutput[1]))
            await ctx.send(f'Status updated to "Playing {statusOutput[1]}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
            print(f"Status updated to playing {statusOutput[1]}")
        else:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusInput))
            await ctx.send(f'Status updated to "Playing {statusInput}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
            print(f"Status updated to playing {statusInput}")

def setup(client):
    client.add_cog(userCommands(client))