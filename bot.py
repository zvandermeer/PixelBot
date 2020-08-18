import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
from botKey import botKey

commandPrefix = "!"
client = commands.Bot(command_prefix = commandPrefix)
#status = cycle(["Status 1", "Status 2"])
debugger = False

#event
# @client.event
# async def on_ready():
#     change_status.start()

#cogs commands
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Sucessfully loaded!")
    print(f"Loaded {extension} cog")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Sucessfully unloaded!")
    print(f"Unloaded {extension} cog")

@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Sucessfully reloaded!")
    print(f"Reloaded {extension} cog")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
       client.load_extension(f"cogs.{filename[:-3]}")
print("Initializing pixelbot 0.2")

#tasks
# @tasks.loop(seconds=10)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))

#errorHandler
@client.event
async def on_command_error(ctx, error):
    print(f"{error}")
    # if debugger == True:
    #     await ctx.send(f"{error}")
    await ctx.send("An error has occured. Please contact the bot author or check the console for more details.")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command!")

#cogErrorHandler
@load.error
async def loadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to load")

@reload.error
async def reloadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to reload")

@unload.error
async def unloadBlankError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the cog you would like to unload")

@unload.error
async def unloadNonexistantError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")

@reload.error
async def reloadNonexistantError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")

@load.error
async def loadNonexistantError(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That cog does not exist!")

# @client.command(aliases=["Debug", "debug", "enableDebugMode", "DebugMode", "debugmode", "Debugmode"])
# async def debugMode(ctx):
#     if debugger == False:
#         debugger = True
#         await ctx.send("Debugger enabled!")
#     elif debugger == True:
#         debugger = False
#         await ctx.send("Debugger disabled!")
    

client.run(botKey)
