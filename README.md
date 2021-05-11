# discord-threads
A discord bot that attempts to mimic Slack-like threads using Discord's built-in reply-function.

When replying to a message, a new category named `threads` is created, in that category a channel named `<UserName>-<ReferencedMessageID>` is created. The referenced message and reply are embedded with a link to the original message.
All future replies to that message will be sent in the same channel.

A public instance is *currently* not available.

## Setup

```bash
git clone https://github.com/runarsf/discord-threads.git
cd discord-threads
printf "BOT_TOKEN=<BotToken>" > .env

# Manual setup
python -m pip install -r requirements.txt
./threads.py

# Docker
# ...Adding tomorrow
```
