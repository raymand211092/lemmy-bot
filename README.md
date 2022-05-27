# Lemmy bot

Telegram bot that sends new posts from a Lemmy community to a Telegram chat group

## Requirements
- Python3.7+
- A telegram bot token, please read [this](https://core.telegram.org/bots#6-botfather)

## Installation

### (Suggested) With Docker
```bash
git clone 
cd lemmy-bot
docker build -t etica-digitale/lemmy .
sudo docker run -d -e token="YOUR_TOKEN_HERE!!" etica-digitale/lemmy
```


### Classic
You may use a python env

```
git clone https://gitlab.com/etica-digitale/lemmy-bot.git
cd lemmy-bot
pip install python-telegram-bot
python3 fed_ed.py YOUR_TOKEN_HERE

```

## How to use this bot
1. Run the program
2. Add the bot to a group
3. Type `/start`, eventually /start@BOT_NAME if you already got some bots in that chat

