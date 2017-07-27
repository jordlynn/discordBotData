import os
import discord
from discord.ext import commands
from Clients import VoiceClient

discord.opus.load_opus
client = discord.Client()

fileName = "defnotkeys"
fileDir = os.path.dirname(os.path.realpath(__file__)) # directory to find private key file
fileDir += "/defnotkeys"
fIn = open(fileDir)
privateKey = ""


voiceBot = VoiceClient(client)

def assignKey():
    global privateKey
    if fIn == None:
        print("ERROR: Couldn't find key file! Message Jordan.")
        return -1 # no file found
    tmpStr = fIn.read() # grab whole file as str
    tmpStr = tmpStr.rstrip() # remove newline character
    privateKey = tmpStr[(tmpStr.find('private:') + 8):] # find 'private:' and read the key to the on of line

assignKey() # assign key

async def joinVoiceChannel(authorChannel):
    channel = client.get_channel(authorChannel) 
    voice = await client.join_voice_channel(channel)
    voiceBot.voice = voice
    print('Bot should joined the Channel')

async def switch(x):
    if (x.content.find("pizza plox") >= 0):
        await voiceBot.pizzaRoutine(x)
    else:
        await voiceBot.unknownCovo(x)

@client.event
async def on_message(message):
    # we do not want the client to reply to itself
    if message.author == client.user:
        return

    if ((voiceBot.exitSystem == 1) and (message.content.find("Jordan-4-7-Alpha-Tango") >= 0)):
        await voiceBot.saySomething("shutting down...", message)
        voiceBot.kill()
    elif ((voiceBot.exitSystem == 2) and (message.content.find("Jordan-4-7-Alpha-Tango") >= 0)):
        await voiceBot.saySomething("rebooting...", message)
        voiceBot.reboot() 

    voiceBot.addMember(message.author)

    # special cases are handled lets start general messages.
    if (message.content.startswith('data') or message.content.startswith('Data')):
        await switch(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(privateKey)