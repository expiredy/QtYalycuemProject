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
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# __________________________________________________Main Code Thing_______________________________
class MainMessage(discord.Client):
    async def on_ready(self):
        config.name_of_bot = self.user.name
        config.SERVERS_DATA[config.name_of_bot] = {}
        for guild in self.guilds:
            config.SERVERS_DATA[config.name_of_bot][guild.id] = {'server_data': guild}
        interface_work = threading.Thread(target=interface.interface_start)
        interface_work.start()
        self.music_is_looped = False

        print(f'Запуск {config.name_of_bot} произошёл')

    async def on_voice_state_update(self, member, before, after):
# __________________________________DUPLICATION PART__________________________________
        print(config.duplicated_channels)
        if after.channel != before.channel:

            if after.channel and not member.bot and after.channel.id not in config.unduplicate_pool:
                is_created = False
                new_name = after.channel.name
                for parent_key in list(config.duplicated_channels.keys()):
                    if after.channel.id in config.duplicated_channels[parent_key] or after.channel.id == parent_key:
                        if self.get_channel(parent_key).members and\
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

    async def next_song(self, channel, member):
        if config.music_data[channel.guild.id]['channel']:
            if not self.music_is_looped:
                del config.music_data[channel.guild.id]['Mdata'][0]
            if 'Mdata' in config.music_data[channel.guild.id] and config.music_data[channel.guild.id]['Mdata']:
                info = AdditionThing.url_info(config.music_data[channel.guild.id]['Mdata'][0],
                                              member)
                player = await YTDLSource.from_url(config.music_data[channel.guild.id]['Mdata'][0],
                                                   loop=self.loop, stream=info[1])
                music_message = await channel.send(embed=info[0])
                config.music_data[channel.guild.id]['channel'].pause()

                config.music_data[channel.guild.id]['channel'].play(player, after=lambda e: None)
                # self.next_song(self.get_channel(payload.channel_id), payload.member)
                config.music_payloads[channel.guild.id]['mes_id'] = music_message.id
                for emoji in [config.music_icons[key] for key in list(config.music_icons.keys())]:
                    await music_message.add_reaction(emoji)


    async def on_message(self, message):
# _____________________________________________MUSICAL PART_______________________________________________________

        for command in config.music_commands:
            if ''.join(str(message.content).lower().split()).startswith(command) and\
                    message.channel.id in config.music_channels:
                search_for = ' '.join(str(message.content).split())[len(command):]
                url = AdditionThing.activate_url(search_for)
                if message.guild.id not in config.music_data:
                    config.music_data[message.guild.id] = {}
                if message.author.voice:
                    voice_channel_to_connect = message.author.voice.channel
                    if 'channel' not in config.music_data[message.guild.id] or not\
                            config.music_data[message.guild.id]['channel']:
                        channel_with_bot = await voice_channel_to_connect.connect()
                        config.music_data[channel_with_bot.channel.guild.id]['channel'] = channel_with_bot
                    elif config.music_data[message.guild.id]['channel'].channel.id != voice_channel_to_connect.id:
                        channel_with_bot = await config.music_data[message.guild.id]\
                            ['channel'].move_to(voice_channel_to_connect)
                else:
                    await message.channel.send(random.choice(config.not_in_channel))
                    return

                if not config.music_data[message.guild.id]['channel'].is_playing():

                    if 'Mdata' in config.music_data[message.guild.id]:
                        config.music_data[message.guild.id]['Mdata'].append(url)
                    else:
                        config.music_data[message.guild.id]['Mdata'] = [url]
                    info = AdditionThing.url_info(config.music_data[message.guild.id]['Mdata'][0],
                                                  message.author)
                    player = await YTDLSource.from_url(config.music_data[message.guild.id]['Mdata'][0],
                                                       loop=self.loop, stream=info[1])
                    if config.music_data[message.author.guild.id]['channel']:
                        channel_with_bot = config.music_data[message.author.guild.id]['channel']
                    channel_with_bot.play(player, after=lambda e: None)
                    # self.next_song(message.channel, message.author))

                    music_message = await message.channel.send(embed=info[0])
                    for emoji in [config.music_icons[key] for key in list(config.music_icons.keys())]:
                        await music_message.add_reaction(emoji)
                    config.music_payloads[message.guild.id] = {'mes_id': music_message.id, 'message': music_message}
                else:
                    config.music_data[message.guild.id]['Mdata'].append(url)
                    await message.channel.send(f'Добавлено в очередь, номер -'
                                         f' {len(config.music_data[message.guild.id]["Mdata"]) - 1}')


#_________________________________________________REACTIONS THING_____________________________________________

    async def on_raw_reaction_add(self, payload):

# _____________________________________________Music _________________________________________________________
        for guild_id in config.music_payloads:
            if payload.message_id == config.music_payloads[guild_id]['mes_id']:
                if not payload.member.bot:
                    await config.music_payloads[payload.guild_id]['message'] \
                        .remove_reaction(payload.emoji, payload.member)
                emoji = payload.emoji.name
                if payload.member.id and not payload.member.bot:
                    print(payload.emoji.name)
                    if emoji == config.music_icons['stop']\
                            and config.music_data[payload.guild_id]['channel'].is_playing():
                        voice_channel = config.music_data[payload.guild_id]['channel']
                        voice_channel.pause()

                    elif emoji == config.music_icons['play']:
                        if not config.music_data[payload.guild_id]['channel']:
                            config.music_data[payload.guild_id]['channel'] =\
                                await payload.member.voice.channel.connect()
                        if config.music_data[payload.guild_id]['channel'].is_paused():
                            voice_channel = config.music_data[payload.guild_id]['channel']
                            voice_channel.resume()

                    elif emoji == config.music_icons['break']:
                        voice_channel = config.music_data[payload.guild_id]['channel']
                        voice_channel.pause()
                        config.music_data[payload.guild_id]['channel'] = None
                        await voice_channel.disconnect()

                    elif emoji == config.music_icons['loop']:
                        if config.music_data[payload.guild_id]['channel']\
                                and config.music_data[payload.guild_id]['channel'].is_playing():
                            if self.music_is_looped:
                                self.music_is_looped = False
                            else:
                                self.music_is_looped = True

                    elif emoji == config.music_icons['skip']:
                        if config.music_data[payload.guild_id]['channel'].is_playing():
                            self.music_is_looped = False
                            await self.next_song(self.get_channel(payload.channel_id), payload.member)
                    elif emoji == config.music_icons['next']:
                        await self.next_song(self.get_channel(payload.channel_id), payload.member)



#_______________________________________________Roles________________________________________________________
        try:
            pass
        except BaseException:
            pass

        # await self.get_channel(payload.channel_id).send(payload)

    async def on_raw_reaction_remove(self, payload):
# _______________________________________________Roles________________________________________________________
        try:
            pass
        except BaseException:
            pass
        # await self.get_channel(payload.channel_id).send(payload)


def activate(token):
    bot = MainMessage()
    bot.run(token)
    print(bot)


if __name__ == '__main__':
    activate('Njk5Mzc0OTAzNzQ4NDYwNTY0.XpTdog.y-IIUJjYRQz93VlLuyKGxE5PZSI')