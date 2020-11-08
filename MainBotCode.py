import sys
from PyQt5.QtWidgets import QApplication, QWidget
import discord
import random
import threading
import youtube_dl
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from random import choice
from discord import utils
import asyncio
import config
import AdditionThing
import os
import interface

#_________________________________________YouTube constans part____________________________
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# __________________________________YouTube Class ____________________________________
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.4):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# __________________________________________________Main Code Thing_______________________________
class MainMessage(discord.Client):
    async def on_ready(self):
        config.SERVERS_DATA[config.name_of_bot] = {}
        for guild in self.guilds:
            config.SERVERS_DATA[config.name_of_bot][guild.id] = {'server_data': guild}
        print(self.guilds)
        interface_work = threading.Thread(target=interface.interface_start)
        interface_work.start()
        print('Запуск произошёл')

    async def on_voice_state_update(self, member, before, after):

# __________________________________DUPLICATION PART__________________________________
        print(config.duplicated_channels)
        if after.channel != before.channel:

            if after.channel and not member.bot:
                is_created = False
                new_name = after.channel.name
                for parent_key in list(config.duplicated_channels.keys()):
                    if after.channel.id in config.duplicated_channels[parent_key] or after.channel.id == parent_key:
                        if self.get_channel(parent_key).members and \
                                all([self.get_channel(id).members for id in config.duplicated_channels[parent_key]]):
                            new_channel = await after.channel.clone(name=new_name, reason=None)
                            config.duplicated_channels[parent_key].append(new_channel.id)
                        is_created = True
                        break
                if not is_created:
                    new_channel = await after.channel.clone(name=new_name, reason=None)
                    config.duplicated_channels[after.channel.id] = [new_channel.id]

            if before.channel:
                for parent_key in list(config.duplicated_channels.keys()):
                    for id in config.duplicated_channels[parent_key]:
                        channel_to_del = self.get_channel(id)
                        if len([1 for id in list(config.duplicated_channels.keys())
                                               + [parent_key] if not self.get_channel(id).members]) >= 2 and not channel_to_del.members:
                            del config.duplicated_channels[parent_key][config.duplicated_channels[parent_key].index(id)]
                            await channel_to_del.delete(reason=None)
            print(config.duplicated_channels)
            print()



    async def on_message(self, message):
        # print(f"chanel: {message.channel}\nauthor: {message.author}")
        # print(message)
        if not message.author.bot:
            pass


# _____________________________________________MUSICAL PART_______________________________________________________

        for command in config.music_commands:
            if ''.join(str(message.content).lower().split()).startswith(command) and\
                    message.channel.id in config.music_channels:
                search_for = ' '.join(str(message.content).split())[len(command):]
                url = AdditionThing.activate_url(search_for)
                info = AdditionThing.url_info(url)
                await message.channel.send(url)
                if message.author.voice.channel:
                    voice_channel_to_connect = message.author.voice.channel
                    channel_with_bot = await voice_channel_to_connect.connect(reconnect=True, timeout=1.0)
                else:
                    channel_with_bot = await self.move_to(voice_channel_to_connect)


                async with message.channel.typing():
                    player = await YTDLSource.from_url(url, loop=self.loop)
                    channel_with_bot.play(player, after=lambda e: print('Player error: %s' % e) if e else None)




    #__________________________________________REACTIONS THING_____________________________________________

    async def on_raw_reaction_add(self, payload):
        for guild_id in config.music_pyloads:
            if payload.id in config.music_pyloads[guild_id]:
                pass
        # await self.get_channel(payload.channel_id).send(payload)

    async def on_raw_reaction_remove(self, payload):
        pass
        # await self.get_channel(payload.channel_id).send(payload)




def activate(token):
    bot = MainMessage()
    bot.run(token)
    print(bot)
    config_name_of_bot = 'Бася-вот'


if __name__ == '__main__':
    activate('Njk5Mzc0OTAzNzQ4NDYwNTY0.XpTdog.fEp1K6hBLZKWhEzrQT3nJTLw06g')