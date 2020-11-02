import sys
from PyQt5.QtWidgets import QApplication, QWidget
import discord
import random
import threading
import youtube_dl
from discord import utils
import asyncio
import config
import AdditionThing
import os
import interface

class MainMessage(discord.Client):
    async def on_ready(self):
        config.SERVERS_DATA[config.name_of_bot] = self.guilds
        print(self.guilds)
        self.is_connected = False
        interface_work = threading.Thread(target=interface.interface_start)
        interface_work.start()
        print('Запуск произошёл')

    async def on_voice_state_update(self, member, before, after):

# __________________________________DUPLICATION PART__________________________________
        if after.channel != before.channel:
            if after.channel and after.channel.id not in config.unduplicate_pool:
                new_name = after.channel.name + '1'
                # for parant_key in list(config.duplicated_channels.keys()):
                #     if all([self.get_channel(channel).members for channel in config.duplicated_channels[parant_key]]):
                #         new_channel = await after.channel.clone(name=new_name, reason=None)
                #         config.duplicated_channels[parant_key].append(new_channel.id)
                # else:
                #     if after.channel.id not in config.duplicated_channels:
                #         new_channel = await after.channel.clone(name=new_name, reason=None)
                #         config.duplicated_channels[after.channel.id] = [new_channel.id]
                for parant_key in list(config.duplicated_channels.keys()):
                    if after.channel.id in config.duplicated_channels[parant_key]:
                        if all([self.get_channel(channel).members
                                for channel in config.duplicated_channels[parant_key]]) and after.channel.members:
                            new_channel = await after.channel.clone(name=new_name, reason=None)
                            config.duplicated_channels[parant_key].append(new_channel.id)
                            break
                else:
                    new_channel = await after.channel.clone(name=new_name, reason=None)
                    config.duplicated_channels[after.channel.id] = [new_channel.id]

            if before.channel:
                for parent_key in list(config.duplicated_channels.keys()):
                    if not self.get_channel(parent_key).members:
                        for id in config.duplicated_channels[parent_key]:
                            channel_to_del = self.get_channel(id)
                            if not channel_to_del.members or all([member.bot for member in channel_to_del.members]):
                                del config.duplicated_channels[parent_key][config.duplicated_channels[parent_key].index(id)]
                                await channel_to_del.delete(reason=None)
            print(config.duplicated_channels)



    async def on_message(self, message):
        print(f"chanel: {message.channel}\nauthor: {message.author}")
        print(message)
        if not message.author.bot:
            #await message.channel.send(message.content)
            pass

# _____________________________Provisional measure for lessons ______________________________________________

        # if ''.join(str(message.content).lower().split()) in config.commands_to_lesson:
        #     chanel, mes_cont = self.get_channel(765120036569481236), self.lesson_sender(message.content[6:])
        #     print(chanel)
        #     if chanel != message.channel:
        #         await message.channel.send(mes_cont)
        #     await chanel.send(mes_cont)

# _____________________________________________MUSICAL PART_______________________________________________________

        for command in config.music_commands:
            if ''.join(str(message.content).lower().split()).startswith(command) and\
                    message.channel.id in config.music_channels:
                # music_thread = threading.Thread(target=self.music_activate)
                # music_thread.start()
                search_for = ' '.join(str(message.content).split())[len(command):]
                url = AdditionThing.activate_url(search_for)

                await message.channel.send(url)
                voice_channel = message.author.voice.channel

                # voice_channel = random.choice(voice_channels)
                # voice_channel = self.get_channel(765185150165450773)
                if not self.is_connected:
                    self.is_connected = True
                    channel_with_bot = await voice_channel.connect(reconnect=True, timeout=1.0)
                else:

                    channel_with_bot = await move_to(voice_channel)
                name_of_song = ''.join([word.capitalize() for word in search_for.split()])
                song_there = os.path.isfile(f"{name_of_song}.mp3")
                try:
                    if song_there:
                        os.remove(f"{name_of_song}.mp3")
                except FermissionError:
                    print("Trying to delete song file, but it's being played")
                    return

                ydl_opts = {"format": "bestaudio/best",
                            "postprocessors":
                                [{'key': 'FFmpegExtractAudio',
                                  "preferredcodec": "mp3",
                                  'preferredquality': '192', }],
                            }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading audio nowlin")
                    try:
                        ydl.download([url])
                    except youtube_dl.utils.DownloadError:
                        pass
                channel_with_bot.FFmpegPCMAudio(f"{name_of_song}.m4a", executable='ffmpeg')
                # discord.FFmpegPCMAudio(),
                #                       after=lambda e: print(f" (name) has finished playing"))

                channel_with_bot.source = discord.PCMVolumeTransformer(channel_with_bot.source)
                channel_with_bot.source.volume = 0.07

                # guild_members = message.author.quild.members

    def lesson_sender(self, lesson):
        return f'Урок {config.lesson_data[lesson]["name"]}\nНомер:' \
               f' {config.lesson_data[lesson]["indef"]}\nПароль: {config.lesson_data[lesson]["password"]}' \
               f'\nСсылка: {config.lesson_data[lesson]["url"]}'.replace('None', 'Нет информации')

    #__________________________________________REACTIONS THING_____________________________________________

    async def on_raw_reaction_add(self, payload):
        pass

    async def on_raw_reaction_remove(self, payload):
        pass



def activate(token):
    bot = MainMessage()
    bot.run(token)
    print(bot)
    config_name_of_bot = 'Бася-вот'

# def activate_bot(token, name):
#     loop = asyncio.new_event_loop()
#     loop.run_forever(activate(token))

if __name__ == '__main__':
    # activate_bot('Токен', 'Бася-вот')
    activate('Токен')
