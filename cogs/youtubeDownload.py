import configparser
import discord
from discord.ext import commands
import os

# Example cog
class youtubeDownload(commands.Cog):

    def __init__(self, client):
        self.client = client

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.commandPrefix = config['pixelBotConfig']['prefix']

    # Example command
    @commands.command(aliases=["youtube-dl", "ytdl"])
    async def youtube(self, ctx, videoURL, downloadType="mp4", priority="res"):
        priority = priority.lower()

        downloadType = downloadType.lower()

        if not videoURL.startswith("https://www.youtube.com/watch?v="):
            await ctx.send("Please enter a valid YouTube video URL!")
        else:
            if "&" in videoURL:
                videoURL = videoURL.split("&")
                videoURL = videoURL[0]
            if downloadType == "mp4":
                if priority == "res" or priority == "resolution":
                    print("res prio")
                    os.system(f"powershell.exe ""youtube-dl -f 'bestvideo[ext=mp4][height<=?1080][fps<=?30]+bestaudio[ext=m4a]/best[ext=mp4]/best' --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}"" ")
                elif priority == "fps" or priority == "frames" or priority == "framerate":
                    print("frames prio")
                    os.system(f"powershell.exe ""youtube-dl -f 'bestvideo[ext=mp4][height<=?720][fps<=?60]+bestaudio[ext=m4a]/best[ext=mp4]/best' --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}"" ")
                else:
                    print("else 1")
                    await ctx.send(f"{self.commandPrefix}youtube command usage:\n{self.commandPrefix}youtube <YouTube video URL> [Download type: mp3/mp4, default mp4] [Download priority: fps/resolution, resolution is default]\nIf resolution is the priority, then the video will be downloaded at 1080p30. If framerate is the priority, then the video will be downloaded at 720p60")
            elif downloadType == "mp3":
                print("mp3")
                os.system(f"powershell.exe ""youtube-dl -x --audio-format mp3 {videoURL}"" ")
            else:
                print("else 2")
                await ctx.send(f"{self.commandPrefix}youtube command usage:\n{self.commandPrefix}youtube <YouTube video URL> [Download type: mp3/mp4, default mp4] [Download priority: fps/resolution, resolution is default]\nIf resolution is the priority, then the video will be downloaded at 1080p30. If framerate is the priority, then the video will be downloaded at 720p60")

def setup(client):
    client.add_cog(youtubeDownload(client))
