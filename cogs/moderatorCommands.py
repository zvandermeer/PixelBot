import discord
from discord.ext import commands
import time

class ModCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #moderation commands
    @commands.command()
    async def clear(self, ctx, amount=0):
        if amount == 0:
            await ctx.send("Please enter the number of messages to be deleted")
        else:
            amount += 1
            await ctx.channel.purge(limit=amount)
            amount -= 1
            await ctx.channel.send(f"{amount} messages deleted!")
            time.sleep(2)
            await ctx.channel.purge(limit=1)

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Sucessfully kicked {member.mention}")

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Sucessfully banned {member.mention}")

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

def setup(client):
    client.add_cog(ModCommands(client))