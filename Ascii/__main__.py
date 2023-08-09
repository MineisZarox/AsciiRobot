from . import ascii
from .utilities.utility import load_plugins
from .utilities.startup import startup

async def initiation():
    load_plugins("plugins")
    print("Ascii Deployed Successfully!")
    await startup()
    return

ascii.loop.run_until_complete(initiation())

if __name__ == "__main__":
    ascii.run_until_disconnected()

    
