import os
import asyncio
import discord
import time
from Clients import VoiceClient
from math import exp
from discord.ext import commands

# ===READ THIS===
# Using the Discord client you should have a pretty solid understanding
# of multitasking, if you're coming from javascript this is just known
# as async calls. In this API they're called 'async' if you're building
# using < python 3.5 then you'll get a bunch of syntax errors about the
# 'async' and 'await' calls. I don't want to go through and translate 
# all these, upgrade or die! Just kidding, you can go make your own branch.

# opus is a library we use to play sound files, you'll need to install it yourself.
discord.opus.load_opus
client = discord.Client()

voiceBot = VoiceClient(client)


fileName = "defnotkeys"
fileDir = os.path.dirname(os.path.realpath(__file__)) # directory to find private key file
fileDir += "/defnotkeys"
fIn = open(fileDir)
privateKey = ""
# grabs the key from local .gitignore-ed file
def assignKey():
    global privateKey
    if fIn == None:
        print("ERROR: Couldn't find key file! Message Jordan.")
        return -1 # no file found
    tmpStr = fIn.read() # grab whole file as str
    tmpStr = tmpStr.rstrip() # remove newline character
    privateKey = tmpStr[(tmpStr.find('private:') + 8):] # find 'private:' and read the key to the on of line

assignKey() # assign key

#loads any media the bot may need (sounds).
async def datasName(message):
    print(message.author.voice.voice_channel.id)
    await joinVoiceChannel(message.author.voice.voice_channel.id)
    
    player = voiceBot.voice.create_ffmpeg_player("media/dataName.mp3", use_avconv=True)
    player.start()
    time.sleep(22) # hack to get this done, update lol
    await voiceBot.voice.disconnect()

    


# puts the client in the "general" channel, right click and copy channel ID
async def joinVoiceChannel(authorChannel):
    channel = client.get_channel(authorChannel) 
    voice = await client.join_voice_channel(channel)
    voiceBot.voice = voice
    print('Bot should joined the Channel')

# Python doesn't have a switch/case statemetn -_-
# format for finding substring in messange:
# x.content.find(STRING_YOURE_LOOKING_FOR) >= 0 : FUNCTION_OR_ACTION
async def switch(x):
    if (x.content.find("top scores") >= 0):
        await voiceBot.reportScores(x)
    elif (x.content.find("my score") >= 0):
        await voiceBot.incScore(x)
    elif (x.content.startswith('data diagnostic')): 
        await voiceBot.performDiagnostic(x)
    elif (x.content.find("pronounce data") >= 0):
        await datasName(x)
    elif (x.content.find("kill yourself") >= 0):
        await voiceBot.beginAuthorize(x)
    elif (x.content.find("reboot") >= 0):
        await voiceBot.beginAuthorize(x)
    elif ((x.content.find("bitch") >= 0) or (x.content.find("fuck") >= 0) or (x.content.find("fag") >= 0)):
        await voiceBot.chewOut(x)
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
