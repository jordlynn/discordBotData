# Clients.py
# General package for various client types (currently just text and text+voice).

from Users import User
from random import randint
import psutil
import discord

# I have a few things to abstract so we'll make an object to wrap up the entire 
# client class, maybe we can extend it?
class VoiceClient(discord.client):
    selfUser = User("Data", 0)
    testUser = User("foo", 5)
    teamNames = [selfUser, testUser]
    def __init__(self, client):
        self.voiceStatus = None
        self.client = client
        self.voice = None
        self.teamScore = None
        self.errors = 0
        self.warns = 0

    async def saySomething(self, msgToSay, message):
        await self.client.send_message(message.channel, msgToSay)

    async def reportScores(self, x):
        scoreMsg = "Scores:\n"
        self.teamNames.sort( key=lambda x: x.score,reverse=True)
        for user in self.teamNames:
            scoreMsg += user.name
            scoreMsg += user.name + " : " + str(user.score) + "\n"
        await self.saySomething(scoreMsg, x)

    async def performDiagnostic(self, message):
        THRESHOLD = 100 * 1024 * 2014 # 100MB

        tmp = psutil.sensors_temperatures(fahrenheit=False)['acpitz'][0].current
        cpuPer = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        if tmp > 50:
            self.errors += 1
        if cpuPer > 90 or mem.available <= THRESHOLD:
            self.warns += 1

        msg = 'Here\'s what I\'ve got\n'
        if(discord.opus.is_loaded()): msg += 'OPUS: ✓\n'
        else: msg += 'OPUS: ❌'
        msg += 'CPU: ' + str(cpuPer) + '%\n'
        msg += 'Temp: ' + str(tmp) + '°C\n'
        msg += 'Mem: ' + str(int(int(mem.free) / 1024**2)) + 'MB\n'
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

    