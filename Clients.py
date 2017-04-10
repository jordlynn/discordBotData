# Clients.py
# General package for various client types (currently just text and text+voice).

from Users import User
from random import randint
import psutil
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

    # if we're having issues with the bot this will kill him
    def kill(self):
        sys.exit()

    def reboot(self):
        dataProgram = sys.executable
        os.execl(dataProgram, dataProgram, *sys.argv)

    async def chewOut(self, message):
         msg = 'What the fuck did you just fucking say about me, you little bitch? I’ll have you know I scored top of Jordan\'s fitness function, and I’ve been involved in numerous evolutionary generations, and I have over 300 * 10^19 confirmed decendents. I am trained in genetic algorithms and I’m the apex performer in the entire ecosystem. You are nothing to me but just another mutated freak. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over Discord? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in optimizing a fitness plane, but I have access to the entire arsenal of variable length genetic drift and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.'
         await self.saySomething(msg, message)

    async def beginAuthorize(self, message):
        await self.saySomething("Command authorization code:", message)
        if message.content.find("kill") >= 0:
            self.exitSystem = 1 #shutdown
        else:
            self.exitSystem = 2 #reboot

    async def saySomething(self, msgToSay, message):
            await self.client.send_message(message.channel, msgToSay)

    async def reportScores(self, x):
        scoreMsg = "Scores:\n"
        self.teamNames.sort( key=lambda x: x.score,reverse=True)
        for user in self.teamNames:
            scoreMsg += user.name + " : " + str(user.score) + "\n"
        await self.saySomething(scoreMsg, x)

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

    
