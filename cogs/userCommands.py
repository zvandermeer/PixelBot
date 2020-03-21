import discord
from discord.ext import commands
import random

_8BallResponses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no." "Outlook not so good.", "Very doubtful."]

class userCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #User controlled events
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency *1000)}ms")

    @commands.command(aliases=["8ball", "eightball", "EightBall", "8Ball"])
    async def _8ball(self, ctx, *, question="blankMessage-NoInput"):
        if question == "blankMessage-NoInput":
            await ctx.send("Please enter a question!")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(_8BallResponses)}")

def setup(client):
    client.add_cog(userCommands(client))