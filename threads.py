#!/usr/bin/env python3
import discord
import asyncio
import json
import os
from config import log
import config as cfg
from datetime import datetime
from discord_slash import SlashCommand

from discord.ext import commands

def get_prefix(_bot, message):
    if message.guild:
        return commands.when_mentioned_or(*cfg.prefixes)(_bot, message)
    return commands.when_mentioned_or(*[])(_bot, message)

bot = commands.Bot(command_prefix=get_prefix,
                   #description=c.description,
                   case_insensitive=True)
                   #intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

cogs = ['cogs.spool',
        'cogs.helpers',
        'cogs.commands',
        'cogs.owner',
        'cogs.help',
        'cogs.slash']

for cog in cogs:
    bot.load_extension(cog)

@bot.event
async def on_ready():
    joined_guilds = []
    for guild in bot.guilds:
        joined_guilds.append(f' - {str(guild.id).ljust(20)} {guild.name}')

    ready_message = [
        'Logged in as:',
        f'{bot.user.name}: {bot.user.id}',
        f'Discord Version: {discord.__version__}',
        f'\nBot currently running in {len(bot.guilds)} server(s):',
        '\n'.join(joined_guilds)
    ]
    log.info('\n'.join(ready_message))

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("with threads"))


if __name__ == '__main__':
    log.debug('Starting bot...')
    bot.run(cfg.token, bot=True, reconnect=False)
