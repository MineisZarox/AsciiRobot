import sys
import traceback
import asyncio 
import random
import pickle
from datetime import datetime
from ..utilities.decorators import check_auth
from telethon import events, Button
from .. import ascii, Vars
from telethon.errors import rpcbaseerrors

async def chrloop(rl, user):
    l = 0
    while l <= 600:
        rloop = ""
        for _ in range(36):
            ir = random.randint(33, 11000)
            char = chr(ir)
            rloop += f"{char}"
        rloop += "    "
        await rl.edit(
            f"Hi [{user.first_name}](tg://user?id={user.id})\nI'm ascii bot to encode any given text in unicode characters[\u200d](https://telegra.ph/file/d2adbd7a528b847e724b7.jpg)\nStart with /help\n\n{rloop}",
            buttons=[
                [
                    Button.switch_inline(
                        "Try inline", query=""
                    )
                ],
                [Button.url("Updates", "https://t.me/execal")],
                [Button.url("Dev", "https://t.me/zarox")],
            ],
            link_preview=True
        )
        await asyncio.sleep(0.2)
        l += 600

@ascii.on(events.NewMessage(incoming=True, pattern=f"^/ping({Vars.BOT_USERNAME})$"))
async def ping(event):
    start = datetime.now()
    ping = await event.reply("ᴘɪɴɢ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await ping.edit(f"ᴘɪɴɢ :`{ms} ms`")

@ascii.on(events.NewMessage(incoming=True, pattern="^/dlt"))
@check_auth
async def delete_module(event):
    B = await event.get_reply_message()
    if B:
        msg_src = await event.get_reply_message()
        try:
            await msg_src.delete()
        except rpcbaseerrors.BadRequestError:
            return
        
    

@ascii.on(events.NewMessage(incoming=True, pattern=f"^/start({Vars.BOT_USERNAME})?$",))
async def start(event):
    user = await ascii.get_entity(int(event.sender.id))
    usersdata = pickle.load(open('users.pkl', 'rb'))
    # Examplay data = {"zarox": {"nio": 12124, "venom": 13412}, "odi": {"zarox": 34243, "iser":3443}
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    with open('users.pkl', 'wb') as f:
        pickle.dump(usersdata, f)
    await ascii.send_message(int(Vars.LOG_GRP), f"#START\n**User**: [{user.first_name}](tg://user?id={user.id})\n**Username**: {user.username}\n**ID**: {user.id}")
    rl = await event.respond(
        f"Hi [{user.first_name}](tg://user?id={user.id})\nI'm ascii bot to encode any given text in unicode characters[\u200d](https://telegra.ph/file/d2adbd7a528b847e724b7.jpg)\nStart with /help\n\nḌᡋᇱ᱗\̃৐࿗ȓͯࢎ⛍⣤⏆ᗖҖᄱ᰼ᥔೊᙃ",
        buttons=[
            [
                Button.switch_inline(
                    "Try inline", query=""
                )
            ],
            [Button.url("Updates", "https://t.me/execal")],
            [Button.url("Dev", "https://t.me/zarox")],
        ],
        link_preview=True
    )
    await asyncio.sleep(7)
    k = 0
    while k <= 300:
        await chrloop(rl, user)
        await asyncio.sleep(1)
        k += 1


@ascii.on(events.NewMessage(incoming=True))
async def logger(event):
    username = event.sender.username or None
    lastname = event.sender.last_name or ""
    user = await ascii.get_entity(int(event.sender.id))
    if event.is_private and event.sender.id != int(Vars.OWNER_ID):
        startm = f"[{user.first_name} {lastname}](https://t.me/{username}) {event.sender.id}\nMessage: `{event.text}`"
        if event.text == "/start web":
            startm += "\n\n**From Web**"
        await ascii.send_message(int(Vars.LOG_GRP), startm, link_preview=False)
        

@ascii.on(events.NewMessage(incoming=True, pattern="^/restart kana"))
@check_auth
async def delee_module(event):
    cmd = "screen -S iris -X stuff '^C python -m Zarox\n'"
    process = await asyncio.create_subprocess_shell(
    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    await asyncio.sleep(7)
    await event.reply("Restarted Kana Successfully..")
    print("Restarted Kana Successfully..")
