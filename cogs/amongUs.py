import discord
from discord.ext import commands

from time import sleep

class amongUs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['kill', 'die', 'k'])
    async def killPlayer(self, ctx, *, members=None):
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

    @commands.command(aliases=['reset', 'restart', 'r'])
    async def resetGame(self, ctx):
        deadRole = discord.utils.get(ctx.guild.roles, name="Among Us - Dead")
        deadMembers = deadRole.members

        for member in deadMembers:
            await member.remove_roles(deadRole)           

        await self.unmuteAllUsers(ctx)

        await ctx.send("Game reset!")

    @commands.command(aliases=["mute", "mutea", 'm'])
    async def muteAll(self, ctx):
        channel = discord.utils.get(ctx.guild.voice_channels, name='Among Us', bitrate=64000)
        members = channel.members

        for member in members:
            await member.edit(mute=True)          

        await ctx.send("Muted channel!")

    @commands.command(aliases=["umutea", "unmutea", 'ua'])
    async def unmuteAll(self, ctx):
        await self.unmuteAllUsers(ctx)

        await ctx.send("Unmuted all players!")

    @commands.command(aliases=["umute", "unmute", 'u', 'um'])
    async def unmuteAlive(self, ctx):
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

    async def unmuteAllUsers(self, ctx):
        channel = discord.utils.get(ctx.guild.voice_channels, name='Among Us', bitrate=64000)
        members = channel.members

        for member in members:
            await member.edit(mute=False)           


def setup(client):
    client.add_cog(amongUs(client))
