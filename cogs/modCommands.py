import configparser
import datetime
import PixelBotData.supportingFunctions as supportingFunctions
import discord
from discord.ext import commands
import time
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"debug-{supportingFunctions.getDate()}.log")]
)

exitLoop = False

class modCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.botShutdownRequiresRole = self.config["pixelBotConfig"]["botShutdownRequiresRole"]
        self.botShutdownRequiresRole = self.botShutdownRequiresRole.lower()
        
        if self.botShutdownRequiresRole != "true" and self.botShutdownRequiresRole != "false":
            logging.warning('Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            print(f'[{supportingFunctions.getTime()}] Please enter either true or false under the "botShutdownRequiresRole" field in config.ini')
            sys.exit()

    #moderation commands
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clear(self, ctx, amount=0):        
        if amount == 0:
            await ctx.channel.send("Please enter a number of messages to be deleted.")
        else:
            if amount > 150:
                await ctx.channel.send("PixelBot does not support clearing more than 150 messages at once due to bot overload issues. If you need to clear more than this, please execute multiple commands in succession.")

            pluralString = ""
            if amount != 1:
                pluralString = "s"
            amount += 1

            if amount > 5:
                logging.debug(f"Over 5. Pre-calculation: {amount}")
                calculateAmount = amount / 5.0
                calculateAmount = round(calculateAmount, 1)
                logging.debug(f"Over 5. Post-calculation: {calculateAmount}")
                overFive = True
            else:
                calculateAmount = amount
                logging.debug(f"Under 5. No calculation: {calculateAmount}")
                overFive = False
                

            looping = True

            while looping:
                logging.debug("loop top")
                if overFive:
                    if calculateAmount >= 1.0:
                        logging.debug("enter purge")
                        await ctx.channel.purge(limit=5)
                        logging.debug("begining timeout")
                        time.sleep(2.5)
                        logging.debug("Timeout complete")
                        logging.debug(f"Over 1. Pre-calculate amount: {calculateAmount}")
                        calculateAmount = calculateAmount - 1
                        calculateAmount = round(calculateAmount, 1)
                        logging.debug(f"Over 1. Post-calculate amount: {calculateAmount}")
                    elif calculateAmount != 0:
                        logging.debug(f"Under 1. Pre-calculation: {calculateAmount}")
                        calculateAmount = calculateAmount * 5
                        calculateAmount = round(calculateAmount)
                        logging.debug(f"Under 1. Post-calculation: {calculateAmount}")
                        await ctx.channel.purge(limit=calculateAmount)
                        looping = False
                    elif calculateAmount == 0:
                        looping = False
                        logging.debug("0. Finished clear.")
                else:
                    await ctx.channel.purge(limit=calculateAmount)
                    looping = False

            amount -= 1
            await ctx.channel.send(f"{amount} message{pluralString} deleted!")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Successfully kicked {member.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Successfully banned {member.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")
        
        for banEntry in bannedUsers:
            user = banEntry.user

            if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Successfully unbanned {user.mention}")
                return

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["muteu"])
    async def muteUser(self, ctx, member: discord.Member = None):
        await member.edit(mute=True)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["umuteu"])
    async def unmuteUser(self, ctx, member: discord.Member = None):
        await member.edit(mute=False)

    @commands.command(aliases=['quit', 'stop', 'exit'])
    async def shutdown(self, ctx):
        runCommand = False
        if self.botShutdownRequiresRole == "false":
            runCommand = True
        else:
            if ctx.message.author == self.client.get_user(self.botAdmin):
                runCommand = True
        
        if runCommand == True:
            await ctx.send("Bot is shutting down. Please wait...")
            logging.info("Shutting down PixelBot")
            print(f"[{supportingFunctions.getTime()}] Shutting down PixelBot")
            quit()
        else:
            await ctx.send("Only the bot admin can run this command. please contact your bot admin if you believe this to be a mistake")

def setup(client):
    client.add_cog(modCommands(client))
