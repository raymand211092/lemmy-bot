# Lemmy bot

Bot che invia i nuovi post da Lemmy al gruppo di Etica Digitale

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

