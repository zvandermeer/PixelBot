import configparser
import discord
from discord.ext import commands
import os
import threading
import glob
import platform
import shutil
import subprocess
import sys
import urllib.request
import json
import urllib
import time
import platform

# Example cog
class youtubeDownload(commands.Cog):

    def __init__(self, client):

        if platform.system() == "Windows":
            print("The YouTube Downloading plugin is currently not supported on Windows. Please rename the 'youtubeDownload.py' file to 'youtubeDownlad.py.disabled' or delete it entirely. Windows functionality will be added in a future update.")
            sys.exit()

        self.client = client

        # checking for required libraries
        try:
            subprocess.check_output(['which', 'ffmpeg'])
        except subprocess.CalledProcessError:
            print("FFMPEG is not installed. FFMPEG is required to download YouTube videos. You are receiving this message because you have the YouTube Downloading plugin enabled. Please run 'sudo apt install ffmpeg' to continue.")
            sys.exit()
        try:
            subprocess.check_output(['which', 'AtomicParsley'])
        except subprocess.CalledProcessError:
            print("AtomicParsley is not installed. AtomicParsley is required to download YouTube videos. You are receiving this message because you have the YouTube Downloading plugin enabled. Please run 'sudo apt install atomicparsley' to continue.")
            sys.exit()

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.commandPrefix = config['pixelBotConfig']['prefix']

    def downloadVideo(self, ctx, type, videoURL):
        if(platform.system() == "Linux" or platform.system() == "Darwin"):
            if type=="resolution":
                os.system(f'youtube-dl -f "bestvideo[ext=mp4][height<=1080][fps<=?30]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
            elif type=="frames":
                os.system(f'youtube-dl -f "bestvideo[ext=mp4][height<=?720][fps<=?60]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
            elif type=="mp3":
                os.system(f'youtube-dl -x --audio-format mp3 {videoURL}')
            else:
                print(f"Internal Error: Type = {type}")

        else:
            if type=="resolution":
                os.system(f'powershell.exe youtube-dl -f "bestvideo[ext=mp4][height<=1080][fps<=?30]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
            elif type=="frames":
                os.system(f'powershell.exe youtube-dl -f "bestvideo[ext=mp4][height<=?720][fps<=?60]+bestaudio[ext=m4a]/best[ext=mp4]/best" --embed-subs --embed-thumbnail --write-sub --add-metadata {videoURL}')
            elif type=="mp3":
                os.system(f'powershell.exe youtube-dl -x --audio-format mp3 {videoURL}')
            else:
                print(f"Internal Error: Type = {type}")

        if(platform.system() == "Linux"):
            pass
            list_of_files = glob.glob('*')

            latest_file = max(list_of_files, key=os.path.getctime)
            print(f"Latest file: {latest_file}") 

            shutil.move(f"{latest_file}", f"/var/www/html/YouTube-Downloads/{latest_file}")

            dmUser = ctx.author.id

            dmUser.send(f"Your video download is ready! Download here: {self.YouTubeDownloadAddress}/YouTube-Downloads/{latest_file}")

    @commands.command(aliases=["youtube-dl", "ytdl"])
    async def youtube(self, ctx, videoURL="emptyString", downloadType="mp4", priority="res"):
        if videoURL == "emptyString":
            await ctx.send(f"{self.commandPrefix}youtube command usage: \n{self.commandPrefix}youtube [Video URL] (Download type: mp4/mp3, default mp4) (Download type: Resolution/res:1080p30, Framerate/fps:720p60, default resolution)")

        authorID = ctx.author.id

        messageAuthor = self.client.get_user(authorID)

        priority = priority.lower()

        downloadType = downloadType.lower()

        if not videoURL.startswith("https://www.youtube.com/watch?v=") and videoURL != "emptyString":
            await ctx.send("Please enter a valid YouTube video URL! (Make sure it starts with HTTPS!)")
        elif videoURL != "emptyString":
            await messageAuthor.send("Your video is now processing. You will receive a DM here with a link to download your video once it has finished processing.")

            if "&" in videoURL:
                videoURL = videoURL.split("&")
                videoURL = videoURL[0]
            if downloadType == "mp4":
                if priority == "res" or priority == "resolution":
                    print("res prio")
                    resThread = threading.Thread(target=self.downloadVideo, args=(ctx, "resolution", videoURL))
                    resThread.start()

                elif priority == "fps" or priority == "frames" or priority == "framerate" or priority == "frame rate":
                    print("frames prio")
                    framesThread = threading.Thread(target=self.downloadVideo, args=(ctx, "frames", videoURL))
                    framesThread.start()

                    time.sleep(2)
                    for file in glob.glob("*.temp.mp4"):
                        print(file)
                else:
                    print("else 1")
                    await ctx.send(f"{self.commandPrefix}youtube command usage: \n{self.commandPrefix}youtube [Video URL] (Download type: mp4/mp3, default mp4) (Download type: Resolution/res:1080p30, Framerate/fps:720p60, default resolution)")
            elif downloadType == "mp3":
                print("mp3")
                audioThread = threading.Thread(target=self.downloadVideo, args=(ctx, "mp3", videoURL))
                audioThread.start()
            else:
                print("else 2")
                await ctx.send(f"{self.commandPrefix}youtube command usage: \n{self.commandPrefix}youtube [Video URL] (Download type: mp4/mp3, default mp4) (Download type: Resolution/res:1080p30, Framerate/fps:720p60, default resolution")

def setup(client):
    client.add_cog(youtubeDownload(client))

    #TODO 1080p60 videos wont download at 1080p, only 720p30 or 720p60, other than that everything seems to work just fine
