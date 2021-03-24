from discord.ext import commands
from cogs.functions import datePretty
import datetime


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def dm(self, ctx, userid, *, message):
        print("function works")
        dmUser = self.bot.get_user(int(userid))
        if dmUser.dm_channel is None:
            chan = await dmUser.create_dm()
            print("channel existing")
        else:
            chan = dmUser.dm_channel
            print("channel created")
        await chan.send(message)
        await ctx.send(f"Message sent to {dmUser.name}", delete_after=2.5)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def oldest(self, ctx):
        oldestDate = datetime.datetime(2021, 12, 31)
        oldestUser = ''
        oldestDay = 0
        oldestYear = 0
        oldestMonth = 0
        for i in ctx.guild.members:
            date = datePretty(i.created_at)
            year = int(date[6:10])
            month = int(date[0:2])
            day = int(date[3:5])
            accountDate = datetime.datetime(year, month, day)
            if accountDate < oldestDate and i.bot is False:
                oldestUser = i
                oldestYear = year
                oldestMonth = month
                oldestDay = day
                oldestDate = accountDate
        await ctx.send(f'The user with the oldest account is `{oldestUser.display_name}` '
                       f'with their account being created on `{oldestMonth}-{oldestDay}-{oldestYear}`')


def setup(bot):
    bot.add_cog(Owner(bot))
