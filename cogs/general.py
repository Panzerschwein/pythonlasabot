import datetime
from datetime import date
import calendar
from datetime import datetime
import gspread
from discord.ext import commands
import discord
from cogs.functions import datePretty, handleFile
from cogs.localerrors import channelerror

levelRoles = {'Freshmen': 615293283693756447, 'Sophomore': 615293021059285019, 'Junior': 615293126294110223,
              'Senior': 615293126294110223}
noAdvDay = {'one': ['8:15', '9:50'], 'two': ['9:55', '11:30']}


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='schedule', aliases=['bell'])
    async def schedule(self, ctx, *, arg1=None):
        #if ctx.message.author.id == 208571050957602816:
            #await ctx.send('wouldn\'t you like you know lol')
        if arg1 is None:
            await ctx.send(file=discord.File('noadv.png'))
        elif 'adv' in arg1.lower():
            await ctx.send(file=discord.File('adv.png'))
        elif 'today' in arg1.lower():
            mydate = date.today()
            weekDay = calendar.day_name[mydate.weekday()]
            if weekDay == 'Tuesday' or weekDay == 'Wednesday':
                await ctx.send(file=discord.File('adv.png'))
            else:
                await ctx.send(file=discord.File('noadv.png'))

    @schedule.error
    async def schedule_error(self, ctx, error):
        embed = channelerror('channel id', 'setaudit', error)
        await ctx.send(embed=embed)


    @commands.command(name='mock')
    async def mock(self, ctx, *, arg1=None):
        messages = await ctx.channel.history(limit=2).flatten()
        print(messages)
        await ctx.message.delete()
        contextMessage = messages[1]
        messageMentions =contextMessage.mentions
        print(messageMentions)
        if arg1 == None:
            counter = 0
            newMessage = ''
            mockMessage = messages[1].content.upper()
            mockMessage = discord.utils.escape_mentions(mockMessage)
            for i in mockMessage:
                if counter == 0:
                    newMessage = newMessage+i.lower()
                    counter = 1
                else:
                    newMessage = newMessage+i
                    counter = 0




            await ctx.send(newMessage)
        else:
            await ctx.send('Function not in yet')


    @commands.command(name='school', aliases=['class'])
    async def school(self, ctx):
        mydate = date.today()
        time = datetime.now()
        weekDay = calendar.day_name[mydate.weekday()]
        print(weekDay)
        if weekDay != 'Tuesday' or weekDay != 'Wednesday':
            print(True)
            if 8 <= time.hour <= 9 and 15 <= time.minute <= 54:
                await ctx.send(f"It is first/fifth period. Second/sixth period starts in {55 - time.minute}")
            if 9 <= time.hour <= 11 and 55 <= time.minute <= 34:
                await ctx.send(f"It is second/sixth period. Lunch starts in {abs(35 - time.minute)}")
            if 12 <= time.hour <= 2 and 40 <= time.minute <= 19:
                await ctx.send(f"It is third/seventh period. Fourth/eighth starts in {abs(20 - time.minute)}")
            if 2 <= time.hour <= 3 and 20 <= time.minute <= 55:
                await ctx.send(f"It is fourth/seventh period. The school day ends in  {abs(55 - time.minute)}")
        else:
            await ctx.send("broken bot")

    @commands.command(name='flatten', aliases=['flat'])
    async def flatten(self, ctx):
        messages = await ctx.channel.history(limit=20).flatten()
        print(ctx.channel.history(limit=20))
        print(messages)
        await ctx.send("Displayed in console")

    @commands.command(name='ping', aliases=['pong', 'ping*'])
    async def ping(self, ctx):
        t = await ctx.send('Pinging...')
        ms = (t.created_at - ctx.message.created_at).total_seconds() * 1000
        if ctx.invoked_with == 'ping':
            pingPong = 'Pong'
        else:
            pingPong = 'Ping'

        await t.edit(content=f':ping_pong: {pingPong}! `{int(ms)}ms`')



    @commands.command(name='userinfo', aliases=['ui'])
    @commands.guild_only()
    async def userinfo(self, ctx, arg1: discord.Member = None):
        if arg1 is None:
            user = ctx.message.author
        else:
            user = arg1
        isBot = user.bot
        if isBot:
            if str(user.status) == 'dnd':
                status = ':robot: Do not Disturb'
            else:
                status = ':robot: ' + str(user.status).capitalize()
        else:
            if str(user.status) == 'dnd':
                status = 'Do not Disturb'
            else:
                status = str(user.status).capitalize()
        # status = 'God'
        embed = discord.Embed(title=f"{user.display_name}", timestamp=datetime.utcnow(),
                              color=discord.Color.blue())
        embed.add_field(name="Account info", value=f"{user}", inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        adate = datePretty(user.created_at)
        cdate = datePretty(date.today())
        embed.add_field(name="Account created on", value=f"{adate}", inline=False)
        embed.add_field(name="Today's date", value=f"{cdate}", inline=False)
        jDate = datePretty(user.joined_at)
        embed.add_field(name="Joined guild on", value=f"{jDate}", inline=False)
        embed.set_thumbnail(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(name='verify')
    @commands.guild_only()
    async def verify(self, ctx):
        gc = gspread.service_account(filename='lasabot-d52b518a4809.json')
        sh = gc.open("Verification Responses")
        worksheet = sh.sheet1
        values_list = worksheet.col_values(7)
        values_list.pop(0)
        values_list.pop(0)
        print(values_list)
        veri_dict = dict()
        counter = 3
        for i in values_list:
            veri_dict[i] = str(counter)
            counter = counter + 1
        print(veri_dict)
        uniqueChan = handleFile('usercodes.txt')
        code = uniqueChan[ctx.message.author.id]
        x = 0
        for i in veri_dict:
            if i == str(code):
                x = veri_dict[i]
        rowList = worksheet.row_values(int(x))
        print(rowList)
        if rowList[4] == 'LASA':
            await ctx.send("Verified!")
            level = rowList[5]
            role = ctx.guild.get_role(levelRoles[level])
            memberRole = ctx.guild.get_role(610536343839309864)
            await ctx.message.author.add_roles(role)
            await ctx.message.author.add_roles(memberRole)
            verification_chan = ctx.guild.get_channel_id(616033613703544882)
            await verification_chan.send(f'**New Member** \n Discord username: `{rowList[3]}` \n Real name: `{rowList[1]} \n '
                                         f'Middle school: `{rowList[2]} \n High school: `LASA` \n Grade: `{level}`')

        else:
            dmUser = ctx.message.author
            if dmUser.dm_channel is None:
                chan = await dmUser.create_dm()
            else:
                chan = dmUser.dm_channel
            await chan.send("Currently, the LASA Server is for LASA Students only. If yu")
            await ctx.guild.kick(ctx.message.author, reason="Is not from LASA")


def setup(bot):
    bot.add_cog(General(bot))
