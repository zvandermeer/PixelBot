import configparser
import datetime
import os
from sys import platform
from time import sleep
import sys


class SupportingFunctions:
    def __init__(self):
        pass

    def getTime(self):
        currentDT = datetime.datetime.now()
        currentDT = str(currentDT)
        currentDT = currentDT.split(" ")
        currentDT = currentDT[1].split(".")
        currentDT = currentDT[0]

        return currentDT

    def createConfig(self):
        self.writeConfig()

        print("A new config.ini file has been created. Please paste your botToken in the config.ini file under"
        "the 'token' field and restart the bot.")
        sleep(5)
        sys.exit()

    def updateConfig(self):
        if os.path.exists("PixelBotData/config-OLD.ini"):
            os.remove("PixelBotData/config-OLD.ini")

        os.rename('config.ini','config-OLD.ini')

        self.writeConfig

        print("Your config is outdated. A new config has been created. Please copy your details from 'config-OLD.ini' to 'config.ini'. "
        "Please delete the 'config-OLD.ini' file once you have updated the details. Please note the 'config-OLD.ini' will be deleted "
        "next time a config update is required.")

        sleep(5)
        sys.exit()        

    def writeConfig(self):
        with open('config.ini', 'w+') as fp: 
            fp.write('[FileDetails]'
            '\nconfigVersion = 1.4'            
            '\n;Please replace "null"'
            '\n[config]'
            '\ntoken = null'
            '\n;The string in the field below will become the bots prefix'
            '\nprefix = &'
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
            '\npublicWebAddress = null')

            os.chmod("config.ini", 0o777)

    def installDiscord(self):
        installInput = input("We have detected that the required discord.py library is not installed on your system. To install the "
          "discord.py library, use 'pip/pip3 install discord'\nWould you like to attempt to automatically install the library? (y/n)\n")
        installInput = installInput.lower()
        if installInput == "y":
            if(platform.system() == "Linux" or platform.system() == "Darwin"):
                os.system("pip3 install discord")
                os.system("python3 bot.py")
                sys.exit()
            else:
                os.system("pip install discord")
                os.system("python bot.py")
                sys.exit()
        print("Please ensure the discord.py library is installed before continuing. Use 'pip/pip3 install discord'")
        sys.exit()

    def checkPythonVersion(self):
        pythonVersion = sys.version
        pythonVersion = pythonVersion.split(" ")
        pythonVersion = pythonVersion[0].replace(".", "")

        if(int(pythonVersion) >= 390):
            print("Due to the Discord.py framework not currently supporting Python 3.9 or later, PixelBot also does not currently support Python 3.9 or later. Please run PixelBot on a Python version earlier than 3.9.")
            sleep(5)
            sys.exit()
        if(int(pythonVersion) < 360):
                print("This program only supports Python 3.6 or later. Please update your Python version.")
                sys.exit()

    def checkConfig(self):
        config = configparser.ConfigParser()
        if os.path.exists("config.ini"):
            config.read('config.ini')
        else:
            self.createConfig()

        configVersion = config['FileDetails']['configVersion']
        configVersion = int(configVersion)

        if configVersion < 3:  
            self.updateConfig()

