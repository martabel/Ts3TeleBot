# Ts3TeleBot
Teamspeak3 Telegram Bot

With this little Telegram bot you can get a list of the current active Teamspeak users.

![alt text](https://github.com/martabel/Ts3TeleBot/raw/master/bot_output.png "Bot output")

# Telegram commands
* `/hello` send a hello message
* `/help` send a help message with all commands
* `/tsclients` request active users of the configured Teamspeak server
* `/uptime` get current uptime of the server with the linux uptime command

# Configuration
Setup a `config.toml` file near the source files or export a environment variable `TS3_TELE_BOT_CFG`

config.toml
```
[teamspeak]
host = "localhost"
port = 10011
sa_passwd = "YourTeamspeakServerAdminPassword"

[telegram]
api_token = "YourTelegramBotApiToken"
```

# Run with python 3
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 telegramBot.py
```
