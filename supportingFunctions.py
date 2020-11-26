import datetime
import os
from time import sleep
import sys


class SupportingFunctions:

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
        if os.path.exists("config-OLD.ini"):
            os.remove("config-OLD.ini")

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
            '\n;If true, the quotes.txt file will attempt to be cloned to the directory below.'
            '\ncopyQuotesToWebDirectory = False'
            '\nwebDirectory = /var/www/html/'
            '\n;Please enter the full web address that you would like to be linked when the "quote list" command is ran. '
            '\n;Not required if copyQuotesToWebDirectory is false'
            '\npublicWebAddress = null')

            os.chmod("config.ini", 0o777)
