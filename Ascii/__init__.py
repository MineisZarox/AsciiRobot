# sourcery skip: avoid-builtin-shadow
import os
import logging
from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from config import chivar as Vars

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

ascii = TelegramClient(
        "ascii",
        api_id=Vars.API_ID,
        api_hash=Vars.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    ).start(bot_token=Vars.BOT_TOKEN)