import requests
import xml.etree.ElementTree as ET
from sys import argv
from telegram.ext import CommandHandler, Updater
from telegram import MessageEntity, Message
from telegram import constants


_url = "https://feddit.it/feeds/c/eticadigitale.xml?sort=New"
_token = ""
_chat_id = ""

def clear_markdown_parse(msg): 
    special = ['.','-']

    for i in range(0,len(msg)):
        for ch in special:

            if msg[i] == ch and msg[i-1] != '\\':
                msg = msg[:i] + "\\" + msg[i:]

    
    return msg

# Returns true if the message should be send in the group, else false
def anythingNew(msg):
    omsg = ""
    try:
        with open('.lastone','r') as f: # Read last message sent
            omsg = f.read()
    except FileNotFoundError: # Probably first run of the program
            pass
    
    if (msg != omsg): # check if new msg is different from last one
        with open('.lastone','w') as f:
            f.write(msg)
        return True
    
    return False
    

# Take the third child of the XML tree
def parseXML():
    global _url
    resp = requests.get(_url)

    with open('eticadigitale.xml','wb') as f:
        f.write(resp.content)
    
    tree = ET.parse("eticadigitale.xml")

    msg = "📬 _Nuova discussione_\n"
    elem = tree.findall('./channel/item[2]/')
    for subelem in elem:
            if (subelem.tag == "title"):
                msg = msg + "*" + subelem.text +  "* \n"
                
            elif (subelem.tag=="link"):
                msg = msg + subelem.text + "\n"
    

    msg = msg + "\n_Vieni a trovarci su [Lemmy](https://t.me/eticadigitalechannel/648)_"

    return clear_markdown_parse(msg)

def work(context):
    global _chat_id

    if _chat_id == "":
        return

    msg = parseXML()

    if anythingNew(msg) == True:
        context.bot.send_message(chat_id=_chat_id, text=msg, parse_mode=constants.PARSEMODE_MARKDOWN_V2, disable_web_page_preview=True )

def start(update, context):
    global _chat_id

    if _chat_id == "":
        _chat_id = str(update.message.chat_id)
        context.bot.send_message(chat_id = _chat_id, text = "Bot inizializzato 👀" ,parse_mode=constants.PARSEMODE_MARKDOWN_V2)

        

def pong(update, context):
    global _chat_id

    if _chat_id != "":
        context.bot.send_message(chat_id = _chat_id, text = "Pong")


def main():
    global _token

    if ( len(argv) > 1):
        _token = argv[1]

    if _token == "":
        print("Token is empty")
        return
    
    updater = Updater(_token, use_context=True)
    dispatcher = updater.dispatcher 

    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('ping', pong))

    j = updater.job_queue

    j.run_repeating(work, interval=6, first=6)

    updater.start_polling()
    updater.idle()
                

if __name__=="__main__":
    main()
