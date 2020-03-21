import discord
from discord.ext import commands

class Name(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Commands go here

def setup(client):
    client.add_cog(Name(client))