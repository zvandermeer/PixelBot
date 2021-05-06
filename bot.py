from PixelBotData.supportingFunctions import SupportingFunctions
import os
from time import sleep
import sys
import configparser

mySupport = SupportingFunctions()

# Checking for supported python version
mySupport.checkPythonVersion()

# Import discord.py library, and installing it if not found
try:
    import discord
    from discord.ext import commands
except(ModuleNotFoundError):
    mySupport.installDiscord()

# checking for config file
mySupport.checkConfig()

# initializing config file
config = configparser.ConfigParser()
config.read('config.ini')

# loading prefix and token from config file   
botToken = config['pixelBotConfig']['token']
commandPrefix = config['pixelBotConfig']['prefix']

if commandPrefix == "":
    print("Please enter a prefix in the 'prefix' field in 'config.ini'")

# initializing bot object
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=commandPrefix, intents=intents)

# cog control commands
# load cog
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully loaded!")
    currentDT = mySupport.getTime()
    print(f"[{currentDT}] Loaded {extension} cog")

# unload cog
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Successfully unloaded!")
    currentDT = mySupport.getTime()
    print(f"[{currentDT}] Unloaded {extension} cog")

# reload cog
@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully reloaded!")
    currentDT = mySupport.getTime()
    print(f"[{currentDT}] Reloaded {extension} cog")

# load cogs into bot
cogCount = 0
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cogCount += 1

        client.load_extension(f"cogs.{filename[:-3]}")

if cogCount == 0:
    print("No cogs have been initialized. The bot is currently running with minimal functionality. Please put .py cog files in the cogs/ directory.")

# Cog error handler
@unload.error
async def unloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        # write in file that the error was handled so the error handler bypasses it
        with open('PixelBotData/cogError.txt', 'w+') as fp: 
            fp.write('cogError = True')
        await ctx.send("That cog does not exist!")

@reload.error
async def reloadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        with open('PixelBotData/cogError.txt', 'w+') as fp: 
            fp.write('cogError = True')
        await ctx.send("That cog does not exist!")

@load.error
async def loadNonExistentError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        with open('PixelBotData/cogError.txt', 'w+') as fp: 
            fp.write('cogError = True')
        await ctx.send("That cog does not exist!")


# error handler
@client.event
async def on_command_error(ctx, error):
    currentDT = mySupport.getTime()
    print(f"[{currentDT}] {error}")
    handledError = False

    if os.path.exists('PixelBotData/cogError.txt'):
        # read to see if the error was caused by a cog command
        with open('PixelBotData/cogError.txt', 'r') as fp:
            if fp.read() == "cogError = True":
                handledError = True
            with open('PixelBotData/cogError.txt', 'w') as fp:
                fp.write('cogError = False')

    if isinstance(error, commands.CommandNotFound):
        handledError = True
        await ctx.send("Invalid command!")   

    elif isinstance(error, commands.MissingRole or commands.MissingPermissions):
        handledError = True
        await ctx.send("You do not have sufficient permissions to use this command. Please contact the server "
                       "administrator if you believe this to be a mistake.")

    elif isinstance(error, commands.MissingRequiredArgument):
        handledError = True
        await ctx.send(f"You are missing arguments for this command. Type {commandPrefix}help <command> for help with the command.")

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

    # if error is not handled, run this
    elif not handledError:
        await ctx.send("An error has occurred. This should not happen. Please contact your bot admin for details.")

        user = ""

        # DM errors to user
        userID = config["pixelBotConfig"]["errorDmUser"]
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

    currentDT = mySupport.getTime()
    print(f"[{currentDT}] Initializing PixelBot v0.4.3")

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
