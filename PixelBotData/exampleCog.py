import discord
from discord.ext import commands


# Example cog
class cogName(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Example command
    @commands.command(aliases=["alias1", "alias2"])
    async def commandName(self, ctx):
        await ctx.send("Command success!")

def setup(client):
    client.add_cog(cogName(client))
