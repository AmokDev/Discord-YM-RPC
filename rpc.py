from pypresence import Presence
from yandex_music import Client
from yandex_music.exceptions import UnauthorizedError
from json import load, dump
import time

import config as cfg

def getTrack():
    client = Client(cfg.access_token).init()
    queues = client.queues_list()
    last_queue = client.queue(queues[0].id)
    last_track_id = last_queue.get_current_track()
    last_track = last_track_id.fetch_track()
    tid = last_track_id.track_id
    url = f"https://music.yandex.ru/track/{tid}"
    artists = ', '.join(last_track.artists_name())
    title = last_track.title
    photo = last_track.getCoverUrl()
    return artists, title, url, photo

client_id = '1114742401878204466'
RPC = Presence(client_id)
RPC.connect() # mq

def getTimer() -> int:
    title = getTrack()[1]
    with open("config.json", "r") as f:
            data = load(f)
    track = data["track"]
    if title == track:
        return int(data["time"])
    else:
        with open("config.json", "w") as f:
            data["track"] = title
            data["time"] = time.time()
            data = dump(data, f)

while True:
    try:
        track = getTrack()
        RPC.update(
            buttons=[{"label": "Слушать", "url": track[2]}],
            state="▶ " + track[1],
            details="" + track[0],
            large_image=track[3],
            large_text="Yandex Music",
            small_image="ym_avatar",
            small_text="#NoWar",
            start=getTimer()
        )
    except (UnauthorizedError, UnicodeEncodeError):
        print("Неверный access_token!")
        print("Введите верный токен в файле config.py!")
        break
    except Exception as e:
        print(e)
        print("Отправьте скриншот ошибки DS: neynq или TG: @neynq")
        RPC.update(
            state="Сейчас ничего не играет!",
            large_image="ym_avatar",
            large_text="Yandex Music"
        )
