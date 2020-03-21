import discord
from discord.ext import commands
from random import randint
import random
import time

_8BallResponses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no." "Outlook not so good.", "Very doubtful."]

class funCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball", "eightball", "EightBall", "8Ball"])
    async def _8ball(self, ctx, *, question="blankMessage-NoInput"):
        if question == "blankMessage-NoInput":
            await ctx.send("Please enter a question!")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(_8BallResponses)}")

    @commands.command(aliases=["rolldice"])
    async def dice(self, ctx, sides=6):
        await ctx.send(f"Rolling a {sides} sided dice!")
        time.sleep(.5)
        await ctx.send("The number is " + str(randint(1, sides)) + "!")

    @commands.command(ailises=["flipcoin", "coinflip"])
    async def coinFlip(self, ctx):
        coinState = randint(0,1)
        if coinState == 0: 
            await ctx.send("The coin landed on heads!")
        elif coinState == 1:
            await ctx.send("The coin landed on tails!")
        else:
            await ctx.send("An internal error has occured")

def setup(client):
    client.add_cog(funCommands(client))