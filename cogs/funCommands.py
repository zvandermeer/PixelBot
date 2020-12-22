import configparser
import datetime
import discord
from discord.ext import commands
from random import randint
import random
import time
import platform
import sys

eightBallResponses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
                      "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                      "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                      "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                      "My sources say no." "Outlook not so good.", "Very doubtful."]


def loadRandomQuote():
    quoteTotal = 0
    with open("PixelBotData/quotes.txt", "r") as fileReader:
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

        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.copyQuotesToWebDirectory = self.config["pixelBotConfig"]["copyQuotesToWebDirectory"]
        self.copyQuotesToWebDirectory = self.copyQuotesToWebDirectory.lower()
        
        if self.copyQuotesToWebDirectory != "true" and self.copyQuotesToWebDirectory != "false":
            print('Please enter either true or false under the "copyQuotesToWebDirectory" field in config.ini')
            sys.exit()

        self.webDirectory = self.config["pixelBotConfig"]["webDirectory"]
        if self.webDirectory.endswith("/") or self.webDirectory.endswith("\\"):
            pass
        else:
            if platform.system == "Windows":
                self.webDirectory = self.webDirectory + "\\"
            else:
                self.webDirectory = self.webDirectory + "/"

        self.publicWebAddress = self.config["pixelBotConfig"]["publicWebAddress"]

        if self.copyQuotesToWebDirectory == "true" and self.publicWebAddress == "null":
            print('Please enter a web address under the "publicWebAddress" felid in config.ini. Please do not leave it "null"')
            sys.exit()

    @commands.command(aliases=["q", "Q", "Quote", "quotes", "Quotes"])
    async def quote(self, ctx, *, quote=""):
        if quote == "":
            randomQuote = loadRandomQuote()

            members = ctx.message.guild.members

            for member in members:
                if member.name == randomQuote["name"].split("#")[0]:
                    quoteAuthor = member

            embed = discord.Embed(title=randomQuote["quote"], description=f"-{randomQuote['author']}",
                                  color=discord.Color.blue())
            try:                      
                embed.set_author(name="Added by: " + randomQuote["name"], icon_url=quoteAuthor.avatar_url)
            except UnboundLocalError:
                embed.set_author(name="Added by: " + randomQuote["name"], icon_url="")
            await ctx.send(embed=embed)

        elif quote == "list" or quote == "List":
            if self.copyQuotesToWebDirectory == "true":
                await ctx.send(f"View the quote list here: {self.publicWebAddress}")
            else:
                await ctx.send("This bot is not configured to clone quotes to a web directory. Please contact your bot admin for more information.")

        else:
            if quote.startswith("add ") or quote.startswith("Add "):
                quote = quote[4:]

            semicolon = False
            newline = False

            if ";" in quote:
                quote = quote.replace(";", ",")
                semicolon = True

            if "”" in quote or "“" in quote:
                quote = quote.replace("“", '"')
                quote = quote.replace("”", '"')

            if "’" in quote:
                quote = quote.replace("’", "'")

            if "\n" in quote:
                quote = quote.replace("\n", " ")
                newline = True

            if '-' in quote:
                if quote.count('-') > 1:
                    quote = quote.split("-")
                else:
                    quote = quote.rsplit("-", 0)
                fullQuote = quote[0]
                quoteAuthor = quote[1]
            else:
                fullQuote = quote
                quoteAuthor = "Unknown"

            if fullQuote.endswith(" "):
                fullQuote = fullQuote[:-1]

            quoteData = f"{ctx.message.author};{fullQuote};{quoteAuthor}"

            with open("PixelBotData/quotes.txt", 'a') as fileWriter:
                fileWriter.write(f"{quoteData}\n")
            
            if self.copyQuotesToWebDirectory == "true":
                with open(f"{self.webDirectory}/quotes.txt", 'a') as fileWriter:
                    fileWriter.write(f"{quoteData}\n")

            await ctx.send(f"-{fullQuote} added to quote list!")

            if semicolon is True:
                await ctx.send("Due to how quotes are saved, semicolons cannot be used. The semicolon in your quote "
                               "has been replaced with a comma.")

            if newline is True:
                await ctx.send("Due to how quotes are saved, new lines cannot be used. The new line in your quote has been removed and replaced with a space.")

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
            await ctx.send("An internal error has occurred")

    @commands.command(aliases=["Hello", "hi", "Hi"])
    async def hello(self, ctx):
        await ctx.send("Hello! :smiley:")

    @commands.command(aliases=["hellothere", "HelloThere"])
    async def helloThere(self, ctx):
        await ctx.send("https://tenor.com/view/grevious-general-kenobi-star-wars-gif-11406339")


def setup(client):
    client.add_cog(funCommands(client))
