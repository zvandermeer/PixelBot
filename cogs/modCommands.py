import datetime
from supportingFunctions import SupportingFuctions
import discord
from discord.ext import commands
import time
import os 

exitLoop = False

class modCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #moderation commands
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clear(self, ctx, amount=0):
        if amount == 0:
            await ctx.send("Please enter a number of messages to be deleted.")
        else:
            pluralString = ""
            if amount != 1:
                pluralString = "s"
            amount += 1
            await ctx.channel.purge(limit=amount)
            amount -= 1
            await ctx.channel.send(f"{amount} message{pluralString} deleted!")
            time.sleep(2)
            await ctx.channel.purge(limit=1)
            exitLoop = True

    @commands.command()
    @commands.dm_only()
    async def dmclear(self, ctx, amount=0):
        if amount == 0:
            await ctx.send("Please enter a number of messages to be deleted.")
        else:
            pluralString = ""
            if amount != 1:
                pluralString = "s"
            amount += 1
            await ctx.channel.purge(limit=amount)
            amount -= 1
            await ctx.channel.send(f"{amount} message{pluralString} deleted!")
            time.sleep(2)
            await ctx.channel.purge(limit=1)
            exitLoop = True

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Sucessfully kicked {member.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Sucessfully banned {member.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")
        
        for banEntry in bannedUsers:
            user = banEntry.user

            if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Sucessfully unbanned {user.mention}")
                return

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["muteu"])
    async def muteUser(self, ctx, member: discord.Member = None):
        await member.edit(mute=True)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["umuteu"])
    async def unmuteUser(self, ctx, member: discord.Member = None):
        await member.edit(mute=False)

    @commands.has_permissions(administrator=True)
    @commands.has_role('Bot Admin')
    @commands.command(aliases=['quit', 'stop', 'exit'])
    async def shutdown(self, ctx):
        await ctx.send("Bot is shutting down. Please wait...")
        currentDT = SupportingFuctions.getTime()
        print(f"[{currentDT}] Shutting down PixelBot")
        quit()

    @commands.has_permissions(administrator=True)
    @commands.has_role('Bot Admin')
    @commands.command()
    async def reboot(self, ctx):
        currentDT = SupportingFuctions.getTime()
        print(f"[{currentDT}] PixelBot restarting\n\n")
        await ctx.send("Bot is rebooting. Please wait...")
        os.system("python3.8 bot.py")
        exit()

    #@commands.has_permissions(administrator=True)
    #@commands.command(aliases=['spamMe'])
    #async def spam(self, ctx):
    #    while exitLoop == False:
            #await ctx.send("@everyone get yeeted")
            #await ctx.send("You have been yote in the boat")
    #        print(f"I BE SPAMMING")
    #        await ctx.send("https://cdn.discordapp.com/attachments/440261154439168001/700080379184545802/i249711442305187847.mp4")

    #@commands.has_permissions(administrator=True)
    #@commands.command()
    #async def stopSpam(self, ctx):
    #    exitLoop = True
    #    await ctx.send("FINE")


def setup(client):
    client.add_cog(modCommands(client))
