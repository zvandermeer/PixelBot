import discord
from discord.ext import commands
import configparser
import sys

from time import sleep

class amongUs(commands.Cog):

    def __init__(self, client):
        self.client = client
        
        self.client = client
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.amongUsRequiresRole = self.config["pixelBotConfig"]["amongUsRequiresRole"]
        self.amongUsRequiresRole = self.amongUsRequiresRole.lower()
        
        if self.amongUsRequiresRole != "true" and self.amongUsRequiresRole != "false":
            print('Please enter either true or false under the "amongUsRequiresRole" field in config.ini')
            sys.exit()
    
    @commands.command(aliases=['kill', 'die', 'k', 'K'])
    async def killPlayer(self, ctx, *, members=None):
        runCommand = False
        if self.amongUsRequiresRole == "false":
            runCommand = True
        else:
            for role in ctx.author.roles:
                    role = str(role)
                    if role == "Among Us permission":
                        runCommand = True
        
        if runCommand is True:
            if members is None:
                await ctx.send('Please mention at least one valid user!')
                return
            members = members.split(" ")

            for member in members:
                member = member[3:]
                member = member[:-1]
                member = int(member)
                memberObject = ctx.guild.get_member(member)
                deadRole = discord.utils.get(ctx.guild.roles, name="Among Us - Dead")
                await memberObject.add_roles(deadRole)
                await memberObject.edit(mute=True)        

            await ctx.send("Player(s) killed!")
        else:
            await ctx.send("This command requires the 'Among Us permission' role to run. Please make sure you have this role, and try again.")

    @commands.command(aliases=['reset', 'restart', 'r', 'R'])
    async def resetGame(self, ctx):
        runCommand = False
        if self.amongUsRequiresRole == "false":
            runCommand = True
        else:
            for role in ctx.author.roles:
                    role = str(role)
                    if role == "Among Us permission":
                        runCommand = True
        
        if runCommand is True:
            deadRole = discord.utils.get(ctx.guild.roles, name="Among Us - Dead")
            deadMembers = deadRole.members

            for member in deadMembers:
                await member.remove_roles(deadRole)           

            await self.unmuteAllUsers(ctx)

            await ctx.send("Game reset!")
        else:
            await ctx.send("This command requires the 'Among Us permission' role to run. Please make sure you have this role, and try again.")

    @commands.command(aliases=["mute", "mutea", 'm', 'M'])
    async def muteAll(self, ctx):
        runCommand = False
        if self.amongUsRequiresRole == "false":
            runCommand = True
        else:
            for role in ctx.author.roles:
                    role = str(role)
                    if role == "Among Us permission":
                        runCommand = True
        
        if runCommand is True:
            channel = discord.utils.get(ctx.guild.voice_channels, name='Among Us', bitrate=64000)
            members = channel.members

            for member in members:
                await member.edit(mute=True)          

            await ctx.send("Muted channel!")
        else:
            await ctx.send("This command requires the 'Among Us permission' role to run. Please make sure you have this role, and try again.")

    @commands.command(aliases=["umute", "unmute", 'u', 'um', 'U', 'UM'])
    async def unmuteAll(self, ctx):
        runCommand = False
        if self.amongUsRequiresRole == "false":
            runCommand = True
        else:
            for role in ctx.author.roles:
                    role = str(role)
                    if role == "Among Us permission":
                        runCommand = True
        
        if runCommand is True:
            await self.unmuteAllUsers(ctx)

            await ctx.send("Unmuted all players!")
        else:
            await ctx.send("This command requires the 'Among Us permission' role to run. Please make sure you have this role, and try again.")

    @commands.command(aliases=["umutea", "unmutea", 'ua', 'UA'])
    async def unmuteAlive(self, ctx):
        runCommand = False
        if self.amongUsRequiresRole == "false":
            runCommand = True
        else:
            for role in ctx.author.roles:
                    role = str(role)
                    if role == "Among Us permission":
                        runCommand = True
        
        if runCommand is True:
            channel = discord.utils.get(ctx.guild.voice_channels, name='Among Us', bitrate=64000)
            members = channel.members

            for member in members:
                dead = False
                for role in member.roles:
                    role = str(role)
                    if role == "Among Us - Dead":
                        dead = True               
                
                if not dead:
                    await member.edit(mute=False)

            await ctx.send("Unmuted alive players!")
        else:
            await ctx.send("This command requires the 'Among Us permission' role to run. Please make sure you have this role, and try again.")
        
    async def unmuteAllUsers(self, ctx):
        channel = discord.utils.get(ctx.guild.voice_channels, name='Among Us', bitrate=64000)
        members = channel.members

        for member in members:
            await member.edit(mute=False)


def setup(client):
    client.add_cog(amongUs(client))
