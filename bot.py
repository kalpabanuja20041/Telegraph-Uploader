# < (c) 2021 @Godmrunal >
#Developed by @Botz_Official
#copy with credit

import logging
import os
from os import remove
import requests
from decouple import config
from telethon import Button, TelegramClient, events
from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions
mdnoor = "SHASA"
TMP_DOWNLOAD_DIRECTORY = "./"
telegraph = Telegraph()
r = telegraph.create_account(short_name=mdnoor)
auth_url = r["auth_url"]



logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

bot = TelegramClient(None, api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e").start(
    bot_token=config("BOT_TOKEN")
)

logging.info("Starting bot...")


@bot.on(events.NewMessage(incoming=True, pattern="^/start"))
async def start_(event):
    await event.reply(
        "Hi {}!\nI am a Telegraph Uploader Bot Commands\n`/tm<reply to media>`\n`/txt <reply to text>`. \n\n**Usage:** This bot will help to get Telegraph Link of Media or Text!".format(
            (await bot.get_entity(event.sender_id)).first_name
        ),
        buttons=[
            [
                Button.url("Repo🌟", url="https://github.com/msy1717/Telegraph-Uploader"),
                Button.url(
                    "Developer⚡️", url="https://t.me/Godmrunal"
                ),
            ],
            [Button.url("Channel🌈", url="https://t.me/Botz_Official")],
        ],
    )

@bot.on(events.NewMessage(pattern="^/t(m|xt) ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "m":
            downloaded_file_name = await bot.download_media(
                r_message,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit("Uploaded to https://telegra.ph{}".format(media_urls[0]), link_preview=True)
        elif input_str == "xt":
            user_object = await bot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await bot.download_media(
                    r_message,
                    TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.reply("Pasted to https://telegra.ph/{} in {} seconds.".format(response["path"], ms), link_preview=True)
    else:
        await event.reply("Reply to a message to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


logging.info("\n\nBot has started.\n(c) @Godmrunal")

bot.run_until_disconnected()
