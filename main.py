import discord, asyncio, os
from discord.ext import commands
import json

with open('config.json') as f:
    key = json.load(f)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"봇={bot.user.name}로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command(aliases = ['hi', '안녕', 'ㅎㅇ'])
async def hello(ctx):
    await ctx.send('{}님 안녕하세요!'.format(ctx.author.name))

@bot.command()
async def copy(ctx,*,text):
    await ctx.send(text)

bot.run(key['token'])
