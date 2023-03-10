import json
import requests
from bs4 import BeautifulSoup

from .. import pixiv, pxv, Vars
from telethon import events, Button
from telethon.events import CallbackQuery
from .illust import artdict, illustResult
seadict = {}

sudos = list(map(int, (Vars.SUDO_IDS).split(" ")))
offlist = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080, 1110, 1140, 1170, 1200, 1230, 1260, 1290, 1320, 1350, 1380, 1410, 1440, 1470, 1500, 1530, 1560, 1590, 1620, 1650, 1680, 1710, 1740, 1770, 1800, 1830, 1860, 1890, 1920, 1950, 1980, 2010, 2040, 2070, 2100, 2130, 2160, 2190, 2220, 2250, 2280, 2310, 2340, 2370, 2400, 2430, 2460, 2490, 2520, 2550, 2580, 2610, 2640, 2670, 2700, 2730, 2760, 2790, 2820, 2850, 2880, 2910, 2940, 2970]

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def ogiMas(url):
    url = url.replace('original', 'master')
    url = url.replace(url[-4:], f"_master1200.jpg")
    return url


async def queryResults(event, query, user_, offset=0, user=False, uc=0):
    if user:
        if offset == 0:
            results = await pxv.user_illusts(int(query))
        else:
            print('han lol')
            results = await pxv.user_illusts(int(query), offset=offset)
            query = f"{query}:{offset}"
    else:
        if offset == 0:
            results = await pxv.search_illust(query)
        else:
            results = await pxv.search_illust(query, offset=offset)
            query = f"{query}:{offset}"
    if len(results['illusts']) == 0: return "`0 results found of given query`"
    c = 0
    cc = uc+offset+1
    seadict[query] = []
    for result in results['illusts']:
        rdict = {}
        pc = result['page_count']
        rdict['id'] = int(result['id'])
        rdict['pc'] = int(pc)
        rdict['title'] = result['title']
        rdict['name'] = result['user']['name']
        rdict['userid'] = result['user']['id']
        if pc == 1:
            img = result['meta_single_page']['original_image_url']
            rdict['imgs'] = [img]
        else:
            imgs = []
            img = result['meta_pages'][c]['image_urls']['original']
            for i in range(pc):
                imgs.append(result['meta_pages'][i]['image_urls']['original'])
            rdict['imgs'] = imgs
        seadict[query].append(rdict)
    c = uc
    pc = offset
    pc += len(results['illusts'])
    print(c, pc)
    url = f"https://www.pixiv.net/en/artworks/{seadict[query][c]['id']}"
    caption = f"""**Title - **[{seadict[query][c]['title']}]({url})
**By user - **[{seadict[query][c]['name']}](https://www.pixiv.net/en/users/{seadict[query][c]['userid']})
**Page count** - `{seadict[query][c]['pc']}`"""
    print(type(query), query)
    img = seadict[query][c]['imgs']
    if type(img) is list: img = img[0]
    buttons = [
        [
            Button.inline("Prev", data=f"bq_{c-1}_{user_}_{query}"),
            Button.inline(f"{cc}/{pc}", data="cc"),
            Button.inline("Next", data=f"nq_{c+1}_{user_}_{query}")
        ],
        [
            Button.inline("Get In", data=f"q_{c}_{user_}_{seadict[query][c]['id']}_{query}")
        ],
    ]
    return [img, caption, buttons]
    
    
    

@pixiv.on(events.InlineQuery(pattern="(\d+)?pixiv(?:\s|$)([\s\S]*)"))
async def iqueryi(event):
    user_ = event.query.user_id
    offset = event.pattern_match.group(1)
    query = "".join(event.text.split(maxsplit=1)[1:])
    if offset:
        offset = int(offset.decode("UTF-8"))
    else: offset = 0
    if not query: return
    if query.isdigit():query = int(query)
    try:
        img, caption, buttons = await queryResults(event, query, user_, offset=offset)
    except:
        results = await queryResults(event, query, user_)
        return await event.answer(results)
    try:
        await event.answer([event.builder.photo(img, text=caption, buttons=buttons)])
    except:
        try:
            await event.answer([event.builder.photo(ogiMas(img), text=caption, buttons=buttons)])
        except:
            await event.answer([event.builder.photo("Pixiv/plugins/un.jpg", text=caption, buttons=buttons)])

@pixiv.on(events.NewMessage(incoming=True))  
async def link(event):
    user_ = int(event.sender.id)
    if "https://www.pixiv.net/en/artworks" in event.text:
        artId = (event.text).split("/")[-1]
        artId = artId.split(" ")[0]
        eve = await event.reply("`Processing...`")
        img, caption, buttons = await illustResult(int(artId), user_)
        await eve.delete()
        try:
            return await event.client.send_file(event.chat_id, file=img, caption=caption, buttons=buttons)
        except:
            try:
                return await event.client.send_file(event.chat_id, file=ogiMas(img), caption=caption, buttons=buttons)
            except:
                return await event.client.send_file(event.chat_id, file="Pixiv/plugins/un.jpg", caption=caption, buttons=buttons)

@pixiv.on(events.NewMessage(incoming=True, pattern="/(\d+)?pixiv(?:\s|$)([\s\S]*)"))
async def query(event):
    user_ = int(event.sender.id)
    offset = event.pattern_match.group(1)
    query = "".join(event.message.message.split(maxsplit=1)[1:])
    if offset:
        offset = int(offset)
    else: offset = 0
    if not query:
        return await event.reply("`Give your words to search pixiv out dummy! ...`")
    eve = await event.reply("`Searching...`")
    
    try:
        if query.isdigit(): img, caption, buttons = await illustResult(int(query), user_)
        else: img, caption, buttons = await queryResults(event, query, user_, offset=offset)
    except Exception as e:
        print(e)
        result = await queryResults(event, query, user_, offset=offset)
        return await eve.edit(result)
    await eve.delete()
    try:
        return await event.client.send_file(event.chat_id, file=img, caption=caption, buttons=buttons)
    except:
        try:
            return await event.client.send_file(event.chat_id, file=ogiMas(img), caption=caption, buttons=buttons)
        except:
            return await event.client.send_file(event.chat_id, file="Pixiv/plugins/un.jpg", caption=caption, buttons=buttons)
        

@pixiv.on(CallbackQuery(pattern="nq_(\d+)_(\d+)_(.*)"))
async def nextq(event):
    user_ = int(event.sender_id)
    c = int(event.pattern_match.group(1).decode("UTF-8"))
    user = int(event.pattern_match.group(2).decode("UTF-8"))
    query = event.pattern_match.group(3).decode("UTF-8")
    if user != user_: return await event.answer("Send your own query")
    pc = len(seadict[query])
    cc = c+1
    nc = 0
    
    if ":" in query:
        query, nc = query.split(":")
        nc = int(nc)
    cc += nc
    pc += nc
    if c == pc-nc and pc<nc+30: 
        c = 0
        cc = nc+1
    if pc in offlist and cc == pc+1:
        if query.isdigit():
            try:
                img, caption, buttons = await queryResults(event, query, user_, user=True, offset=pc)
            except Exception as e:
                return print(e)
        else:
            try:
                img, caption, buttons = await queryResults(event, query, user_, offset=pc)
            except Exception as e:
                return print(e)
        try:
            return await event.edit(file=img, text=caption, buttons=buttons)
        except:
            try:
                return await event.edit(file=ogiMas(img), text=caption, buttons=buttons)
            except:
                return await event.edit(file="Pixiv/plugins/un.jpg", text=caption, buttons=buttons)
    else:
        pass
    if nc != 0: query = f"{query}:{nc}"
    url = f"https://www.pixiv.net/en/artworks/{seadict[query][c]['id']}"
    caption = f"""**Title - **[{seadict[query][c]['title']}]({url})
**By user - **[{seadict[query][c]['name']}](https://www.pixiv.net/en/users/{seadict[query][c]['userid']})
**Page count** - `{seadict[query][c]['pc']}`"""
    img = seadict[query][c]['imgs']
    if type(img) is list: img = img[0]
    buttons = [
        [
            Button.inline("Prev", data=f"bq_{c-1}_{user}_{query}"),
            Button.inline(f"{cc}/{pc}", data="cc"),
            Button.inline("Next", data=f"nq_{c+1}_{user}_{query}")
        ],
        [
            Button.inline("Get In", data=f"q_{c}_{user}_{seadict[query][c]['id']}_{query}")
        ],
    ]
    try:
        return await event.edit(file=img, text=caption, buttons=buttons)
    except:
        try:
            return await event.edit(file=ogiMas(img), text=caption, buttons=buttons)
        except:
            return await event.edit(file="Pixiv/plugins/un.jpg", text=caption, buttons=buttons)

        
@pixiv.on(CallbackQuery(pattern="bq_(-?(\d+))_(\d+)_(.*)"))
async def backq(event):
    print("han back ")
    user_ = int(event.sender_id)
    c = int(event.pattern_match.group(1).decode("UTF-8"))
    user = int(event.pattern_match.group(3).decode("UTF-8"))
    query = event.pattern_match.group(4).decode("UTF-8")
    if user != user_: return await event.answer("Send your own query")
    pc = len(seadict[query])
    cc = c+1
    nc = 0
    if ":" in query:
        query, nc = query.split(":")
        nc = int(nc)
    if c == -1 and nc != 0:
        pc = nc - 30
    cc += nc
    print("out", c, cc, pc, nc, len(seadict[query]))
    if cc == nc or pc in offlist and cc == nc:
        print("In", c, cc, pc, nc)
        if query.isdigit():
            img, caption, buttons = await queryResults(event, query, user_, user=True, offset=pc, uc=29)
            # try:
            #     img, caption, buttons = await queryResults(event, query, user_, user=True, offset=pc, c=cc-1)
            # except Exception as e:
            #     return print(e)
        else:
            try:
                img, caption, buttons = await queryResults(event, query, user_, offset=pc, uc=29)
            except Exception as e:
                return print(e)
        try:
            return await event.edit(file=img, text=caption, buttons=buttons)
        except:
            try:
                return await event.edit(file=ogiMas(img), text=caption, buttons=buttons)
            except:
                return await event.edit(file="Pixiv/plugins/un.jpg", text=caption, buttons=buttons)
    else:
        pass
    if nc != 0: query = f"{query}:{nc}"
    pc += nc
    if cc == 0: return await event.answer("No previous illustration to show Honey.")
    url = f"https://www.pixiv.net/en/artworks/{seadict[query][c]['id']}"
    caption = f"""**Title - **[{seadict[query][c]['title']}]({url})
**By user - **[{seadict[query][c]['name']}](https://www.pixiv.net/en/users/{seadict[query][c]['userid']})
**Page count** - `{seadict[query][c]['pc']}`"""
    img = seadict[query][c]['imgs']
    if type(img) is list: img = img[0]
        
    buttons = [
        [
            Button.inline("Prev", data=f"bq_{c-1}_{user}_{query}"),
            Button.inline(f"{cc}/{pc}", data="cc"),
            Button.inline("Next", data=f"nq_{c+1}_{user}_{query}")
        ],
        [
            Button.inline("Get In", data=f"q_{c}_{user}_{seadict[query][c]['id']}_{query}")
        ],
    ]
    try:
        return await event.edit(file=img, text=caption, buttons=buttons)
    except:
        try:
            return await event.edit(file=ogiMas(img), text=caption, buttons=buttons)
        except:
            return await event.edit(file="Pixiv/plugins/un.jpg", text=caption, buttons=buttons)
        
        
    
            
@pixiv.on(CallbackQuery(pattern="q_(\d+)_(\d+)_(\d+)_(.*)"))
async def qi(event):
    user_ = int(event.sender_id)
    qc = int(event.pattern_match.group(1).decode("UTF-8"))
    user = int(event.pattern_match.group(2).decode("UTF-8"))
    artId = int(event.pattern_match.group(3).decode("UTF-8"))
    query = event.pattern_match.group(4).decode("UTF-8")
    print(user, user_)
    if user != user_: return await event.answer("Send your own query")
    
    url = f"https://www.pixiv.net/en/artworks/{artId}"
    results = await pxv.illust_detail(artId)
    caption = f"""**Title - **[{results['illust']['title']}]({url})
**By user - **[{results['illust']['user']['name']}](https://www.pixiv.net/en/users/{results['illust']['user']['id']})"""
    pc = results['illust']['page_count']
    c = 0
    cc = 1
    img = ""
    if pc == 1:
        img = results['illust']['meta_single_page']['original_image_url']
        artdict[artId] = [img]
    else:
        img = results['illust']['meta_pages'][c]['image_urls']['original']
        imgs = []
        for i in range(pc):
            imgs.append(results['illust']['meta_pages'][i]['image_urls']['original'])
        artdict[artId] = imgs
    
    buttons = [
        [
            Button.inline("Prev", data=f"b_{0}_{pc}_{user}_{artId}"),
            Button.inline(f"{cc}/{pc}", data="cc"),
            Button.inline("Next", data=f"n_{cc+1}_{pc}_{user}_{artId}")
        ],
        [
            Button.inline("Download", data=f"d_{c}_{pc}_{user}_{artId}")
        ],
        [
            Button.inline("Get out", data=f"nq_{qc}_{user}_{query}")
        ]
    ]
    
    try:
        return await event.edit(file=img, text=caption, buttons=buttons)
    except Exception as e:
        print(e)
        try:
            return await event.edit(file=ogiMas(img), text=caption, buttons=buttons)
        except:
            return await event.edit(file="Pixiv/plugins/un.jpg", text=caption, buttons=buttons)
