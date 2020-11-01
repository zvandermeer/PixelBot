from os import system
from supportingFunctions import SupportingFunctions
import os
import datetime
from time import sleep, time
import sys
import platform
import configparser

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
if os.path.exists("botProperties.ini"):
    config.read('botProperties.ini')
else:
    with open('botProperties.ini', 'w') as fp: 
        fp.write(';Please replace "null"\n[Options]\ntoken = null\n;Right click on the user profile and click "Copy ID". Paste the code below. Leave null if this is not needed.\nerrorDmUser = null\n;If true, @everyone pings will be limited to only specified channels.\nmanageAtEveryone = False\n;Usage example: (announcements,polls,notifications) DO NOT include the hash in front of the channel names.\nallowedChannelNames = null\ndeleteUnwantedPings = true\n;If true, a role named "Among Us permission" is required to use the Among Us commands\namongUsRequiresRole = False\n;If true, the quotes.txt file will attempt to be cloned to the directory two lines down.\naddQuotesToApache2Directory = False\nApache2Directory = /var/www/html/\n;Please enter the full web address that you would like to be linked when "&quote list" is ran\npublicWebAddress = null')
    print("A new botProperties.ini file has been created. Please paste your botToken in the botProperties.ini file under the 'token' field and restart the bot.")
    sleep(5)
    sys.exit()
    
botToken = config['Options']['token']

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

        user = ""

        # DM errors to user
        userID = config["Options"]["errorDmUser"]
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

    if botToken == "null":
        print("Bot Token not found. Please paste your botToken in the botProperties.ini file under the 'token' field and restart the bot.")
        sleep(5)
        sys.exit()

    try:
        client.run(botToken)
    except discord.errors.LoginFailure:
        print("The token you have entered in the botProperties.ini file is invalid. Please check to make sure you have entered a valid token.")
        sleep(5)
        sys.exit()

# TODO bot.properties file contains bot token, DM user, @everyone details (Channels to allow, on/off), Among Us role requirements, apache quote add, quote address
