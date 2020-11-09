import datetime
import threading
import random
import config
from re import findall
from time import sleep
import discord
from urllib import request, parse
import urllib.request
import json
import urllib
import pprint


#____________________________________________________TIMER THING_______________________________________________

def plug():
    pass


def timer_run(time_plus, condition=True, intermediate_func=plug(), args_for_intermediate_func=None, end_func=plug(),
              args_for_end_func=None, is_return=False):
    print(f"\nfrom timer: 'Timer is started, time if end - {datetime.datetime.now().time() + time_plus}'\n")
    end_time = datatime.datetime.now() + time
    while datatime.datetime.now() < end_time - 1:
        sleep(1)
        if eval(condition):
            intermediate_func()
    if args_for_end_func:
        if is_return:
            return end_func(args_for_end_func)
        else:
            end_func(args_for_end_func)
    else:
        if is_return:
            return end_func()
        else:
            end_func()


def timer_activate(time, condition=True, intermediate_func=plug(), args_for_intermediate_func=None, end_func=plug(),
              args_for_end_func=None, is_return=False):
    timer = threading.Thread(target=timer_run, args=(time, func, args))
    timer.start()


#____________________________________________URL SEARCHING_________________________________________

def fast_play():
    pass

def play():
    pass



def activate_url(serch_for):
    if not ''.join(serch_for.split()).startswith("https://www.youtube.com/watch?v="):
        html_page = request.urlopen(f"https://www.youtube.com/results?search_query="
                               f"{parse.quote('+'.join(serch_for.lower().split()))}") if not \
            serch_for.startswith('https://www.youtube.com/results?search_query=') else serch_for
        # print(html_page.read().decode())
        video_ids = findall(r"watch\?v=(\S{11})", html_page.read().decode())
        main_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        # print(video_ids)
        return main_url
    return ''.join(serch_for.split())

def events_timer():
    while True:
        now_time = datetime.datetime.now().time().strftime('%Y+%m+%d+%H+%M+%S')
        if now_time in config.events:
            print(event[now_time])

def url_parsing(video_url):
    params = {"format": "json", "url": video_url}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        return json.loads(response_text.decode())




def url_info(video_url, member):
    new_color = ''
    for _ in range(3):
        color = str(random.randint(0, 255))
        new_color += '0' * (3 - len(color)) + color
    if int(new_color) > 16777215:
        new_color = 16777215
    data_about_vid = url_parsing(video_url)
    embed = discord.Embed(title="**Сейчас играет:** " + data_about_vid['title'],
                          url=video_url,
                          description=data_about_vid['author_name'], color=int(new_color))
    embed.set_author(name=f"По заказу {member.nick}",
                     icon_url = member.avatar_url)
    embed.set_thumbnail(url=data_about_vid['thumbnail_url'])
    if 'Mdata' in config.music_data[member.guild.id]:
        for i in range(len(config.music_data[member.guild.id]['Mdata'][1:])):
            if i < 5:
                vid_info = url_parsing(config.music_data[message.guild.id]['Mdata'][i])
                embed.add_field(name=f"**{i}**.", value=f'Название: {vid_info["title"]}'
                                                        f' Автор: {vid_info["author_name"]}', inline=False)
            else:
                embed.add_field(name='И много всего другого)))')
                break
    print(data_about_vid['type'])
    return (embed, data_about_vid['type'] != 'video')

def ChoiceColor():
    pass

# async def sender(channel, text):
#     await channel.send(text)

# activate_url('Dice boi')