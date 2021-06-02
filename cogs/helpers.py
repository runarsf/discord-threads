import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from config import log

# FIXME: https://i.runarsf.dev/runar/fUmoyEjE11.png

class Helpers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_command_error(self, ctx, exception):
        log.info(exception)
        if isinstance(exception, commands.errors.MissingPermissions):
            exception = f'Sorry {ctx.message.author.name}, you don\'t have permissions to do that!'
        elif isinstance(exception, commands.errors.CheckFailure):
            exception = f'Sorry {ctx.message.author.name}, you don\'t have the necessary roles for that!'
        elif isinstance(exception, TimeoutError):
            log.warn(f'TimeoutError: {exception}')
            return

        error_embed = discord.Embed(title='',
                                    timestamp=datetime.utcnow(),
                                    description=f'> ```css\n> {exception}```',
                                    color=discord.Color.from_rgb(200, 0, 0))
        error_embed.set_author(name='Woops!',
                            icon_url=str(ctx.message.guild.icon_url))
        error_embed.set_footer(text=str(type(exception).__name__))
        error_message = await ctx.send(embed=error_embed)

        await error_message.add_reaction('❔')

        def check_reaction(reaction, user):
            return user != ctx.bot.user and str(reaction.emoji) == '❔'
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0, check=check_reaction)
        except asyncio.TimeoutError:
            await error_message.remove_reaction('❔', ctx.bot.user)
        else:
            await error_message.remove_reaction('❔', ctx.bot.user)
            if exception.__doc__:
                error_embed.add_field(name='Details', value=exception.__doc__, inline=False)
            #if exception.__cause__:
            #    error_embed.add_field(name='Cause', value=exception.__cause__ , inline=False)
            await error_message.edit(embed=error_embed)


def setup(bot):
    bot.add_cog(Helpers(bot))
