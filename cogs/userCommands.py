import datetime
from supportingFunctions import SupportingFuctions
import discord
from discord.ext import commands
from bot import commandPrefix
import time
import json


class userCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.commandPrefix = "!"

    # User controlled events
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Bot ping time: {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["changestatus", "updatestatus", "status", "playing"])
    async def changeStatus(self, ctx, *, statusInput=""):
        if statusInput == "":
            await ctx.send("Please enter a status for the bot")
        else:
            lowerStatusInput = statusInput.lower()
            if lowerStatusInput.startswith("playing "):
                statusOutput = statusInput.split(" ", 1)
                await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusOutput[1]))
                await ctx.send(
                    f'Status updated to "Playing {statusOutput[1]}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                currentDT = SupportingFuctions.getTime()
                print(f"[{currentDT}] Status updated to playing '{statusOutput[1]}''")
            else:
                await self.client.change_presence(status=discord.Status.online, activity=discord.Game(statusInput))
                await ctx.send(
                    f'Status updated to "Playing {statusInput}"! Please note this is not permenant, and will be reset when the bot is rebooted.')
                currentDT = SupportingFuctions.getTime()
                print(f"[{currentDT}] Status updated to 'playing {statusInput}''")

    # @commands.command(aliases=["prefix", "changeprefix"])
    # async def changePrefix(self, ctx, newPrefix=""):
    #     if newPrefix == "":
    #         await ctx.send("Please enter a prefix.")
    #     elif newPrefix == self.commandPrefix:
    #         await ctx.send("That is the current prefix. Please enter a new prefix!")
    #     else:
    #         with open("botData.json") as file:
    #             jsonData = file.read()
    #             jsonFormatted = json.loads(jsonData)
    #             jsonFormatted["prefix"] = newPrefix
    #             jsonData = json.dumps(jsonFormatted)
    #             file.write(jsonData)

    @commands.command(aliases=["creator", "info"])
    async def about(self, ctx):
        embed = discord.Embed(title="**PixelBot v0.4.0**", description="This bot is running PixelBot v0.4.0. "
                                                                       "Developed by "
                                                                       "NinjaPixels. Code is hosted at "
                                                                       "https://github.com/ovandermeer/PixelBot",
                              color=discord.Color.green())

        embed.set_author(name="", icon_url="https://cdn.discordapp.com/avatars/690639974772637826/dae6197fc28fdd6a6fb73a9909397556.webp?size=256")

        embed.add_field(name="Command help",
                        value="Type &help for a list of commands and how to use them.",
                        inline=True)
        embed.add_field(name="Bugs? Issues?",
                        value="Report problems with the bot at:\n https://github.com/ovandermeer/PixelBot/issues",
                        inline=False)
        embed.add_field(name="Documentation",
                        value="Documentation and more detailed command help can be found at: "
                              "https://ovandermeer.github.io/PixelBot/",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def testing(self, ctx):
        embed = discord.Embed(title="*Quote*", description="-quote author", color=discord.Color.green())

        embed.set_author(name="Jeff", icon_url="https://cdn.discordapp.com/avatars/690639974772637826"
                                               "/dae6197fc28fdd6a6fb73a9909397556.webp?size=256")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(userCommands(client))
