from cogs.functions import handleFile, editFile
import discord
from discord.ext import commands
import gspread
intents = discord.Intents(messages=True, guilds=True, members=True, presences=True)
gc = gspread.service_account(filename='lasabot-d52b518a4809.json')

custom_prefixes = handleFile('setprefix.txt')
default_prefixes = ['*']

tokenFile = open('token.txt', 'r')
TOKEN = str(tokenFile.read().strip())
tokenFile.close()

async def determine_prefix(bot, message):
    guild = message.guild
    # Only allow custom prefixes in guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

initial_extensions = ['cogs.general', 'cogs.mod', 'cogs.owner', 'cogs.help']


bot = commands.Bot(command_prefix=determine_prefix, description='a LasaBot', help_command=None, intents=intents)

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.command(name='prefix', aliases=['setprefix', 'sp'])
@commands.has_permissions(manage_messages=True)
async def set_prefix(ctx, *, arg):
    custom_prefixes[ctx.guild.id] = arg or default_prefixes
    editFile('setprefix.txt', custom_prefixes)
    await ctx.send(f"Prefix changed to `{arg}`")

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    print(f'Successfully logged in and booted...!')


bot.run(TOKEN, bot=True, reconnect=True)
