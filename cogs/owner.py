import discord
import asyncio
from discord.ext import commands
from config import log


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def _load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
            try:
                self.bot.load_extension(f'cogs.{cog}')
            except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
                await ctx.message.add_reaction('👎')
            else:
                await ctx.message.add_reaction('👌')
        else:
            await ctx.message.add_reaction('👌')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def _unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
            try:
                self.bot.unload_extension(f'cogs.{cog}')
            except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
                await ctx.message.add_reaction('👎')
            else:
                await ctx.message.add_reaction('👌')
        else:
            await ctx.message.add_reaction('👌')

    @commands.command(name='reload', hidden=True, aliases=['r'])
    @commands.is_owner()
    @commands.guild_only()
    async def _reload(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
        except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
            try:
                self.bot.reload_extension(f'cogs.{cog}')
            except (AttributeError, ImportError, commands.CommandError, commands.ExtensionNotLoaded) as error:
                await ctx.message.add_reaction('👎')
                #await ctx.send(f'```py\nCould not reload {cog}: {type(error).__name__} - {error}\n```')
            else:
                await ctx.message.add_reaction('👌')
        else:
            await ctx.message.add_reaction('👌')


def setup(bot):
    bot.add_cog(Owner(bot))
