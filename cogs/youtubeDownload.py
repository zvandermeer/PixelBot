import configparser
import discord
from discord.ext import commands
import os
import threading
import glob

# Example cog
class youtubeDownload(commands.Cog):

    def __init__(self, client):
        self.client = client

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.commandPrefix = config['pixelBotConfig']['prefix']

    def downloadVideo(self, type, videoURL):
        if type=="resolution":
            os.system(f'powershell.exe youtube-dl -f "bestvideo[ext=mp4][height<=?1080][fps<=?30]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
        elif type=="frames":
            os.system(f'powershell.exe youtube-dl -f "bestvideo[ext=mp4][height<=?720][fps<=?60]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
        elif type=="mp3":
            os.system(f'powershell.exe youtube-dl -x --audio-format mp3 {videoURL}')
        else:
            print("Internal Error")
        
        list_of_files = glob.glob('*')

        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Latest file: {latest_file}")

        print("post script outside if")

        


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
                    resThread = threading.Thread(target=self.downloadVideo, args=("resolution", videoURL))
                    resThread.start()
                elif priority == "fps" or priority == "frames" or priority == "framerate":
                    print("frames prio")
                    framesThread = threading.Thread(target=self.downloadVideo, args=("frames", videoURL))
                    framesThread.start()
                else:
                    print("else 1")
                    await ctx.send(f"{self.commandPrefix}youtube command usage:\n{self.commandPrefix}youtube <YouTube video URL> [Download type: mp3/mp4, default mp4] [Download priority: fps/resolution, resolution is default]\nIf resolution is the priority, then the video will be downloaded at 1080p30. If framerate is the priority, then the video will be downloaded at 720p60")
            elif downloadType == "mp3":
                print("mp3")
                audioThread = threading.Thread(target=self.downloadVideo, args=("mp3", videoURL))
                audioThread.start()
            else:
                print("else 2")
                await ctx.send(f"{self.commandPrefix}youtube command usage:\n{self.commandPrefix}youtube <YouTube video URL> [Download type: mp3/mp4, default mp4] [Download priority: fps/resolution, resolution is default]\nIf resolution is the priority, then the video will be downloaded at 1080p30. If framerate is the priority, then the video will be downloaded at 720p60")

def setup(client):
    client.add_cog(youtubeDownload(client))
