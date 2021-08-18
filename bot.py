import PixelBotData.supportingFunctions as supportingFunctions
import os
from time import sleep
import sys
import configparser
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"debug.log")]
)

logging.info(f"Initializing PixelBot v0.4.3")
print(f"[{supportingFunctions.getTime()}] Initializing PixelBot v0.4.3")

# Import discord.py library, and installing it if not found
try:
    import discord
    from discord.ext import commands
except(ModuleNotFoundError):
    logging.critical("The required Python libraries were not found on your system. Please run 'pip install -r requirements.txt' to install them")
    print(f"[{supportingFunctions.getTime()}] The required Python libraries were not found on your system. Please run 'pip install -r requirements.txt' to install them")
    sleep(5)
    sys.exit()

# checking for config file
supportingFunctions.checkConfig()

# initializing config file
config = configparser.ConfigParser()
config.read('config.ini')

# loading prefix and token from config file   
botToken = config['pixelBotConfig']['token']
commandPrefix = config['pixelBotConfig']['prefix']

if commandPrefix == "":
    logging.critical("Please enter a prefix in the 'prefix' field in 'config.ini'")
    print(f"[{supportingFunctions.getTime()}] Please enter a prefix in the 'prefix' field in 'config.ini'")
    sleep(5)
    sys.exit()

# initializing bot object
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=commandPrefix, intents=intents)

userID = config["pixelBotConfig"]["botAdmin"]
if userID != "null":
    userID = int(userID)
    user = client.get_user(userID)
else:
    logging.warning("NO USER IS SET AS THE BOT ADMIN IN 'CONFIG.INI'. CERTAIN FUNCTIONALITY OF THE BOT WILL NOT BE AVAILABLE. SET A BOT ADMIN USER IN 'CONFIG.INI' TO REMOVE THIS MESSAGE")
    print(f"[{supportingFunctions.getTime()}] WARNING: NO USER IS SET AS THE BOT ADMIN IN 'CONFIG.INI'. CERTAIN FUNCTIONALITY OF THE BOT WILL NOT BE AVAILABLE. SET A BOT ADMIN USER IN 'CONFIG.INI' TO REMOVE THIS MESSAGE")
    
    user = "null"

# cog control commands
# load cog
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully loaded!")
    logging.info("Loaded {extension} cog")
    print(f"[{supportingFunctions.getTime()}] Loaded {extension} cog")

# unload cog
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Successfully unloaded!")
    logging.info("Unloaded {extension} cog")
    print(f"[{supportingFunctions.getTime()}] Unloaded {extension} cog")

# reload cog
@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully reloaded!")
    logging.info("Reloaded {extension} cog")
    print(f"[{supportingFunctions.getTime()}] Reloaded {extension} cog")

# load cogs into bot
cogCount = 0
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cogCount += 1

        client.load_extension(f"cogs.{filename[:-3]}")

experimentalCogs = config['pixelBotConfig']['experimentalCogs']
experimentalCogs = experimentalCogs.lower()

if experimentalCogs != "true" and experimentalCogs != "false":
    logging.warning('Please enter either true or false under the "experimentalCogs" field in config.ini')
    print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "experimentalCogs" field in config.ini')
    sys.exit()

if experimentalCogs == "true":
    logging.info("You are currently running the bot with experimental cogs enabled. Experimental cogs are cogs that are still in an experimental state and may not work properly. Disable 'experimental cogs' in config.ini to remove this message.")
    print(f"[{supportingFunctions.getTime()}] You are currently running the bot with experimental cogs enabled. Experimental cogs are cogs that are still in an experimental state and may not work properly. Disable 'experimental cogs' in config.ini to remove this message.")

    for filename in os.listdir("./experimental-cogs"):
        if filename.endswith(".py"):
            cogCount += 1

            client.load_extension(f"experimental-cogs.{filename[:-3]}")


if cogCount == 0:
    logging.info("No cogs have been initialized. The bot is currently running with minimal functionality. Please put .py cog files in the 'cogs' directory.")
    print(f"[{supportingFunctions.getTime()}] No cogs have been initialized. The bot is currently running with minimal functionality. Please put .py cog files in the 'cogs' directory.")

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
    logging.error("{error}")
    print(f"[{supportingFunctions.getTime()}] {error}")
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

        # DM errors to user
        if user != "null":
            try:
                await user.send("An error has occurred. Message details: \n" + f"[{supportingFunctions.getTime()}] Message was sent by " + str(
                    ctx.message.author) + " in '" + str(ctx.message.guild.name) + "' in the '" + ctx.message.channel.name +
                                f"' text channel. \nError details: '{error}'")
            except AttributeError:
                await user.send("An error has occurred. Message details: \n" + f"[{supportingFunctions.getTime()}] Message was sent by " + str(
                    ctx.message.author) + f" in DM. \nError details: '{error}'")
        else:
            logging.warning("No user is defined to DM error to, skipping.")
            print(f"[{supportingFunctions.getTime()}] No user is defined to DM error to, skipping.")

    try:
        logging.warning("Message was sent by " + str(ctx.message.author) + " in '" + str(
            ctx.message.guild.name) + "' in the '" + ctx.message.channel.name + "' text channel.")
        print(f"[{supportingFunctions.getTime()}] Message was sent by " + str(ctx.message.author) + " in '" + str(
            ctx.message.guild.name) + "' in the '" + ctx.message.channel.name + "' text channel.")
    except AttributeError:
        logging.warning("Message was sent by " + str(ctx.message.author) + " in DM")
        print(f"[{supportingFunctions.getTime()}] Message was sent by " + str(ctx.message.author) + " in DM")


if __name__ == "__main__":

    if botToken == "null":
        logging.critical("Bot Token not found. Please paste your botToken in the config.ini file under the 'token' field and restart the bot.")
        print(f"[{supportingFunctions.getTime()}] Bot Token not found. Please paste your botToken in the config.ini file under the 'token' field and restart the bot.")
        sleep(5)
        sys.exit()

    try:
        client.run(botToken)
    except discord.errors.LoginFailure:
        logging.critical("The token you have entered in the config.ini file is invalid. Please check to make sure you have entered a valid token.")
        print("[{supportingFunctions.getTime()}] The token you have entered in the config.ini file is invalid. Please check to make sure you have entered a valid token.")
        sleep(5)
        sys.exit()
