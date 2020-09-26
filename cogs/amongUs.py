import discord
from discord.ext import commands


class AmongUs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['kill', 'die'])
    async def moveToDead(self, ctx, member : discord.Member = None):
        if member is None:
            await ctx.send('Please pass in a valid user')
            return

        deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us - Dead', bitrate=64000)
        await member.move_to(deadChannel)

    @commands.command(aliases=['revive', 'alive'])
    async def moveToAlive(self, ctx, member : discord.Member = None):
        if member is None:
            await ctx.send('Please pass in a valid user')
            return

        aliveChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us - Alive', bitrate=64000)
        await member.move_to(aliveChannel)

    @commands.command(aliases=["muteu"])
    async def muteUser(self, ctx, member : discord.Member = None):
        await member.edit(mute=True)

    @commands.command(aliases=["umuteu"])
    async def unmuteUser(self, ctx, member : discord.Member = None):
        await member.edit(mute=False)

    @commands.command(aliases=["mute", "mutea"])
    async def muteAll(self, ctx):
        channel = self.client.get_channel(759234633647915009)
        members = channel.members

        for member in members:
            await member.edit(mute=True)

    @commands.command(aliases=["umute", "umutea"])
    async def unmuteAll(self, ctx):
        channel = self.client.get_channel(759234633647915009)
        members = channel.members

        for member in members:
            await member.edit(mute=False)


def setup(client):
    client.add_cog(AmongUs(client))
