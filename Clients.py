# Clients.py
# General package for various client types (currently just text and text+voice).

from Users import User
from random import randint
from payClient import amznPay
import discord
import socket
import sys
import os


# I have a few things to abstract so we'll make an object to wrap up the entire 
# client class, maybe we can extend it?
class VoiceClient:
    selfUser = User("Data", 0)
    testUser = User("foo", 5)
    teamNames = [selfUser, testUser]
    exitSystem = 0 # zero for standby, 1 for authorizing

    # 'constructor' if you wanna call it that.
    def __init__(self, client):
        self.voiceStatus = None
        self.client = client
        self.voice = None
        self.teamScore = None
        self.errors = 0
        self.warns = 0
        self.payClient = amznPay()

    # if we're having issues with the bot this will kill him
    def kill(self):
        sys.exit()

    async def unknownCovo(self, message):
        tmpmsg = "Sorry I don't understand, but I'm "
        await self.saySomething(tmpmsg, message)
        
    async def beginAuthorize(self, message):
        await self.saySomething("Command authorization code:", message)
        if message.content.find("kill") >= 0:
            self.exitSystem = 1 #shutdown
        else:
            self.exitSystem = 2 #reboot

    async def saySomething(self, msgToSay, message):
            await self.client.send_message(message.channel, msgToSay)

    async def pizzaRoutine(self, message):
        await self.saySomething("alright ordering your regular...", message)
        self.payClient.SetORD()

    async def performDiagnostic(self, message):
    
        tmp = os.popen('vcgencmd measure_temp').readline()
        tmp = tmp.replace("temp=","").replace("'C\n","")
        cpuPer = psutil.cpu_percent(interval=1)
        mem = str(psutil.virtual_memory().percent)
        if float(tmp) > 70:
            self.errors += 1
        if cpuPer > 80 or psutil.virtual_memory().percent > 50:
            self.warns += 1

        msg = 'Here\'s what I\'ve got\n'
        if(discord.opus.is_loaded()): msg += 'OPUS: ✓\n'
        else: msg += 'OPUS: ❌'
        msg += 'I\'m on: ' + socket.gethostname() + '\n'
        msg += 'CPU: ' + str(cpuPer) + '%\n'
        msg += 'Temp: ' + str(tmp) + '°C\n'
        msg += 'Mem: ' + mem + '%\n'
        msg += 'Tracking ' + str(len(self.teamNames)) + ' users.\n'

        if self.errors == 0 and self.warns == 0:
            msg += 'Everything looks good ✅'
        elif self.errors > 0:
            msg += '\nSir I\'m having SERIOUS issues can I restart?❌❌'
        elif self.warns > 0:
            msg += '\nSir I\'m not feeling well. ❌'
        await self.client.send_message(message.channel, msg)

    def addMember(self, auth):
        for user in self.teamNames:
            if auth.name == user.name:
                return

        tmpUser = User(auth.name, randint(0,314159))
        self.teamNames.append(tmpUser)

    def incScore(self, auth):
        print(self.teamNames.index(auth.author.name))

    