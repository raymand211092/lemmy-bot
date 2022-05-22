import requests
import xml.etree.ElementTree as ET
from sys import argv
from telegram.ext import CommandHandler, Updater
from telegram import MessageEntity, Message
from telegram import constants


_url = "https://feddit.it/feeds/c/eticadigitale.xml?sort=New"
_token = ""
_chat_id = ""


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
    

# Take the third child of the tree
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
                tmp = subelem.text.split(".")
                msg = msg + tmp[0] + '\\.' + tmp[1] + "\n"
    
    msg = msg + '\n_Vieni a trovarci su [Lemmy](https://t\\.me/eticadigitalechannel/648)_'
    return msg

def work(context):
    global _chat_id

    if _chat_id == "":
        return

    msg = parseXML()

    if anythingNew(msg) == True:
        print(msg)
        context.bot.send_message(chat_id=_chat_id, text=msg, parse_mode=constants.PARSEMODE_MARKDOWN_V2, disable_web_page_preview=True )

def start(update, context):
    global _chat_id

    if _chat_id == "":
        _chat_id = str(update.message.chat_id)
        context.bot.send_message(chat_id = _chat_id, text = "Ok 👀" ,parse_mode=constants.PARSEMODE_MARKDOWN_V2)


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

    j = updater.job_queue

    j.run_repeating(work, interval=600, first=10)

    updater.start_polling()
    updater.idle()
                

if __name__=="__main__":
    main()
