import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Slash(commands.Cog, name="Slash"):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='ping', description='pong!')
    async def _pingu(self, ctx: SlashContext):
        await ctx.send(f'🏓 `{round(self.bot.latency * 1000)}ms`')


def setup(bot):
    bot.add_cog(Slash(bot))
