import configparser
from logging import warning
import sys
from random import randint
import sys
import discord
from discord.ext import commands
import platform
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log")]
)

def loadRandomQuote(destination):
    quoteTotal = 0
    with open(f"PixelBotData/{destination}.txt", "r") as fileReader:
        allQuotes = []
        for line in fileReader:
            allQuotes.append(line)
        quoteTotal = len(allQuotes)
        quoteInt = randint(1, quoteTotal)
        selectedQuote = allQuotes[quoteInt - 1]
        parsedQuote = selectedQuote.split(';')
        quoteDict = {"name": parsedQuote[0], "quote": parsedQuote[1], "author": parsedQuote[2]}

        return quoteDict

class quoteCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.copyQuotesToWebDirectory = self.config["pixelBotConfig"]["copyQuotesToWebDirectory"]
        self.copyQuotesToWebDirectory = self.copyQuotesToWebDirectory.lower()
        
        if self.copyQuotesToWebDirectory != "true" and self.copyQuotesToWebDirectory != "false":
            warning('Please enter either true or false under the "copyQuotesToWebDirectory" field in config.ini')
            sys.exit()

        self.webDirectory = self.config["pixelBotConfig"]["webDirectory"]
        if self.webDirectory.endswith("/") or self.webDirectory.endswith("\\"):
            pass
        else:
            if platform.system() == "Windows":
                self.webDirectory = self.webDirectory + "\\"
            else:
                self.webDirectory = self.webDirectory + "/"

        self.publicWebAddress = self.config["pixelBotConfig"]["publicWebAddress"]

        if not self.publicWebAddress.startswith("http"):
            self.publicWebAddress = "http://" + self.publicWebAddress

        if self.copyQuotesToWebDirectory == "true" and self.publicWebAddress == "null":
            logging.warning('Please enter a web address under the "publicWebAddress" felid in config.ini. Please do not leave it "null"')
            print('Please enter a web address under the "publicWebAddress" felid in config.ini. Please do not leave it "null"')
            sys.exit()

    @commands.command(aliases=["q", "Q", "Quote", "quotes", "Quotes"])
    async def quote(self, ctx, *, quote=""):
        if quote == "":
            randomQuote = loadRandomQuote("quotes")

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
            await self.saveQuote(ctx, quote, "quotes")

    # @commands.command(aliases=["d", "D", "dave", "Dave", "David"])
    # async def david(self, ctx, *, quote=""):
    #     if quote == "":
    #         randomQuote = loadRandomQuote("david")

    #         members = ctx.message.guild.members

    #         for member in members:
    #             if member.name == randomQuote["name"].split("#")[0]:
    #                 quoteAuthor = member

    #         embed = discord.Embed(title=randomQuote["quote"], description=f"-{randomQuote['author']}",
    #                               color=discord.Color.purple())
    #         try:                      
    #             embed.set_author(name="Added by: " + randomQuote["name"], icon_url=quoteAuthor.avatar_url)
    #         except UnboundLocalError:
    #             embed.set_author(name="Added by: " + randomQuote["name"], icon_url="")
    #         await ctx.send(embed=embed)

    #     elif quote == "list" or quote == "List":
    #         if self.copyQuotesToWebDirectory == "true":
    #             await ctx.send(f"View the quote list here: {self.publicWebAddress}")
    #         else:
    #             await ctx.send("This bot is not configured to clone quotes to a web directory. Please contact your bot admin for more information.")

    #     else:
    #         await self.saveQuote(ctx, quote, "david")

    async def saveQuote(self, ctx, quote, destination):
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
                quote = quote.rsplit("-", 1)
            else:
                quote = quote.split("-")
            fullQuote = quote[0]
            quoteAuthor = quote[1]
        else:
            fullQuote = quote
            if destination == "david":
                quoteAuthor = "Dave"
            else:
                quoteAuthor = "Unknown"

        if fullQuote.endswith(" "):
            fullQuote = fullQuote[:-1]

        quoteData = f"{ctx.message.author};{fullQuote};{quoteAuthor}"

        with open(f"PixelBotData/{destination}.txt", 'a') as fileWriter:
            fileWriter.write(f"{quoteData}\n")
        
        if self.copyQuotesToWebDirectory == "true":
            with open(f"{self.webDirectory}/{destination}.txt", 'a') as fileWriter:
                fileWriter.write(f"{quoteData}\n")

        await ctx.send(f"-{fullQuote} added to quote list!")

        if semicolon is True:
            await ctx.send("Due to how quotes are saved, semicolons cannot be used. The semicolon in your quote "
                            "has been replaced with a comma.")

        if newline is True:
            await ctx.send("Due to how quotes are saved, new lines cannot be used. The new line in your quote has been removed and replaced with a space.")

def setup(client):
    client.add_cog(quoteCommands(client))
