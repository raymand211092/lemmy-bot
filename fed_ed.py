import requests
import xml.etree.ElementTree as ET
from sys import argv
from telegram.ext import CommandHandler, Updater
from telegram import MessageEntity, Message
from telegram import constants

from datetime import datetime


_url = "https://feddit.it/feeds/c/eticadigitale.xml?sort=New"
_token = ""
_chat_id = ""


# Algorithm that finds the number of sticky posts
# Assuming communities could add or remove sticked posts over time, this must be runned periodically
def find_stickies():
    offset=1

    tree = ET.parse('eticadigitale.xml')

    # Get and parse every dates from channel posts
    dates_list = []
    elems = tree.findall('./channel/item/pubDate')
    for elem in elems:
        to_parse = elem.text[0:len(elem)-6]
        dates_list.append(datetime.strptime(to_parse, '%a, %d %b %Y %H:%M:%S'))
    
    # This only works if you sort xml by New
    # If you find that the next post is older than the current one, then that's a sticky
    for i in range(0,len(dates_list)-1):
        if dates_list[i] < dates_list[i+1]:
            return offset + i + 1

    return offset

# Some characters are reserverd for telegram markdown, so they must be escaped with the precedenting substring "\\"
# https://core.telegram.org/bots/api#markdownv2-style
def clear_markdown_parse(msg): 

    reserved = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    for i in range(0,len(msg)):
        for ch in reserved:

            if msg[i] == ch and msg[i-1] != '\\':
                msg = msg[:i] + "\\" + msg[i:]

    
    return msg

# Reads the old link from file, if it doesn't matches the new one, then it's a new post
def anythingNew(link):
    old_link = ""
    try:
        with open('.lastone','r') as f: # Read last message sent
            old_link = f.read()
    except FileNotFoundError: # Probably first run of the program
            pass
    
    if (link != old_link): # check if new msg is different from last one
        with open('.lastone','w') as f:
            f.write(link)
        return True
    
    return False
    

# Take the third child of the XML tree
def parseXML():
    global _url
    resp = requests.get(_url)
    link=""

    with open('eticadigitale.xml','wb') as f:
        f.write(resp.content)
    
    tree = ET.parse("eticadigitale.xml")

    msg = ""
    offset = find_stickies()
    elem = tree.findall("./channel/item[" + str(offset) + "]/")
    for subelem in elem:
            if (subelem.tag == "title"):
                msg = msg + "*" + clear_markdown_parse(subelem.text) +  "* \n"
                
            elif (subelem.tag=="link"):
                link = subelem.text
                msg = msg + clear_markdown_parse(subelem.text) + "\n"
    

    msg = "📬 _Nuova discussione_\n" + msg + "\n_Vieni a trovarci su [Lemmy](https://t.me/eticadigitalechannel/648)_"

    return msg, link

def work(context):
    global _chat_id

    if _chat_id == "":
        return

    msg, link = parseXML()

    if anythingNew(link) == True:
        context.bot.send_message(chat_id=_chat_id, text=msg, parse_mode=constants.PARSEMODE_MARKDOWN_V2, disable_web_page_preview=True )

def start(update, context):
    global _chat_id

    print(update.message.chat_id)

    with open(".config") as f:
        _chat_id = f.read()

    #if _chat_id != "":
    #    context.bot.send_message(chat_id = _chat_id, text = "Bot inizializzato." ,parse_mode=constants.PARSEMODE_MARKDOWN_V2)

        

def pong(update, context):
    global _chat_id

    if _chat_id != "":
        context.bot.send_message(chat_id = _chat_id, text = "Pong")
        find_stickies()


def main():
    global _token
    global _chat_id

    if ( len(argv) > 1):
        _token = argv[1]

    if _token == "":
        print("Token is empty")
        return
    
    with open(".config") as f:
        _chat_id = f.read()
    
    updater = Updater(_token, use_context=True)
    dispatcher = updater.dispatcher 

    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('ping', pong))

    j = updater.job_queue

    j.run_repeating(work, interval=10, first=5)

    updater.start_polling()
    updater.idle()
                

if __name__=="__main__":
    main()
