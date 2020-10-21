import datetime


class SupportingFuctions:
    def getTime():
        currentDT = datetime.datetime.now()
        currentDT = str(currentDT)
        currentDT = currentDT.split(" ")
        currentDT = currentDT[1].split(".")
        currentDT = currentDT[0]

        return currentDT
