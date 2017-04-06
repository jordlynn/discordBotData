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
async def datasName():
    await joinVoiceChannel()
    
    player = voiceBot.voice.create_ffmpeg_player("media/dataNameShort.mp3")
    player.start()

    voiceBot.voice.disconnect()


# puts the client in the "general" channel, right click and copy channel ID
async def joinVoiceChannel():
    channel = client.get_channel('246101402361790474') # TODO change to author.channel
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
        await datasName()
    elif (x.content.find("kill yourself") >= 0):
        await voiceBot.beginAuthorize(x)
    elif (x.content.find("reboot") >= 0):
        await voiceBot.beginAuthorize(x)
    else:
        await voiceBot.saySomething("Sorry I don't understand", x)

@client.event
async def on_message(message):
    # we do not want the client to reply to itself
    if message.author == client.user:
        return

    print("system value: " + str(voiceBot.exitSystem))
    if ((voiceBot.exitSystem == 1) and (message.content.find("Jordan-4-7-Alpha-Tango") >= 0)):
        await voiceBot.saySomething("shutting down...", message)
        voiceBot.kill()
    elif ((voiceBot.exitSystem == 2) and (message.content.find("Jordan-4-7-Alpha-Tango") >= 0)):
        await voiceBot.saySomething("rebooting...", message)
        voiceBot.reboot() 

    voiceBot.addMember(message.author)

    # if ((message.content.find("bitch") >= 0 or message.content.find("fuck") >= 0 or message.content.find("faggot") >= 0) and (message.content.find("data") >= 0) or (message.content.find("Data") >= 0) ):
    #     msg = 'What the fuck did you just fucking say about me, you little bitch? I’ll have you know I scored top of Jordan\'s fitness function, and I’ve been involved in numerous evolutionary generations, and I have over 300 * 10^19 confirmed decendents. I am trained in genetic algorithms and I’m the apex performer in the entire ecosystem. You are nothing to me but just another mutated freak. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over Discord? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in optimizing a fitness plane, but I have access to the entire arsenal of variable length genetic drift and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.'
    #     await client.send_message(message.channel, msg)

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
