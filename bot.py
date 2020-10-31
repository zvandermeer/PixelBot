from os import system
from supportingFunctions import SupportingFunctions
import os
import datetime
from time import sleep
import sys
import platform

try:
    import discord
except(ModuleNotFoundError):
    installInput = input("We have detected that the required discord.py library is not installed on your system. To install the "
          "discord.py library, use 'pip/pip3 install discord'\nWould you like to attempt to automatically install the library? (y/n)")
    installInput = installInput.lower()
    if installInput == "y":
        if(platform.system() == "Linux" or platform.system() == "Darwin"):
            os.system("pip3 install discord")
            os.system("python3 bot.py")
            sys.exit()
        else:
            os.system("pip install discord")
            os.system("python bot.py")
            sys.exit()
    print("Please ensure the discord.py library is installed before continuing. Use 'pip/pip3 install discord'")
    sys.exit()

from discord.ext import commands, tasks

try:
    with open('botToken.txt', 'r') as file:
        botKey = file.read()
except(FileNotFoundError):
    with open('botToken.txt', 'w') as fp: 
        pass
    print(
        "Please open the 'botToken.txt' file and input the token for your bot. Please do not include any other text in "
        "this file.")
    sleep(5)
    sys.exit()

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
    currentDT = SupportingFunctions.getTime()
    print(f"[{currentDT}] Loaded {extension} cog")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Successfully unloaded!")
    currentDT = SupportingFunctions.getTime()
    print(f"[{currentDT}] Unloaded {extension} cog")


@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully reloaded!")
    currentDT = SupportingFunctions.getTime()
    print(f"[{currentDT}] Reloaded {extension} cog")

cogCount = 0

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cogCount = cogCount + 1

        client.load_extension(f"cogs.{filename[:-3]}")

if cogCount == 0:
    pass

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
    currentDT = SupportingFunctions.getTime()
    print(f"[{currentDT}] {error}")
    # if debugger == True:
    #     await ctx.send(f"{error}")
    handledError = False
    if isinstance(error, commands.CommandNotFound):
        handledError = True
        await ctx.send("Invalid command!")   

    elif isinstance(error, commands.MissingRole or commands.MissingPermissions):
        handledError = True
        await ctx.send("You do not have sufficient permissions to use this command. Please contact the server "
                       "administrator if you believe this to be a mistake.")

    elif isinstance(error, commands.MissingRequiredArgument):
        handledError = True
        await ctx.send("You are missing arguments for this command. Type !help <command> for help with the command.")

    elif isinstance(error, commands.MissingRole):
        handledError = True
        await ctx.send("You are missing the required role to run this command Please contact the server administrator "
                       "for more information and if you believe this to be a mistake.")

    elif isinstance(error, commands.MissingPermissions):
        handledError = True
        await ctx.send("You are missing the required permissions to run this command. Please contact the server "
                       "administrator for more information and if you believe this to be a mistake")

    elif isinstance(error, commands.NoPrivateMessage):
        handledError = True
        await ctx.send("This command cannot be used in a DM. This may mean that the command requires specific "
                       "permissions, or is simply restricted from running in a DM. Please attempt to run this command"
                       " in a server.")

    elif not handledError:
        await ctx.send("An error has occurred. This should not happen. Please contact your server admin or the bot "
                       "author for details.")

        # DM errors to user
        try:
            with open('errorDM.txt', 'r') as dmFile:
                userID = dmFile.read()

            user = client.get_user(userID)
        except(FileNotFoundError):
            print("There is no errorDM.txt file found. To DM bot errors to a user, please add a errorDM.txt file with "
                  "the userID and nothing else in the file.")

        try:
            await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                ctx.message.author) + " in '" + str(ctx.message.guild.name) + "' in the '" + ctx.message.channel.name +
                            f"' text channel. \nError details: '{error}'")
        except AttributeError:
            await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                ctx.message.author) + f" in DM. \nError details: '{error}'")

    try:
        print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in '" + str(
            ctx.message.guild.name) + "' in the '" + ctx.message.channel.name + "' text channel.\n")
    except AttributeError:
        print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in DM\n")

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
        sys.exit()

    currentDT = datetime.datetime.now()
    currentDT = str(currentDT)
    currentDT = currentDT.split(" ")
    currentDT = currentDT[1].split(".")
    currentDT = currentDT[0]

    currentDT = SupportingFunctions.getTime()
    print(f"[{currentDT}] Initializing PixelBot v0.4.0")
    client.run(botKey)

# TODO bot.properties file contains bot token, DM user, @everyone details (Channels to allow, on/off), Among Us role requirements, apache quote add, quote address

# TODO fix out of range error for quote command