import asyncio
import discord
import psutil
import time
from Clients import VoiceClient
from math import exp
from discord.ext import commands

discord.opus.load_opus
client = discord.Client()

voiceBot = VoiceClient(client)

#loads any media the bot may need (sounds).
async def datasName():
    await joinVoiceChannel()
    
    player = voiceBot.voice.create_ffmpeg_player("media/dataNameShort.mp3")
    player.start()

    voiceBot.voice.disconnect()


# puts the client in the "general" channel, right click and copy channel ID
async def joinVoiceChannel():
    channel = client.get_channel('246101402361790474')
    voice = await client.join_voice_channel(channel)
    voiceBot.voice = voice
    print('Bot should joined the Channel')


@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))

# Python doesn't have a switch/case statemetn -_-
# format for finding substring in messange:
# x.content.find(STRING_YOURE_LOOKING_FOR) >= 0 : FUNCTION_OR_ACTION
async def switch(x):
    if (x.content.find("top scores") >= 0):
        await voiceBot.reportScores(x)
    elif (x.content.find("my score") >= 0):
        await voiceBot.incScore(x)
    else:
        await voiceBot.saySomething("Sorry I don't understand", x)

@client.event
async def on_message(message):
    # we do not want the client to reply to itself
    if message.author == client.user:
        return


    voiceBot.addMember(message.author)

    if message.content.startswith('data diagnostic'):
        errors = 0
        warns = 0
        THRESHOLD = 100 * 1024 * 2014 # 100MB

        tmp = psutil.sensors_temperatures(fahrenheit=False)['acpitz'][0].current
        cpuPer = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        if tmp > 50:
            errors += 1
        if cpuPer > 90 or mem.available <= THRESHOLD:
            warns += 1

        msg = 'Here\'s what I\'ve got\n'
        if(discord.opus.is_loaded()): msg += 'opus: UP\n'
        else: msg += 'opus: ❌'
        msg += 'CPU: ' + str(cpuPer) + '%\n'
        msg += 'Temp: ' + str(tmp) + '°C\n'
        msg += 'Mem: ' + str((int(mem.free) / 1024**2)) + 'MB\n'
        msg += 'names: \n'
        for names in voiceBot.teamNames:
            msg += '\t' 
            msg += names[0] 
            msg += '\n'

        if errors == 0 and warns == 0:
            msg += 'Everything looks good ✅'
        elif errors > 0:
            msg += '\nSir I\'m having SERIOUS issues can I restart?❌❌'
        elif warns > 0:
            msg += '\nSir I\'m not feeling well. ❌'
        await client.send_message(message.channel, msg)
        

    elif (message.content.find("pronounce data") >= 0):
        await datasName()

    elif ((message.content.find("bitch") >= 0 or message.content.find("fuck") >= 0 or message.content.find("faggot") >= 0) and (message.content.find("data") >= 0) or (message.content.find("Data") >= 0) ):
        msg = 'What the fuck did you just fucking say about me, you little bitch? I’ll have you know I scored top of Jordan\'s fitness function, and I’ve been involved in numerous evolutionary generations, and I have over 300 * 10^19 confirmed decendents. I am trained in genetic algorithms and I’m the apex performer in the entire ecosystem. You are nothing to me but just another mutated freak. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over Discord? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in optimizing a fitness plane, but I have access to the entire arsenal of variable length genetic drift and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.'
        await client.send_message(message.channel, msg)

    # special cases are handled lets start general messages.
    elif (message.content.startswith('data')):
        await switch(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('Mjk5MzU4NTI5MTAwNDQ3NzU0.C8cu9A.n9j2Ek5cP8gHVqgbMW6gKUR4LsA')
