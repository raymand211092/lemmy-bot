import requests
import xml.etree.ElementTree as ET
from telegram.ext import CommandHandler, Updater

_url = "https://feddit.it/feeds/c/eticadigitale.xml?sort=New"
_token = ""
_chat_id = ""


# Returns true if the message should be send in the group, else false
def AnythingNew(msg):
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
    

# Take the third child of the three
def parseXML():
    global _url
    resp = requests.get(_url)

    with open('eticadigitale.xml','wb') as f:
        f.write(resp.content)
    
    tree = ET.parse("eticadigitale.xml")

    msg = ""
    ll = tree.findall('./channel/item[2]/')
    for e in ll:
            if (e.tag == "title"):
                msg = msg + e.text + "\n"
            elif (e.tag=="link"):
                msg = msg + e.text
    
    return msg

def work(context):
    global _chat_id
    msg = parseXML()
    flag = AnythingNew(msg)

    if _chat_id == "":
        return
      
    if AnythingsNew(msg) == True:
        context.bot.send_message(chat_id=_chat_id, text=msg)

def start(update, context):
    global _chat_id

    if _chat_id == "":
        _chat_id = str(update.message.chat_id)
        update.message.reply_text("Ok")

def main():
    global _token
    if _token == "":
        print("Token is empty")
        return
    
    updater = Updater(_token, use_context=True)
    dispatcher = updater.dispatcher 

    dispatcher.add_handler(CommandHandler('start',start))

    j = updater.job_queue

    j.run_repeating(work, interval=600, first=5)

    updater.start_polling()
    updater.idle()
                


if __name__=="__main__":
    main()
