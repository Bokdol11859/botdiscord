import discord, asyncio, os
from discord.ext import commands
import json

with open('config.json') as f:
    key = json.load(f)

game = discord.Game("Currently Testing")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)

@bot.command()
async def hello(ctx):
    await ctx.send('{}님 안녕하세요!'.format(ctx.author.name))

bot.run(key['token'])

#test1fdsa
#hello
#hello
#test1