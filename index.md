# Pixelbot


## Installation
Download the most recent release from the [releases](https://github.com/ovandermeer/PixelBot/releases) page. Once the source code is downloaded, add a file called botToken.txt to the root directory. This file should contain your bot's token, and nothing else. Then, just run bot.py and the bot will start! 
-Note: Python 3.6 or higher is required to run.

## Among Us help
The main feature of this bot is it's Among Us moderation commands. Before you can use them, a little bit of set-up on your server is required.

 1. Create a voice channnel called "Among Us"
 2. Create a role called "Among Us - Dead". Note that the bot will give this to users once they die, so don't give the role higher priority or permissions then you want your users to have
 3. You're good to go! Note that you must be using the "Among Us" voice channel while playing Among Us, otherwise the bot will not work.

Command list:
- &kill
Mention member(s) after this command to give them the role "Among Us - Dead" When a user has this role, the bot will not unmute them when &unmute is called.
Example: "&kill @NinjaPixels @bobIsCool @yay121"
- &reset
Removed the "Among Us - Dead" role from all users in the "Among Us" voice channel. Use this at the end of the round so that everyone can talk again. Also unmutes all users.
Example: "&reset"
- &mute
Mutes all users in the "Among Us" voice channel.
Example: "&mute"
- &unmute
Unmutes all users that do not have the "Among Us - Dead" role in the "Among Us" voice channel.
Example: "&unmute"
- &muteAll / unmuteAll
Mutes or unmutes all users in the "Among Us" voice channel, regardless of role.
Example: "&mute/&unmute"

## Try it before you download!
You can run PixelBot in repl.it to try it out without having to dowload it! Click the link below to try it now! 
[![Try me in repl.it!](https://repl.it/badge/github/ovandermeer/PixelBot)](https://repl.it/github/ovandermeer/PixelBot)

