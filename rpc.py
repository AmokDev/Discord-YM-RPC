from pypresence import Presence
from yandex_music import Client
from yandex_music.exceptions import UnauthorizedError
import time

from config import access_token

def getTrack():
    client = Client(access_token).init()
    queues = client.queues_list()
    last_queue = client.queue(queues[0].id)
    last_track_id = last_queue.get_current_track()
    last_track = last_track_id.fetch_track()
    artists = ', '.join(last_track.artists_name())
    title = last_track.title
    return artists, title

client_id = '1079901231817965598'
RPC = Presence(client_id)
RPC.connect()

while True:
    try:
        track = getTrack()
        RPC.update(
            state="▶ " + track[1],
            details="" + track[0],
            large_image="ym_avatar",
            large_text="Yandex Music"
        )
    except (UnauthorizedError, UnicodeEncodeError):
        print("Неверный access_token!")
        print("Введите верный токен в файле config.py!")
        break
    except:
        RPC.update(
            state="Сейчас ничего не играет!",
            large_image="ym_avatar",
            large_text="Yandex Music"
        )
    time.sleep(15)
