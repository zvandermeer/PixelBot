from supportingFunctions import SupportingFunctions
import os
import datetime
from time import sleep
import sys
import platform
import configparser

pythonVersion = sys.version
pythonVersion = pythonVersion.split(" ")
pythonVersion = pythonVersion[0].replace(".", "")

if(int(pythonVersion) >= 390):
    print("Due to the Discord.py framework not currently supporting Python 3.9.0 or later, PixelBot also does not currently support Python 3.9.0 or later. Please run PixelBot on a Python version earlier than 3.9.0.")
    sleep(5)
    sys.exit()

try:
    import discord
except(ModuleNotFoundError):
    installInput = input("We have detected that the required discord.py library is not installed on your system. To install the "
          "discord.py library, use 'pip/pip3 install discord'\nWould you like to attempt to automatically install the library? (y/n)\n")
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

config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    config.read('config.ini')
else:
    SupportingFunctions.createConfig()

configVersion = config['FileDetails']['configVersion']
configVersion = configVersion.replace(".", "")
configVersion = int(configVersion)

if configVersion < 14:
    
    SupportingFunctions.createConfig()
    
botToken = config['config']['token']
commandPrefix = config['config']['prefix']

if commandPrefix == "":
    print("Please enter a prefix in the 'prefix' field in 'config.ini'")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=commandPrefix, intents=intents)

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

# cogErrorHandler
@unload.error
async def unloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        handledError = True
        await ctx.send("That cog does not exist!")
        return


@reload.error
async def reloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        handledError = True
        await ctx.send("That cog does not exist!")
        return


@load.error
async def loadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")
        handledError = True
        return


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

    elif isinstance(error, commands.MemberNotFound):
        handledError = True
        await ctx.send(f"Error: {error} Please use '{commandPrefix}help [command]' to find the proper formatting for the command.")

    elif not handledError:
        await ctx.send("An error has occurred. This should not happen. Please contact your bot admin for details.")

        user = ""

        # DM errors to user
        userID = config["config"]["errorDmUser"]
        if userID != "null":
            userID = int(userID)
            user = client.get_user(userID)
        else:
            print(f"[{currentDT}] No user is defined to DM error to, skipping.")
                  
        if user != "":
            try:
                await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                    ctx.message.author) + " in '" + str(ctx.message.guild.name) + "' in the '" + ctx.message.channel.name +
                                f"' text channel. \nError details: '{error}'")
            except AttributeError:
                await user.send("An error has occurred. Message details: \n" + f"[{currentDT}] Message was sent by " + str(
                    ctx.message.author) + f" in DM. \nError details: '{error}'")

    try:
        print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in '" + str(
            ctx.message.guild.name) + "' in the '" + ctx.message.channel.name + "' text channel.")
    except AttributeError:
        print(f"[{currentDT}] Message was sent by " + str(ctx.message.author) + " in DM")


if __name__ == "__main__":
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
    print(f"[{currentDT}] Initializing PixelBot v0.4.1")

    if botToken == "null":
        print("Bot Token not found. Please paste your botToken in the config.ini file under the 'token' field and restart the bot.")
        sleep(5)
        sys.exit()

    try:
        client.run(botToken)
    except discord.errors.LoginFailure:
        print("The token you have entered in the config.ini file is invalid. Please check to make sure you have entered a valid token.")
        sleep(5)
        sys.exit()

# TODO bot.properties file contains bot token, DM user, @everyone details (Channels to allow, on/off), Among Us role requirements, apache quote add, quote address
