from .. import ascii, Vars
from telethon import Button

async def startup():
    await ascii.send_message(Vars.LOG_GRP, "**Ascii has been started successfully.**", buttons=[(Button.url("Shinichi", "https://t.me/catuserbotot"),)],)
