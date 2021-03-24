import discord
from discord.ext import commands
from cogs.functions import handleFile, editFile, generateID
from cogs.localerrors import channelerror

auditChan = handleFile('auditChannel.txt')
messChan = handleFile('messagelog.txt')


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setmessagelog', aliases=['sma'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def setmessagelog(self, ctx, chanid):
        chanid = int(chanid)
        messChan[ctx.guild.id] = chanid
        editFile('messagelog.txt', messChan)
        await ctx.send(f"Message log channel set to {self.bot.get_channel(chanid).mention}")

    @setmessagelog.error
    async def setmessagelog_error(self, ctx, error):
        embed = channelerror('channel id', 'setmessagelog', error)
        await ctx.send(embed=embed)

    @commands.command(name='setaudit', aliases=['sa'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def setaudit(self, ctx, chanid):
        chanid = int(chanid)
        auditChan[ctx.guild.id] = chanid
        editFile('auditChannel.txt', auditChan)
        await ctx.send(f"Audit channel set to {self.bot.get_channel(chanid).mention}")

    @setaudit.error
    async def setaudit_error(self, ctx, error):
        embed = channelerror('channel id', 'setaudit', error)
        await ctx.send(embed=embed)

    @commands.command(name='purge', aliases=['p'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(self, ctx, amount):

        amount = int(amount) + 1
        messages = await ctx.channel.history(limit=amount).flatten()
        file = open('message.txt', 'w')
        for i in messages:
            info = i.content
            user = i.author
            time = i.created_at
            file.write(f'Author: {user} **Message Send Time: {time} \n Content: {info} \n')
        file.close()
        disFile = discord.File('message.txt')
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f'Purged {len(deleted) - 1} message(s)', delete_after=5)
        try:
            chan = self.bot.get_channel(int(messChan[ctx.guild.id]))
            deleteL = len(deleted) - 1
            await chan.send(f'{ctx.author} purged {deleteL} message(s) in {ctx.channel.mention}')
            await chan.send(file=disFile)
        except:
            await ctx.send("Please set an message log through the `setmessagelog <channel id>` command",
                           delete_after=5)

    @purge.error
    async def purge_error(self, ctx, error):
        embed = channelerror('number of messages', 'purge', error)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        text = await self.bot.get_context(message)
        if text.valid:
            pass
        else:
            if message.author == self.bot.user:
                return
            messageM = message.mentions
            for i in messageM:
                if i == self.bot.user:
                    custom_prefixes = handleFile('setprefix.txt')
                    try:
                        prefix = custom_prefixes[message.guild.id].strip('[]')
                    except:
                        prefix = '*'
                    await message.channel.send(f"My prefix is {prefix} and my help command is `{prefix}help`")
            if message.guild.id == 608035355345813534:
                if message.channel.id == 778771740095414332:
                    if str(message.attachments) == '[]':
                        role = message.guild.get_role(610536160338378765)
                        if role not in message.author.roles and message.author.bot is False:
                            await message.delete()
                            artChannel = self.bot.get_channel(778771740095414332)
                            await message.channel.send(f"Please refrain from talking in {artChannel.mention}",
                                                       delete_after=5)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"guild joined by {member.id} ")
        if member.guild.id == 608035355345813534:
            userid = member.id
            dmUser = self.bot.get_user(int(userid))
            if dmUser.dm_channel is None:
                chan = await dmUser.create_dm()
            else:
                chan = dmUser.dm_channel
            uniqueID = generateID()
            uniqueChan = handleFile('usercodes.txt')
            uniqueChan[member.id] = uniqueID
            editFile('Cusercodes.txt', uniqueChan)

            message = f"**Welcome to the LASA Discord** " \
                      f"\n Please fill out this verification form to be let into the server - " \
                      f"https://forms.gle/omKYwimJ8gucQVfh9 \n Your unique ID is `{uniqueID}` " \
                      f"\n Once you finish, please go to `#verification` and type `lasa verify`"
            await chan.send(message)


def setup(bot):
    bot.add_cog(Moderation(bot))
