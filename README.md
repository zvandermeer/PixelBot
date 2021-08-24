# Pixelbot
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

A multi-purpose moderation discord bot
## Installation
Download the most recent release from the [releases](https://github.com/ovandermeer/PixelBot/releases) page. Alternatively, download the source code of the repository to download the most recent (and likely unstable) release. Once the bot is downloaded, configure your bot using the automatically created "botConfig.ini" file. Then, just run bot.py and the bot will start! 
-Note: Python 3.6 or higher is required to run.
# Command Documentation
All commands in the list below are formatted as following:

 - [Command Prefix] [Command] [arguments]
 [Command description] 

Square brackets represent required arguments, curly represent optional arguments.

## Among Us Commands
The main feature of this bot is it's Among Us moderation commands. Before you can use them, a little bit of set-up on your server is required.

 1. Create a voice channel called "Among Us"
 2. Create a role called "Among Us - Dead". Note that the bot will give this to users once they die, so don't give the role higher priority or permissions then you want your users to have
 3. You're good to go! Note that you must be using the "Among Us" voice channel while playing Among Us, otherwise the bot will not work.

Command list:
- &kill [user(s) to kill]
Mention member(s) after this command to give them the role "Among Us - Dead" When a user has this role, the bot will not unmute them when &unmute is called.
Example: "&kill @NinjaPixels @bobIsCool @yay121"
- &reset
Removed the "Among Us - Dead" role from all users in the "Among Us" voice channel. Use this at the end of the round so that everyone can talk again. Also unmutes all users.
- &mute
Mutes all users in the "Among Us" voice channel.
- &unmute
Unmutes all users that do not have the "Among Us - Dead" role in the "Among Us" voice channel.
- &muteAll / unmuteAll
Mutes or unmutes all users in the "Among Us" voice channel, regardless of role.
## Quote Commands
- &quote
Recalls random quote from the bots quote index
- &quote "[quote]" -[quote author]
Adds quote to the bots quote index, and clones to a web directory (if configured). Quote is split on the last "-" character, and anything following it is set as the author of the quote.
- &quote add "[quote] " -[quote author]
Same as above
- &quote list
Sends a link to the full list of quotes (if configured in botconfig.ini)
## Basic user commands
- &ping
Pings the bot and lists the ping speed
- &status [status]
Changes the bots status. Can be configured to be ran by only the bot admin in config.ini. Effective until bot restart, will it will read the status from the config file again
- &resetStatus
Resets the status to what is listed in the config file
- &about
Sends details about the bot, including author, documentation, and bug reporting
- &eightBall
A basic Magic 8 Ball command
- &dice
A basic dice rolling command
- &coinFlip
A basic coin flip command
- &helloThere
Funni Star wars reference
- &messageAdmin [message]
Command that allows users to send messages to the bot admin directly. Messages will be sent as a DM from the bot, so even if users don't know who the bot admin is they can still contact them. Can be disabled from config.
## Admin Commands
- &clear [amount to clear]
Command that allows server admins to delete a specific number of messages from a channel
- &kick [user to kick]
Kicks a specified user from the server
- &ban [user to ban]
Bans a specified user from the server
- &unban [user to unban, formatted as "username#user tag"]
Unbans a specified user from the server
- &muteUser [user to mute]
Mutes a specified user in VC
- &unmuteUser [user to unmute]
Unmutes a specified user in VC
- &shutdown
Shuts down the bot. Can only be run by the Bot Admin.
## Temporary Invitation Command
Sends a one-time use invite link to join the voice channel that the inviter is currently in. The invite will be deleted after it is used, and the user will be kicked from the server upon disconnecting from the voice channel.

Can be improved on by making all channels invisible and private by default.

Useful if you want someone to join the voice chat in a server, but not allow them to actually be in the server or see any of the text channels.

### Usage:
- &tempInvite {user to temporarily invite}
If the user shares a server with the bot, then they can be mentioned/written (format: "user#user tag") and they will receive the invite link in a DM. Otherwise, the link will be sent in the chat and the user can be dmed the invite link separately.
