import discord
import asyncio

# https://github.com/fengsp/color-thief-py/blob/master/examples/demo.py

import urllib.request
import requests
from io import BytesIO
from PIL import Image

from config import log
from discord.ext import commands


def getDominantColor(filename: str):
    try:
        #Resizing parameters
        width, height = 150, 150
        response = requests.get(filename)
        image = Image.open(BytesIO(response.content))

        #image.seek(image.tell() + 1)
        image = image.resize((width, height), resample=0)
        #Get colors from image object
        pixels = image.getcolors(width * height)
        #Sort them by count number(first element of tuple)
        sorted_pixels = sorted(pixels, key=lambda t: t[0])
        #Get the most frequent color
        dominant_color = sorted_pixels[-1][1]
        hexColor = discord.Color.from_rgb(
            dominant_color[0], dominant_color[1], dominant_color[2])
        return hexColor
    except:
        #return discord.Color.from_rgb(48, 105, 152)
        return 0x306998


class Spool(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.guild is None or message.author.bot:
            return
        if message.reference and message.reference.resolved and not message.is_system():
            referenced = message.reference.resolved
            thread_category = None
            for category in message.guild.categories:
                if category.name == 'threads':
                    thread_category = category
                    break
            if not thread_category:
                thread_category = await message.guild.create_category('threads')

            leid = message.guild.get_channel(referenced.id)
            log.info(leid)

            #thread_names = []
            #for channel in thread_category.text_channels:
            #    thread_names.append(channel.name)

            # Does the message have a parent?
            # yes -> Is the message already a thread?
            #        yes -> Use this message and break. This will be the thread used.
            #         no -> Use this message and continue. Same test will be attempted for this? Parent?
            #  no -> Use this message and break. A thread will be created if it doesn't exist.
            # intermediate = referenced
            # while True:
            #     # Intermediate has a parent and is therefore not at the end of the chain.
            #     if intermediate.reference and intermediate.reference.resolved:
            #         # Intermediate is already a thread and we can use this from now on.
            #         if any(s.endswith(str(intermediate.id)) for s in thread_names):
            #             # Yes
            #             log.info("1")
            #             referenced = intermediate
            #             break
            #         else: # Intermediate is not at the end of the chain or already a thread.
            #             log.info("2")
            #             intermediate = intermediate.reference.resolved
            #             continue
            #     else: # Reached the end of reply chain
            #         log.info("3")
            #         referenced = intermediate
            #         break

                #if any(s.endswith(str(intermediate.id)) for s in thread_names):
                #    log.info("A thread with that name already exists")
                #    referenced = intermediate
                #    break
                
            # Get thread-channel if it already exists
            thread_channel = None
            for channel in thread_category.text_channels:
                if channel.name.endswith(str(referenced.id)):
                    thread_channel = channel

            # Create new thread-channel if it didn't already exist
            if not thread_channel:
                #thread_channel = await message.guild.create_text_channel(name=f'{referenced.author.name}-{referenced.id}',
                #                                                         category=thread_category,
                #                                                         topic=referenced.content,
                #                                                         permissions_synced=False)
                thread_channel = await message.channel.clone(name=f'{referenced.author.name}-{referenced.id}',
                                                             reason=f'Creating thread from {referenced.id}')
                await thread_channel.move(category=thread_category,
                                          beginning=True,
                                          sync_permissions=False,
                                          reason='Moving thread-channel to threads category')
                embed = discord.Embed(description=f'> [original message]({referenced.jump_url})\n{referenced.content}',
                                      colour=getDominantColor(referenced.author.avatar_url))
                embed.set_author(name=referenced.author.name,
                                 icon_url=referenced.author.avatar_url,
                                 url=referenced.jump_url)
                if referenced.attachments:
                    embed.set_image(url=referenced.attachments[0].url)
                original_message = await thread_channel.send(embed=embed)
                await original_message.pin() # Delete this message

            embed = discord.Embed(description=message.content,
                                  colour=getDominantColor(message.author.avatar_url))
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
            await thread_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Spool(bot))
