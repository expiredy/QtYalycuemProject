from urllib import request, parse
from re import findall
from discord import utils
from discord.ext import commands
import MainBotCode
import config

def fast_play():
    pass

def play():
    pass



def activate_url(serch_for):
    if not ''.join(serch_for.split()).startswith("https://www.youtube.com/watch?v="):
        html = request.urlopen(f"https://www.youtube.com/results?search_query="
                               f"{parse.quote('+'.join(serch_for.lower().split()))}") if not \
            serch_for.startswith('https://www.youtube.com/results?search_query=') else serch_for
        # print(html.read().decode())
        video_ids = findall(r"watch\?v=(\S{11})", html.read().decode())
        main_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        # print(video_ids)
        return main_url
    return ''.join(serch_for.split())

# async def sender(channel, text):
#     await channel.send(text)

# activate_url('Dice boi')