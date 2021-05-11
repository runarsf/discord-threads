import discord
import asyncio

# https://github.com/fengsp/color-thief-py/blob/master/examples/demo.py

import urllib.request
import requests
from io import BytesIO
from PIL import Image

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


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
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

            thread_channel = None
            for channel in message.guild.text_channels:
                if channel.category and channel.category.name == 'threads' and channel.name.endswith(str(referenced.id)):
                    thread_channel = channel

            if not thread_channel:
                thread_channel = await message.guild.create_text_channel(name=f'{referenced.author.name}-{referenced.id}',
                                                                         category=thread_category,
                                                                         topic=referenced.content)
                embed = discord.Embed(description=f'> [original message]({referenced.jump_url})\n{referenced.content}',
                                      colour=getDominantColor(referenced.author.avatar_url))
                embed.set_author(name=referenced.author.name,
                                 icon_url=referenced.author.avatar_url,
                                 url=referenced.jump_url)
                if referenced.attachments:
                    embed.set_image(url=referenced.attachments[0].url)
                await thread_channel.send(embed=embed)

            embed = discord.Embed(description=message.content,
                                  colour=getDominantColor(message.author.avatar_url))
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
            await thread_channel.send(embed=embed)

            # TODO: Delete command for thread owner / admins
            # TODO: Delete original messages?
            # TODO: Permissions
            # TODO: Recursive detection for replies


def setup(bot):
    bot.add_cog(Utils(bot))
