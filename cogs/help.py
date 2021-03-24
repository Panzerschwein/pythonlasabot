import traceback
import sys
from discord.ext import commands
import discord
from cogs.functions import handleFile


def embedCreate(name, value, embed):
    embed.add_field(name=f'{name}', value=f'{value}', inline=False)

botcommands = {'General': {'ping': {'des':'Pings the bot!'}, 'prefix': {'des':'Change the bot\'s prefix'}, 'mock': {'des':'Mentally destroys anybody it\'s used on'}, 'userinfo': {'des': 'Gives info on the user'}},
               'Moderation': {'setmessagelog': {'des':'Sets a message logging channel'}, 'setaudit': {'des':'sets a audit logging channel'}, 'purge': {'des':'Purges messages'}}
               }

botDetails = {'ping': {'descrip': 'Pings the bot!', 'aliases': ['pong'], 'perms': [], 'guild': False, 'usage': ['ping'], 'category': 'General'},
              'prefix': {'descrip': 'Change the bot\'s prefix','aliases': ['setprefix', 'sp'], 'perms': ['Manage Messages'], 'guild': True, 'usage': ['prefix <new prefix>'], 'category': 'General'},
              'setmessagelog': {'descrip': 'Sets a message logging channel', 'aliases': ['sma'], 'perms': ['Manage Messages'], 'guild': True, 'usage': ['setmessagelog <channel id>'], 'category': 'Moderation'},
              'setaudit': {'descrip': 'Sets a audit logging channel', 'aliases': ['sa'], 'perms': ['Manage Messages'], 'guild': True, 'usage': ['setaudit <channel id>'], 'category':'Moderation'},
              'purge': {'descrip': 'Purges messages', 'aliases': ['p'], 'perms': ['Manage Messages'], 'guild': True, 'usage': ['purge <number of messages>'], 'category':'Moderation'},
              'mock': {'descrip': 'Mentally destroys anybody it\'s used on', 'aliases': [''], 'perms': [], 'guild': True, 'usage': ['mock'], 'category': 'General'},
              'userinfo':{'descrip': 'Gives info on the user', 'aliases': ['ui'], 'perms':[], 'guild': True, 'usage': ['userinfo', 'userinfo <user>'], 'category': 'General'}}


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help(self, ctx, arg1=None):
        custom_prefixes = handleFile('setprefix.txt')
        default_prefixes = ['*']
        try:
            prefix = custom_prefixes[ctx.guild.id].strip('[]')
        except:
            prefix = '*'
        if arg1 is None:
            embed = discord.Embed(title="Help Menu",
                                  description=f'For more detailed info, use `{prefix}help <command name>`',
                                  color=discord.Color.purple())

            for category in sorted(botcommands):
                x = botcommands[category]
                totcmd = ""
                for i in x:
                    des = x[i]['des']
                    totcmd = totcmd + f'`{i}` - {des} \n'
                embed.add_field(name=f'{category}', value=f'{totcmd}', inline=False)
            await ctx.send(embed=embed)

        else:
            cmd = botDetails[arg1.lower()]
            des = cmd['descrip']
            ali = cmd['aliases']
            perm = cmd['perms']
            print(perm)
            guild = cmd['guild']
            use = cmd['usage']
            cate = cmd['category']
            embed = discord.Embed(description=f'{arg1.capitalize()}', color=discord.Color.purple())
            embedCreate('Description', des, embed)
            usage = ''
            for i in use:
                usage = usage + '`'+ prefix + i + '` \n'
            usage = usage.strip()
            embed.add_field(name='Usage', value=f'{usage}', inline=False)
            #embedCreate('Category', cate, embed)
            embed.add_field(name='Category', value=cate, inline=False)
            if str(ali).strip('[]') == '':
                ali_comp = 'None'
            else:
                ali_comp = ''
                for i in ali:
                    ali_comp = ali_comp + '`' + i + '`, '
                ali_comp = ali_comp.strip(', ')

            #embedCreate('Aliases', ali_comp, embed)
            embed.add_field(name='Aliases', value=ali_comp, inline=False)
            perm_comp = ""
            if str(perm).strip('[]') == '':
                perm_comp = "None"
            else:
                for i in perm:
                    perm_comp = perm_comp + i + ', '
                perm_comp = perm_comp.strip(', ')
            #perm_comp = "LOLLLL"
            #embedCreate('Permissions required', perm_comp, embed)
            embed.add_field(name='Permissions required', value=perm_comp, inline=False)

            if guild:
                mess = 'Guilds'
            else:
                mess = "Guilds and DMs"
            #embedCreate('Restricted to', mess, embed)
            embed.add_field(name='Restricted to', value=mess, inline=False)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))