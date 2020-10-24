import sys
from PyQt5.QtWidgets import QApplication, QWidget
import discord
import random
import threading
import youtube_dl
from discord import utils
import asyncio
import config
import serching_for_url
import os


class MainMessage(discord.Client):
    async def on_ready(self):
        self.is_connected = False
        print('Запущенский')

    async def on_voice_state_update(self, member, before, after):
        print(before, '\n', after)
        channel = after
        print('Присоединился')
        connected = None

    async def on_message(self, message):
        print(f"chanel: {message.channel}\nauthor: {message.author}")
        print(message)
        if not message.author.bot:
            #await message.channel.send(message.content)
            pass

# _____________________________Provisional measure for lessons ______________________________________________

        if ''.join(str(message.content).lower().split()) in config.commands_to_lesson:
            chanel, mes_cont = self.get_channel(765120036569481236), self.lesson_sender(message.content[6:])
            print(chanel)
            if chanel != message.channel:
                await message.channel.send(mes_cont)
            await chanel.send(mes_cont)

# ___________________________________________________________________________________________________________

        for command in config.music_commands:
            if ''.join(str(message.content).lower().split()).startswith(command) and\
                    message.channel.id in config.music_channels:
                # music_thread = threading.Thread(target=self.music_activate)
                # music_thread.start()
                search_for = ' '.join(str(message.content).split())[len(command):]
                url = serching_for_url.activate_url(search_for)

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
                channel_with_bot.FFmpegAudio(f"{name_of_song}.m4a", executable='ffmpeg')
                # discord.FFmpegPCMAudio(),
                #                       after=lambda e: print(f" (name) has finished playing"))

                channel_with_bot.source = discord.PCMVolumeTransformer(channel_with_bot.source)
                channel_with_bot.source.volume = 0.07

                # guild_members = message.author.quild.members

    def lesson_sender(self, lesson):
        return f'Урок {config.lesson_data[lesson]["name"]}\nНомер:' \
               f' {config.lesson_data[lesson]["indef"]}\nПароль: {config.lesson_data[lesson]["password"]}' \
               f'\nСсылка: {config.lesson_data[lesson]["url"]}'.replace('None', 'Нет информации')




def activate(token, name):
    bot = MainMessage()
    print(f'{name} is online')
    bot.run(token)

def activate_bot(token, name):
    config.SERVERS_DATA[name] = threading.Thread(target=activate, args=(token,))
    config.SERVERS_DATA[name].start()

if __name__ == '__main__':
    activate('ТОКЕН', 'Бася-вот')
