# Discord threads

> [Add the bot to your server](https://discord.com/api/oauth2/authorize?client_id=841727105816461312&permissions=8&scope=bot%20applications.commands)

A [Discord](https://discord.com) bot with the goal of mimicking [Slack](https://slack.com)-like threads using the built-in reply function.

![Example thread](./example.png)


## Setup

```bash
git clone https://github.com/runarsf/discord-threads.git
cd discord-threads
printf "BOT_TOKEN=<BotToken>" > .env

# Manual setup
python -m pip install -r requirements.txt
./threads.py

# Docker
docker-compose up -d
```
