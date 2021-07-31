import os
import time

from telethon import TelegramClient
from telethon.tl.functions.photos import UpdateProfilePhotoRequest

TG_APP_ID = os.getenv("TG_APP_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
TG_SESSION_NAME = "session_name"


# This is our update handler. It is called when a new update arrives.
async def print_update_handler(update):
    print(update)


async def update_profile_photo_cron(client, sleep_time=10):
    photos = await client.get_profile_photos("me")
    print(f"你当前的所有的头像列表:", [p.id for p in photos], "\n")

    for p in photos:
        await client(UpdateProfilePhotoRequest(p))
        print("当前头像=", p.id)
        time.sleep(sleep_time)


async def update_forver(client):
    me = await client.get_me()
    print(f"正在为: {me.username} 循环更新头像")
    while True:
        await update_profile_photo_cron(client)


def run():
    client = TelegramClient("session_name", TG_APP_ID, TG_API_HASH)
    client.start()
    client.loop.create_task(update_forver(client))

    print("请用  Ctrl+C 来结束当前程序)")
    client.run_until_disconnected()
