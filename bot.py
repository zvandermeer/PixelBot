try:
    import discord
except(ModuleNotFoundError):
    print("We have detected that the required discord.py library is not installed on your system. To install the discord.py library, use 'pip/pip3 install discord'")
    exit()

from supportingFunctions import SupportingFuctions
from discord.ext import commands, tasks
import os
import datetime

from discord.ext import commands

try:
    with open('botToken.txt', 'r') as file:
        botKey = file.read()
except(FileNotFoundError):
    print(
        "Please add a 'botToken.txt' file containing the token for your bot. Please do not include any other text in "
        "this file.")
    exit()

commandPrefix = "&"
client = commands.Bot(command_prefix=commandPrefix)
# status = cycle(["Status 1", "Status 2"])
debugger = False


# event
# @client.event
# async def on_ready():
#     change_status.start()

# cogs commands
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully loaded!")
    currentDT = SupportingFuctions.getTime()
    print(f"[{currentDT}] Loaded {extension} cog")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Successfully unloaded!")
    currentDT = SupportingFuctions.getTime()
    print(f"[{currentDT}] Unloaded {extension} cog")


@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully reloaded!")
    currentDT = SupportingFuctions.getTime()
    print(f"[{currentDT}] Reloaded {extension} cog")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# tasks
# @tasks.loop(seconds=10)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))

# cogErrorHandler
@load.error
async def loadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to load")
        handledError = True


@reload.error
async def reloadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to reload")
        handledError = True


@unload.error
async def unloadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to unload")
        handledError = True


@unload.error
async def unloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")
        handledError = True


@reload.error
async def reloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")
        handledError = True


@load.error
async def loadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")
        handledError = True


# errorHandler
@client.event
async def on_command_error(ctx, error):
    currentDT = SupportingFuctions.getTime()
    print(f"[{currentDT}] {error}")
    # if debugger == True:
    #     await ctx.send(f"{error}")
    handledError = False
    if isinstance(error, commands.CommandNotFound):
        handledError = True
        await ctx.send("Invalid command!")
        try:
            print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in '" + str(
                ctx.message.guild.name) + "' in the '" + ctx.message.channel.name + "' text channel.")
        except AttributeError:
            print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in DM")
    elif isinstance(error, commands.MissingRole or commands.MissingPermissions):
        handledError = True
        await ctx.send("You do not have sufficient permissions to use this command. Please contact the server "
                       "administrator if you believe this to be a mistake.")
    elif isinstance(error, commands.MissingRequiredArgument):
        handledError = True
        await ctx.send("You are missing arguments for this command. Type !help <command> for help with the command.")
    elif (handledError == False):
        await ctx.send("An error has occurred. This should not happen. Please contact your server admin or the bot "
                       "author for details.")

        user = client.get_user(309771442763857931)
        try:
            await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                ctx.message.author) + " in '" + str(ctx.message.guild.name) + "' in the '" + ctx.message.channel.name +
                            f"' text channel. \nError details: '{error}'")
        except AttributeError:
            await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                ctx.message.author) + f" in DM. \nError details: '{error}'")

    # @client.command(aliases=["Debug", "debug", "enableDebugMode", "DebugMode", "debugmode", "Debugmode"])


# async def debugMode(ctx):
#     if debugger == False:
#         debugger = True
#         await ctx.send("Debugger enabled!")
#     elif debugger == True:
#         debugger = False
#         await ctx.send("Debugger disabled!")

if __name__ == "__main__":
    import sys
    import datetime
    pythonVersion = sys.version
    pythonVersion = pythonVersion.split(" ")
    pythonVersion = pythonVersion[0].replace(".", "")

    if(int(pythonVersion) < 360):
        print("This program only supports Python 3.6 or later. Please update your Python version.")
        exit()

    currentDT = datetime.datetime.now()
    currentDT = str(currentDT)
    currentDT = currentDT.split(" ")
    currentDT = currentDT[1].split(".")
    currentDT = currentDT[0]

    currentDT = SupportingFuctions.getTime()
    print(f"[{currentDT}] Initializing PixelBot v0.3.1")
    client.run(botKey)
