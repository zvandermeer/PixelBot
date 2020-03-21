import discord
from discord.ext import commands

class userCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #User controlled events
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency *1000)}ms")

def setup(client):
    client.add_cog(userCommands(client))