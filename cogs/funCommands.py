import datetime
import discord
from discord.ext import commands
from random import randint
import random
import time
import platform

eightBallResponses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
                      "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                      "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                      "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                      "My sources say no." "Outlook not so good.", "Very doubtful."]


def loadRandomQuote():
    quoteTotal = 0
    with open("quotes.txt", "r") as fileReader:
        allQuotes = []
        for line in fileReader:
            allQuotes.append(line)
        # print(f"allQuotes: {allQuotes}")
        quoteTotal = len(allQuotes)
        # print(f"quoteTotal: {quoteTotal}")
        quoteInt = randint(1, quoteTotal)
        # print(f"quoteInt: {quoteInt}")
        selectedQuote = allQuotes[quoteInt - 1]
        # print(f"selectedQuote: {selectedQuote}")
        parsedQuote = selectedQuote.split(';')
        # print(f"parsedQuote: {parsedQuote}")
        quoteDict = {"name": parsedQuote[0], "quote": parsedQuote[1], "author": parsedQuote[2]}

        return quoteDict


class funCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def quote(self, ctx, *, quote=""):
        if quote == "":
            randomQuote = loadRandomQuote()

            embed = discord.Embed(title=randomQuote["quote"], description=f"-{randomQuote['author']}",
                                  color=discord.Color.blue())
            embed.set_author(name=randomQuote["name"], icon_url="")
            await ctx.send(embed=embed)

        elif quote == "list":
            await ctx.send("View the quote list here: https://www.ovmcloud.ddns.net/quotes.txt")

        else:
            if '-' in quote:
                if quote.count('-') > 1:
                    quote = quote.split("-")
                else:
                    quote = quote.rsplit("-")
                fullQuote = quote[0]
                quoteAuthor = quote[1]
            else:
                fullQuote = quote
                quoteAuthor = "Unknown"

            quoteData = f"{ctx.message.author};{fullQuote};{quoteAuthor}"

            with open("quotes.txt", 'a') as fileWriter:
                fileWriter.write(f"{quoteData}\n")

            if platform.system() == "Linux":
                with open("/var/www/html/quotes.txt", 'a') as fileWriter:
                    fileWriter.write(f"{quoteData}\n")

            await ctx.send(f"-{fullQuote} added to quote list!")

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
        await ctx.send("The number is " + str(randint(1, sides)) + "!")

    @commands.command(aliases=["FlipACoin", "flipacoin", "coinflip", "flipcoin"])
    async def coinFlip(self, ctx):
        coinState = randint(0, 1)
        if coinState == 0:
            await ctx.send("The coin landed on heads!")
        elif coinState == 1:
            await ctx.send("The coin landed on tails!")
        else:
            await ctx.send("An internal error has occured")

    @commands.command(aliases=["Hello", "hi", "Hi"])
    async def hello(self, ctx):
        await ctx.send("Hello! :smiley:")

    @commands.command(aliases=["hellothere", "HelloThere"])
    async def helloThere(self, ctx):
        await ctx.send("https://tenor.com/view/grevious-general-kenobi-star-wars-gif-11406339")


def setup(client):
    client.add_cog(funCommands(client))
