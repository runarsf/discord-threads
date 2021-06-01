import config as cfg

import discord
from discord.ext import commands


async def user_owns_thread(ctx):
    #is_owner = await ctx.bot.is_owner(ctx.author)
    #if is_owner:
    #    return True
    #else:
    return True
    #return str(ctx.message.channel.name).endswith(str(ctx.message.author.id))

def thread_owner():
    async def checker(ctx):
        return await user_owns_thread(ctx)
    return commands.check(checker)