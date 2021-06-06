import configparser
import datetime
import logging
import os
import platform
from time import sleep
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log")]
)

def getTime():
    currentDT = datetime.datetime.now()
    currentDT = str(currentDT)
    currentDT = currentDT.split(" ")
    currentDT = currentDT[1].split(".")
    currentDT = currentDT[0]

    return currentDT

def createConfig():
    writeConfig()

    logging.info("A new config.ini file has been created. Please paste your botToken in the config.ini file under"
    "the 'token' field and restart the bot.")
    print("A new config.ini file has been created. Please paste your botToken in the config.ini file under"
    "the 'token' field and restart the bot.")
    sleep(5)
    sys.exit()

def updateConfig():
    if os.path.exists("PixelBotData/config-OLD.ini"):
        os.remove("PixelBotData/config-OLD.ini")

    while True:
        try:
            os.rename('config.ini','config-OLD.ini')
            break
        except FileExistsError:
            os.remove('config-OLD.ini')

    sleep(2)

    writeConfig()

    logging.warning("Your config is outdated. A new config has been created. Please copy your details from 'config-OLD.ini' to 'config.ini'. "
    "Please delete the 'config-OLD.ini' file once you have updated the details. Please note the 'config-OLD.ini' will be deleted "
    "next time a config update is required.")
    print("Your config is outdated. A new config has been created. Please copy your details from 'config-OLD.ini' to 'config.ini'. "
    "Please delete the 'config-OLD.ini' file once you have updated the details. Please note the 'config-OLD.ini' will be deleted "
    "next time a config update is required.")

    sleep(5)
    sys.exit()        

def writeConfig():
    with open('config.ini', 'w+') as fp: 
        fp.write('[FileDetails]'
        '\npixelBotConfigVersion = 6'            
        '\n;Please replace "null"'
        '\n[pixelBotConfig]'
        '\ntoken = null'
        '\n;The string in the field below will become the bots prefix'
        '\nprefix = &'
        '\n;If true, the bots status will appear as "streaming". The string in the "botStatus" felid will be the status, and the string in the "streamURL" will be the linked URL'
        '\nstreamingStatus = False'
        '\n;The string in the field below will become the bots static status if dynamic status is disabled'
        '\nbotStatus = Version 0.4.3'
        '\n;Please make sure this is a Twitch or YouTube link if streamingStatus = True. Otherwise, the status will revert to a default status'
        '\nstreamURL = null'
        '\n;Allows users to use the "changeStatus" command to change the bots status. Ignored if "dynamicBotStatus" is set to true.'
        '\nstatusChangeCommand = False'
        '\n;If true, a role named "Bot Admin" will be required to change the bots status'
        '\nstatusChangeRequiresRole = True'
        '\n;DMs a new user a custom welcome message when they join a server with the bot'
        '\nDMnewUsers = True'
        '\n;Enter the message you would like to DM a new user below. Use {member} to put the members username in the message'
        '\nnewUserWelcome = Welcome {member}, to my server!'
        '\n;Right click on the user profile and click "Copy ID". Paste the code below. Leave null if this is not needed.'
        '\nerrorDmUser = null'
        '\n;If true, @everyone pings will be limited to only specified channels.'
        '\nmanageAtEveryone = False'
        '\n;Usage example: (announcements,polls,notifications) DO NOT include the hash in front of the channel names.'
        '\nallowedChannelNames = null'
        '\ndeleteUnwantedPings = True'
        '\n;If true, a role named "Among Us permission" is required to use the Among Us commands'
        '\namongUsRequiresRole = False'
        '\n;If true, a role named "Bot Admin" will be required to reboot or stop the bot'
        '\nbotShutdownRequiresRole = True'
        '\n;If true, the PixelBotData/quotes.txt file will attempt to be cloned to the directory below.'
        '\ncopyQuotesToWebDirectory = False'
        '\nwebDirectory = /var/www/html/'
        '\n;Please enter the full web address that you would like to be linked when the "quote list" command is ran. '
        '\n;Not required if copyQuotesToWebDirectory is false'
        '\npublicWebAddress = null'
        '\n;Prefix address that the bot will provide when returning a download link for a downloaded YouTube video'
        '\nYouTubeDownloadAddress = null')

        os.chmod("config.ini", 0o777)

def installDiscord():
    installInput = input("We have detected that the required discord.py library is not installed on your system. To install the "
        "discord.py library, use 'pip/pip3 install discord'\nWould you like to attempt to automatically install the library? (y/n)\n")
    installInput = installInput.lower()
    if installInput == "y":
        if(platform.system() == "Linux" or platform.system() == "Darwin"):
            try:
                os.system("pip3 install discord")
            except:
                logging.error("An unknown error occurred. Please attempt to install manually by typing 'pip3 install discord' into your terminal.")
                print("An unknown error occurred. Please attempt to install manually by typing 'pip3 install discord' into your terminal.")
                sys.exit()
            logging.info("\nInstall success! Rebooting...\n")
            print("\nInstall success! Rebooting...\n")
            os.system("python3 bot.py")
            sys.exit()
        else:
            try:
                os.system("pip install discord")
            except:
                logging.error("An unknown error occurred. Please attempt to install manually by typing 'pip install discord' into your terminal.")
                print("An unknown error occurred. Please attempt to install manually by typing 'pip install discord' into your terminal.")
                sys.exit()
            logging.info("\nInstall success! Rebooting...\n")
            print("\nInstall success! Rebooting...\n")
            os.system("python bot.py")
            sys.exit()
    logging.warning("Please ensure the discord.py library is installed before continuing. Use 'pip/pip3 install discord'")
    print("Please ensure the discord.py library is installed before continuing. Use 'pip/pip3 install discord'")
    sys.exit()

def logPrintStatements(message):
    pass

def checkConfig():
    config = configparser.ConfigParser()
    if os.path.exists("config.ini"):
        config.read('config.ini')
    else:
        createConfig()

    pixelBotConfigVersion = config['FileDetails']['pixelBotConfigVersion']
    pixelBotConfigVersion = int(pixelBotConfigVersion)

    if pixelBotConfigVersion < 6:
        updateConfig()
