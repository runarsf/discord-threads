import os
import datetime
from inspect import signature
import config as cfg

import discord
from discord.ext import commands


class Help(commands.Cog, name="Help"):

    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.command()
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx):
        """Gets all cogs and commands of mine.
           https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html?highlight=commands#command
           https://github.com/Rapptz/discord.py/blob/967d43c35b4d4c288d47a9eb9d374bef34292f1d/discord/ext/commands/bot.py
        """
        embed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```apache\n{", ".join(cfg.prefixes)}```', color=discord.Color.from_rgb(48, 105, 152))
        for index, command in enumerate(self.bot.commands, start=2):
            nameAliases = str(command) if not ' | '.join(command.aliases) else str(' • '.join(str(command).split(" ")+command.aliases))
            if not command.hidden:
                embed.add_field(name=nameAliases+str(f' `{command.cog.qualified_name}`'), value=str(command.help.split('\n', 1)[0][:30]), inline=False)
        await ctx.send(embed=embed)
        '''


    @commands.command(name='help', aliases=['man'])
    async def help(self, ctx, *, command: str = ''):
        # No command provided
        if not command:
            help_embed = discord.Embed(timestamp=datetime.datetime.utcnow(),
                                       description=f'```less\n{", ".join(cfg.prefixes)}\n```',
                                       color=discord.Color.from_rgb(48, 105, 152))
            help_embed.set_footer(text='⚙️ All Commands')
            for cog in self.bot.cogs:
                body = ''
                for cmd in self.bot.commands:
                    if str(cmd.cog.qualified_name) == str(cog) and not cmd.hidden:
                        nameAliases = str(cmd) if not cmd.aliases else ' / '.join(str(cmd).split(" ")+cmd.aliases)
                        body += f'  • {nameAliases}\n'
                if body:
                    help_embed.add_field(name=str(cog), value=body, inline=False)
            await ctx.send(embed=help_embed)
            return

        # Command is a cog
        cog = self.bot.get_cog(command)
        if cog is None:
            cog = self.bot.get_cog(command.title())
        if command and cog is not None:
            help_embed = discord.Embed(timestamp=datetime.datetime.utcnow(),
                                       description=f'```\n{cog.description}\n```' if cog.description else '',
                                       color=discord.Color.from_rgb(75, 187, 112))
            help_embed.set_footer(text=f'⚙️ {cog.qualified_name}')

            body = ''
            for cmd in self.bot.commands:
                if str(cmd.cog.qualified_name) == str(cog.qualified_name) and not cmd.hidden:
                    nameAliases = str(cmd) if not cmd.aliases else ' / '.join(str(cmd).split(" ")+cmd.aliases)
                    body += f'  • {nameAliases}\n'

            if body:
                help_embed.add_field(name='Commands', value=body, inline=False)

            await ctx.send(embed=help_embed)
            return

        # Command is a command
        for cmd in self.bot.commands:
            if str(cmd) == str(self.bot.get_command(command)):
                nameAliases = str(cmd) if not cmd.aliases else ' / '.join(str(cmd).split(" ")+cmd.aliases)
                usage = f'{ctx.prefix}{cmd}'
                for key, value in cmd.clean_params.items():
                    usage += f' <{value}>'
                #await ctx.send(str(cmd.__doc__)[:1990])
                #await ctx.send(str(cmd.callback)[:1990])
                help_embed = discord.Embed(title='',
                                           timestamp=datetime.datetime.utcnow(),
                                           description=f'```markdown\n{usage}```\n{cmd.help if cmd.help else ""}',
                                           color=discord.Color.from_rgb(194, 124, 13))
                help_embed.set_author(name=nameAliases, icon_url=str(ctx.message.author.avatar_url))
                help_embed.set_footer(text=f'⚙️ {cmd.cog.qualified_name}')

                await ctx.send(embed=help_embed)
                return


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
