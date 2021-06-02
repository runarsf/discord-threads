import discord
import asyncio
from discord.ext import commands
from config import log
from cogs.utils import checks


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def _ping(self, ctx):
        await ctx.send(f'🏓 `{round(self.bot.latency * 1000)}ms`')

    @commands.command(name='delete', aliases=['slett'])
    @commands.guild_only()
    #@checks.thread_owner()
    async def _delete(self, ctx):
        await ctx.send("Deleting thread...")

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
            await ctx.send('No threads-category found...')
            return

        confirmation_emojis = [ '👎', '👍' ]
        confirmation = await ctx.message.channel.send('Are you sure you want to delete all threads?')

        for emoji in confirmation_emojis:
            await confirmation.add_reaction(emoji)

        def check_reaction(reaction, user):
            return (user != ctx.bot.user and
                    user.id == ctx.message.author.id and
                    str(reaction.emoji) in confirmation_emojis)

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15, check=check_reaction)
        except asyncio.TimeoutError:
            for emoji in confirmation_emojis:
                await confirmation.remove_reaction(emoji, ctx.bot.user)
        else:
            for emoji in confirmation_emojis:
                await confirmation.remove_reaction(emoji, ctx.bot.user)
            if str(reaction.emoji) == confirmation_emojis[1]:
                await confirmation.edit(content=f'Purging all threads with permission from {ctx.message.author.mention}')

                for channel in thread_category.text_channels:
                    await channel.delete(reason='Purging threads with permission from {ctx.message.author.name} ({ctx.message.author.id})')
                await thread_category.delete(reason='Purging threads with permission from {ctx.message.author.name} ({ctx.message.author.id})')

                if ctx.message.channel.category_id != thread_category.id:
                    await confirmation.edit(content="All threads successfully deleted", delete_after=25)
            elif str(reaction.emoji) == confirmation_emojis[0]:
                await confirmation.edit(content='Purge aborted 🙂')
                # await confirmation.remove_reaction(confirmation_emojis[0], ctx.message.author)


def setup(bot):
    bot.add_cog(Commands(bot))
