import discord
from discord.ext import commands


def channelerror(input, command, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Error", description="Insufficent Permissions", color=discord.Color.red())
        return embed
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error", description=f"Format message like this `{command} <{input}>`",
                              color=discord.Color.red())
        return embed
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Error", description=f"Input must be a {input}", color=discord.Color.red())
        return embed

    if isinstance(error, KeyError):
        embed = discord.Embed(title="Error", description=f"Shut the fuck up", color=discord.Color.red())
        return embed
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error", description=f"Command not found, please check syntax", color=discord.Color.red())
        return embed