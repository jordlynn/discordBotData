# Clients.py
# General package for various client types (currently just text and text+voice).

from Users import User
from random import randint

# I have a few things to abstract so we'll make an object to wrap up the entire 
# client class
class VoiceClient:
    selfUser = User("Data", 0)
    testUser = User("foo", 5)
    teamNames = [selfUser, testUser]
    def __init__(self, client):
        self.voiceStatus = None
        self.client = client
        self.voice = None
        self.teamScore = None

    async def saySomething(self, msgToSay, message):
        await self.client.send_message(message.channel, msgToSay)

    async def reportScores(self, x):
        scoreMsg = "Scores:\n"
        self.teamNames.sort( key=lambda x: x.score,reverse=True)
        for user in self.teamNames:
            scoreMsg += user.name
            scoreMsg += user.name + " : " + str(user.score) + "\n"
        await self.saySomething(scoreMsg, x)

    def addMember(self, auth):
        for user in self.teamNames:
            if auth.name == user.name:
                return

        tmpUser = User(auth.name, randint(0,314159))
        self.teamNames.append(tmpUser)

    def incScore(self, auth):
        print(self.teamNames.index(auth.author.name))