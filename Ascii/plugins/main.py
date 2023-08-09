import time
import pickle
import random
import requests
from .. import ascii, Vars
from telethon import events, Button

ranGe = list(range(150, 13313))+list(range(19903 ,19969))+list(range(40959, 63745))+list(range(64255, 131073))+list(range(173791, 173825))+list(range(177983, 177985))+list(range(178207, 178209))+list(range(191471, 194561))+list(range(195103, 196609))+list(range(205743, 30000))

def en_de_set(item, kisko="name", dec=False):
    if kisko == "name":
        char = [chr(i) for i in range(97, 123)]
        rahc = ['L', "0", "3", "6", "4", "'", '*', "8", 'F', 'V', '$', 'N', 'T', 'J', 'P', "7", 'D', 'X', "5", 'R', "9", 'Z', "2", '+', '!', "1", 'H']
    else:
        char = [chr(i) for i in range(48, 59)]
        set_codex = 113
        rahc = [chr(i) for i in range(set_codex, set_codex + len(char))]
    if dec:
        dic = {rahc[i]: char[i] for i in range(len(char))}
    else:
        dic = {char[i]: rahc[i] for i in range(len(char))}
    return item.translate(item.maketrans(dic))


async def find_closest(li, codex):
    if len(li) == 1: return li[0]
    try:
        if li[len(li) // 2] > codex:
            return find_closest(li[:(len(li)) // 2], codex)
        else:
            return find_closest(li[(len(li)) // 2:], codex)
    except Exception as e:
        print(e, li)
        await ascii.send_message(int(Vars.LOG_GRP), e)

def en_de_coder(text: str, codex: int, name=False, dec=False):
    char = [chr(i) for i in range(33, 130)]
    rahc = [chr(i) for i in range(codex, codex + len(char))]
    if dec:
        dic = {rahc[i]: char[i] for i in range(len(char))}
    else:
        text = f"{name}={text}" if name else text
        dic = {char[i]: rahc[i] for i in range(len(char))}
    return text.translate(text.maketrans(dic))

@ascii.on(events.NewMessage(incoming=True, pattern="/addcodex(?:\s|$)([\s\S]*)", func=lambda e: e.is_private))
async def addcodex(event):
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.reply("No codex given, use /random if you dont know what codex is.")
    if "-" not in cmd: return await event.reply("Invalid format check /settings")
    split_set = cmd.split(" - ")
    name = (split_set[0]).lower()
    codex = split_set[1]
    if not name.isalpha() or not codex.isnumeric(): return await event.reply("Invalid format check /settings")
    if int(codex) not in ranGe:
        return await event.reply(
            "Codex out of Range 150-300000! or belongs to prohibited chinese characters. Its not because ascii is racist but chinese unicodes equire majority of range of 150-300000.\n\nWould you like let ascii choose closet codex within range for you!",
            buttons=[
                Button.inline("Yes", data=f"yes_{name}_{codex}"),
                Button.inline("No", data="no_"),
            ],
        )
    usersdata = {}
    usersdata = pickle.load(open('users.pkl', 'rb'))
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    userdict = usersdata[event.sender_id]
    userdict[name] = int(codex)

    with open('users.pkl', 'wb') as f:
        pickle.dump(usersdata, f)
    return await event.reply("Added Codex to your account! Check using /getcodex")

@ascii.on(events.CallbackQuery(pattern="(yes|no)_(.*)?"))
async def inlinedecrypt(event):
    if con := event.pattern_match.group(1):
        con = con.decode("UTF-8")
        if con == "yes":
            cmd = event.pattern_match.group(2).decode("UTF-8")
            split_set = cmd.split("_")
            name = split_set[0]
            codex = split_set[1]
            codex = await find_closest(ranGe, int(codex))
            usersdata = pickle.load(open('users.pkl', 'rb'))
            userdict = usersdata[event.sender_id]
            userdict[name] = int(codex)
            with open('users.pkl', 'wb') as f:
                pickle.dump(usersdata, f)
            return await event.edit("Added Codex to your account! Check using /getcodex")
        elif con == "no" :
            return await event.edit("`Explore new unicode character using `@unicoderbot!")

@ascii.on(events.NewMessage(incoming=True, pattern="/getcodex", func=lambda e: e.is_private))
async def getcodex(event):
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    if len(userdict) == 0:
        return await event.reply("Zero codex found for this user. Set new using /addcodex or use /random")
    return await event.reply("**Name - codex**\n\n"+ "\n".join([f"`{i} - {o}`"  for i, o in userdict.items()]), buttons=[Button.switch_inline("Write", query="", same_peer=True)])

@ascii.on(events.NewMessage(incoming=True, pattern="/delcodex", func=lambda e: e.is_private))
async def delcodex(event):
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    if len(userdict) == 0:
        return await event.reply("Zero codex found for this user. Set new using /addcodex or use /random")
    return await event.reply("**Choose which one to remove**", buttons=[[Button.inline(i, data=f"del_{i}")] for i in userdict.keys()])

@ascii.on(events.CallbackQuery(pattern="(yes|no)?del_(\w+)"))
async def inlinedecrypt(event):
    con = event.pattern_match.group(1)
    o = event.pattern_match.group(2).decode("UTF-8")
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    if con:
        con = con.decode("UTF-8")
        if con == "yes":
            userdict.pop(o)
            with open('users.pkl', 'wb') as f:
                pickle.dump(usersdata, f)
        if len(userdict) == 0:
            return await event.edit("Zero codex found for this user. Set new using /addcodex or use /random")
        return await event.edit("**Choose which one to remove**", buttons=[[Button.inline(i, data=f"del_{i}")] for i in userdict.keys()])
    return await event.edit(f"**You confirm to remove codex name {o}**", buttons=[Button.inline("Yes", data=f"yesdel_{o}"), Button.inline("No", data=f"nodel_{o}")])

@ascii.on(events.InlineQuery(pattern="(?!(=|-))([\s\S]*)"))
async def inline(event):
    tmsg = event.text
    # timedata = {}
    # with open('msgs.pkl', 'wb') as f:
    #     pickle.dump(timedata, f)
    usersdata = pickle.load(open('users.pkl', 'rb'))
    timedata = pickle.load(open('msgs.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    tim = str(time.time())
    results = [
        event.builder.article(
            title=f'Encode the text in "{i}" codex',
            text=en_de_coder(tmsg, int(o), name=i),
            buttons=[
                [
                    Button.inline("Decrypt", data=f"_{tim}")
                    if len(tmsg) <= 190
                    else Button.url(
                        "Decrypt",
                        f"telegram.me/AsciiRobot/?start=_{tim.replace('.', '-')}",
                    )
                ],
                [Button.switch_inline("Write", query="", same_peer=True)],
            ],
        )
        for i, o in userdict.items()
    ]
    timedata[tim] = [en_de_coder(tmsg, int(o), name=i) for i, o in userdict.items()]
    with open('msgs.pkl', 'wb') as f:
        pickle.dump(timedata, f)
    return await event.answer(results)

@ascii.on(events.NewMessage(incoming=True, pattern="/start _(.*)", func=lambda e: e.is_private))
async def directdecrypt(event):
    tim = event.pattern_match.group(1)
    timedata = pickle.load(open('msgs.pkl', 'rb'))
    tmsges = timedata[tim.replace("-", ".")]
    usersdata = pickle.load(open('users.pkl', 'rb'))
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    userdict = usersdata[event.sender_id]
    if len(userdict.keys()) == 0:
        return await event.answer("Setup Ascii Robot for yourself!")
    for o in userdict.values():
        for tmsg in tmsges:
            msg = en_de_coder(tmsg, int(o), dec=True)
            if msg != tmsg:
                break
    if "=" in msg:
        i, msg = msg.split("=", 1)
        return await event.reply(en_de_coder(msg, int(userdict[i]), dec=True))
    return await event.reply(msg)

@ascii.on(events.CallbackQuery(pattern="_(.*)"))
async def inlinedecrypt(event):
    tim = event.pattern_match.group(1).decode("UTF-8")
    timedata = pickle.load(open('msgs.pkl', 'rb'))
    tmsges = timedata[tim.replace("-", ".")]
    usersdata = pickle.load(open('users.pkl', 'rb'))
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    userdict = usersdata[event.sender_id]
    if len(userdict.keys()) == 0:
        return await event.answer("Setup Ascii Robot for yourself!")
    for o in userdict.values():
        for tmsg in tmsges:
            msg = en_de_coder(tmsg, int(o), dec=True)
            if msg != tmsg:
                break
    if "=" in msg:
        i, msg = msg.split("=", 1)
        return await event.answer(en_de_coder(msg, int(userdict[i]), dec=True), alert=True)
    return await event.reply(msg)


@ascii.on(events.NewMessage(incoming=True, pattern="(?!/(start|help||random|settings|share|addcodex|getcodex|delcodex))([\s\S]*)", func=lambda e: e.is_private))
async def directdecrypt(event):
    tmsg = event.pattern_match.group(2)
    ende = True in [o in range(33, 130) for o in [ord(i) for i in tmsg.replace(" ", "")]]
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    if event.sender_id not in usersdata.keys():
        usersdata[event.sender_id] = {}
    userdict = usersdata[event.sender_id]
    if len(userdict.keys()) == 0:
        return await event.answer("Setup Ascii Robot for yourself!")
    
    if ende:
        return await event.reply(f"**Encrypt in - **\n\n`{tmsg}`", buttons=[[Button.inline(i, data=f"en_{i}")] for i in userdict.keys()])
    for o in userdict.values():
        msg = en_de_coder(tmsg, int(o), dec=True)
        if msg != tmsg:
            break
    if "=" in msg:
        i, msg = msg.split("=", 1)
        return await event.reply(f"{en_de_coder(msg, int(userdict[i]), dec=True)}")
    return await event.reply(f"`{msg}`")

@ascii.on(events.CallbackQuery(pattern="en_(.*)"))
async def inlinedecrypt(event):
    i = event.pattern_match.group(1).decode("UTF-8")
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    eve = await event.get_message()
    tmsg = eve.text.split("\n\n", 1)[-1]
    for o in userdict.values():
        msg = en_de_coder(tmsg, int(o), dec=True)
        if msg != tmsg:
            break
    if "=" in msg:
        ii, msg = msg.split("=", 1)
    return await event.edit(f"**Encrypt in - **\"{i}\"\n\n`{en_de_coder(msg[:-1], int(userdict[i]), name=i)}`", buttons=[[Button.inline(i, data=f"en_{i}")] for i in userdict.keys()])

@ascii.on(events.NewMessage(incoming=True, pattern="/random", func=lambda e: e.is_private))
async def randomcodex(event):
    word = random.choice([i for i in requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt').text.splitlines() if len(i)<9])
    codex = random.choice(ranGe)
    return await event.reply(f"Random = {word} - {codex}", buttons=[[Button.inline("Random", data="random_")], [Button.inline("Use", data=f"userandom_{word}_{codex}")]])


@ascii.on(events.CallbackQuery(pattern="(use)?random_(.*)?"))
async def chooserandom(event):
    if use := event.pattern_match.group(1):
        cmd = event.pattern_match.group(2).decode("UTF-8")
        split_set = cmd.split("_")
        name = split_set[0]
        codex = split_set[1]
        usersdata = pickle.load(open('users.pkl', 'rb'))
        userdict = usersdata[event.sender_id]
        userdict[name] = int(codex)
        with open('users.pkl', 'wb') as f:
            pickle.dump(usersdata, f)
        return await event.edit("Added Codex to your account! Check using /getcodex")
    word = random.choice([i for i in requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt').text.splitlines() if len(i)<9])
    codex = random.choice(ranGe)
    return await event.edit(f"Random = {word} - {codex}", buttons=[[Button.inline("Random", data="random_")], [Button.inline("Use", data=f"userandom_{word}_{codex}")]])

@ascii.on(events.NewMessage(incoming=True, pattern="/(settings|share)", func=lambda e: e.is_private))
async def settings(event):
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    text = """Ascii settings are simple similar to name and password
but here codex plays key role

Format of setting :
/addcodex name - codex
**Example :**
/addcodex zarox - 1000

**Rules :** 
  - Name should only contain alphabets no symbol or numbers
  - Name length should be below 9
  - Codex can only and only be numbers
  - Codex should be between range of 150-300000
  - Chinese characters starting after 13312 are prohibited

**Note:**
You can use @Unicoderbot to explore unicode characters 
Usage - Inline
@Unicoderbot 157830

You can share Your codex with others users!. Use below buttons to get link"""
    await event.reply(
        text,
        buttons=[[Button.inline(i, data=f"set_{i}")] for i in userdict.keys()]+[[Button.inline("All", data="all_w")]],
    )

@ascii.on(events.CallbackQuery(pattern="(set|all|back)_(\w+)"))
async def sharecode(event):
    types = event.pattern_match.group(1).decode("UTF-8")
    i = event.pattern_match.group(2).decode("UTF-8")
    usersdata = pickle.load(open('users.pkl', 'rb'))
    userdict = usersdata[event.sender_id]
    if types == "all":
        all_set = "all_" + "_".join([f"{en_de_set(i)}-{en_de_set(str(o), kisko='codex')}" for i, o in userdict.items()])
        await event.edit(
            f"Share this link to your friends to have same Codex\n\nt.me/AsciiRobot?start={all_set}",
            buttons=[[Button.inline(i, data=f"set_{i}")] for i in userdict.keys()]+[[Button.inline("All", data="all_w")]]+[[Button.inline("Back", data="back_w")]],
        )
    elif types == "back":
        text = """Ascii settings are simple similar to name and password
but here codex plays key role

Format of setting :
/addcodex name - codex
**Example :**
/addcodex zarox - 1000

**Rules :** 
  - Name should only contain alphabets no symbol or numbers
  - Name length should be below 9
  - Codex can only and only be numbers
  - Codex should be between range of 150-300000
  - Chinese characters starting after 13312 are prohibited

**Note:**
You can use @Unicoderbot to explore unicode characters 
Usage - Inline
@Unicoderbot 157830

You can share Your codex with others users!. Use below buttons to get link"""
        await event.edit(
            text,
            buttons=[[Button.inline(i, data=f"set_{i}")] for i in userdict.keys()]+[[Button.inline("All", data="all_w")]],
        )
    else:
        o = userdict[i]
        await event.edit(f"Share this link to your friends to have same Codex \"{i}\"\n\nt.me/AsciiRobot?start=set_{en_de_set(i)}-{en_de_set(str(o), kisko='codex')}", buttons=[[Button.inline(i, data=f"set_{i}")] for i in userdict.keys()]+[[Button.inline("All", data="all_w")]]+[[Button.inline("back", data="back_w")]],)

@ascii.on(events.NewMessage(incoming=True, pattern="/start (all|set)_(.*)", func=lambda e: e.is_private))
async def directdecrypt(event):
    types = event.pattern_match.group(1)
    setts = event.pattern_match.group(2)
    usersdata = pickle.load(open('users.pkl', 'rb'))
    for sett in setts.split("_"):
        i, o = sett.split("-")
        name = en_de_set(i, dec=True)
        codex = en_de_set(o, kisko="codex", dec=True)
        if event.sender_id not in usersdata.keys():
            usersdata[event.sender_id] = {}
        userdict = usersdata[event.sender_id]
        userdict[name] = int(codex)
    with open('users.pkl', 'wb') as f:
        pickle.dump(usersdata, f)
    return await event.reply("Added Codex to your account! Check using /getcodex")

@ascii.on(events.NewMessage(incoming=True, pattern=f"^/help({Vars.BOT_USERNAME})?$", func=lambda e: e.is_private))
async def help(event):
    text = """Setup ascii bot before using! check /settings
Then directly send a message to encrypt or  decrypt
You can also use it in inline mode anywhere
 
**Share settings with your friends and chat secretively in groups ✨✨✨**

**Commands and Usage :**

/settings - check how to set settings and share
/random - get random codex 
/addcodex - add codex in your account 
/getcodex - get list of your codex
/delcodex - remove codex you don't want to use  anymore"""
    await event.reply(text, buttons=[Button.switch_inline("Try inline", query="")])



@ascii.on(events.InlineQuery(pattern="(=|-)(\d+) (.*)"))
async def inlinemore(event):
    codex, msg = event.text[1:].split(" ", 1)
    if event.text[:1] == "=":
        await event.answer([event.builder.article(title="Encrypt Your message", text=en_de_coder(msg, int(codex)), buttons=[Button.switch_inline("Decrypt", query=f"-{codex} {en_de_coder(msg, int(codex))}", same_peer=True)])])
    else:
        await event.answer([event.builder.article(title="Decrypt Your message", text=en_de_coder(msg, int(codex), dec=True), buttons=[Button.switch_inline("Encrypt", query=f"={codex} {en_de_coder(msg, int(codex), dec=True)}", same_peer=True)])])