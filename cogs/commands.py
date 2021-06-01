import discord
import asyncio
from discord.ext import commands
from config import log
from cogs.utils import checks


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete', aliases=['slett'])
    @commands.guild_only()
    #@checks.thread_owner()
    async def _delete(self, ctx):
        await ctx.message.send("Deleting thread...")

    @commands.command(name='purge')
    @commands.guild_only()
    #@checks.thread_owner()
    async def _purge(self, ctx):
        thread_category = None
        for category in ctx.message.guild.categories:
            if category.name == 'threads':
                thread_category = category
                break
        if not thread_category:
            await ctx.message.channel.send('No threads-category found...')
            return

        message = await ctx.message.channel.send('Purging all threads...')

        for channel in thread_category.text_channels:
            await channel.delete(reason='Purging threads')
        await thread_category.delete(reason='Purging threads')

        # FIXME: Doesn't update message
        if ctx.message.channel.category_id != thread_category.id:
            message.edit(content="All threads successfully deleted", delete_after=25)


def setup(bot):
    bot.add_cog(Commands(bot))
