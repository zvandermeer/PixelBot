from logging import debug, info
import discord
from discord.ext import commands
import PixelBotData.supportingFunctions as supportingFunctions
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"debug-{supportingFunctions.getDate()}.log")]
)

class tempInvite(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.invites = {}

    def find_invite_by_code(self, invite_list, code):

        # Simply looping through each invite in an
        # invite list which we will get using guild.invites()

        for inv in invite_list:
            
            # Check if the invite code in this element
            # # of the list is the one we're looking for
            if inv.code == code:
                # If it is, we return it.
                return inv

    @commands.command()
    async def tempInvite(self, ctx, invitedUser=""):
        if ctx.author.voice and ctx.author.voice.channel:
            voice = ctx.author.voice.channel

            discord_server_invite = await voice.create_invite(max_age=3600)

            if invitedUser == "":            
                await ctx.send(f"This is a one-time use invite link to join the voice channel you are currently in. \n**WARNING: THIS INVITE LINK WILL BE DELETED AFTER IT IS USED ONCE AND WILL EXPIRE IN ONE HOUR.**\nSend this link to whoever you would like to join!\n{discord_server_invite}")
            else:
                try:
                    invitedUser = int(invitedUser)
                    user = self.client.get_user(invitedUser)
                    await user.send(f"Hello,\nYou have been invited to temporarily join the voice channel listed below. Upon disconnecting from this voice channel, you will be kicked from the server. \n**WARNING: THIS INVITE LINK WILL BE DELETED AFTER IT IS USED ONCE AND WILL EXPIRE IN ONE HOUR.**\nClick the link below to join!\n{discord_server_invite}")
                    await ctx.send("User has been DM'ed an invite link!")
                except AttributeError:
                    await ctx.send(f"I was unable to send that user a DM. This could mean that I don't share a server with the intended recipient, or the user ID is invalid. Please manually send the user this link:\n{discord_server_invite}\n**WARNING: THIS INVITE LINK WILL BE DELETED AFTER IT IS USED ONCE AND WILL EXPIRE IN ONE HOUR.**")
                except ValueError:
                    await ctx.send(f"I was unable to send that user a DM. This could mean that I don't share a server with the intended recipient, or the user ID is invalid. Please manually send the user this link:\n{discord_server_invite}\n**WARNING: THIS INVITE LINK WILL BE DELETED AFTER IT IS USED ONCE AND WILL EXPIRE IN ONE HOUR.**")

            logging.info(f'[{supportingFunctions.getTime()}] Temp link generated: "{discord_server_invite}"')
            print(f'[{supportingFunctions.getTime()}] Temp link generated: "{discord_server_invite}"')

            # update our invite list after creating a new invite
            for guild in self.client.guilds:
                self.invites[guild.id] = await guild.invites()
        else:
            await ctx.send("You are not connected to a voice channel! Please join one before creating an invite!")

    @commands.Cog.listener()
    async def on_ready(self):      
        # Getting all the guilds the bot is in
        for guild in self.client.guilds:
            # Adding each guild's invites to our dict
            self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        # Getting the invites before the user joining
        # from our cache for this specific guild

        invites_before_join = self.invites[member.guild.id]
        
        # Getting the invites after the user joining
        # so we can compare it with the first one, and
        # see which invite uses number increased

        invites_after_join = await member.guild.invites()

        # Loops for each invite we have for the guild
        # the user joined.

        for invite in invites_before_join:
            
            # Now, we're using the function we created just
            # before to check which invite count is bigger
            # than it was before the user joined.
             
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:

                # Now that we found which link was used,
                # we will print a couple things in our console:
                # the name, invite code used the the person
                # who created the invite code, or the inviter.
                logging.info(f'Member "{member.name}" Joined')
                print(f'\n[{supportingFunctions.getTime()}] Member "{member.name}" Joined')
                logging.info(f"Invite Code: {invite.code}")
                print(f"[{supportingFunctions.getTime()}] Invite Code: {invite.code}")
                logging.info(f"Inviter: {invite.inviter}")
                print(f"[{supportingFunctions.getTime()}] Inviter: {invite.inviter}\n")

                # We will now update our cache so it's ready
                # for the next user that joins the guild

                self.invites[member.guild.id] = invites_after_join
                
                # We return here since we already found which
                # one was used and there is no point in
                # looping when we already got what we wanted

                # Check if user was invited by bot, if so add "temporary user" to them because this is
                # the only way they could have been invited by the bot

                inviter = str(invite.inviter)
                if inviter == "PixelBot#9752" or inviter == "PixelBot - Dev#4458":
                    tempRole = discord.utils.get(member.guild.roles, name="Temporary user role")
                    await member.add_roles(tempRole)
                    await invite.delete()

                return

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        # Updates the cache when a user leaves to make sure
        # everything is up to date

        self.invites[member.guild.id] = await member.guild.invites()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, preState, postState):
        if postState.channel is None and preState.channel is not None:

            tempUser = False

            for role in member.roles:
                role = str(role)
                if role == "Temporary user role":
                    tempUser = True
                
            if tempUser:
                await member.kick(reason="Temp user disconnected from VC")

def setup(client):
    client.add_cog(tempInvite(client))