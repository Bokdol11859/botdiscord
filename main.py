import discord, asyncio, os
import youtube_dl
from discord.ext import commands
import json
import random

#
import discord
with open('config.json') as f:
    key = json.load(f)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"봇={bot.user.name}로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command(aliases = ['hi', 'ㅎㅇ'])
async def hello(ctx):
    await ctx.send('{}님 안녕하세요!'.format(ctx.author.name))

@bot.command(aliases=['주사위'])
async def dice(ctx):
    dice0={1:'⚀=1',2:'⚁=2',3:'⚂=3',4:'⚃=4',5:'⚄=5',6:'⚅=6'}#딕셔너리
    embed = discord.Embed(title="주사위 굴리는중", color=0x4432a8)
    dice1=random.randrange(1,7)
    dice11=dice0[dice1]
    dice2=random.randrange(1,7)
    dice22=dice0[dice2]
    embed.add_field(name="1번:game_die:",value=f"{dice11}",inline=True)
    embed.add_field(name="2번:game_die:", value=f"{dice22}",inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def serverInfo(ctx):
    members = [member.name for member in ctx.guild.members]
    await ctx.send(
        "{} 서버의 인원은 총 {} 명입니다.".format(
            ctx.guild.name,
            ctx.guild.member_count
        )
    )

#embed 기능 테스트 추가
@bot.command()
async def github(ctx,text):
    embed=discord.Embed(title=text,
                        url="https://github.com/{}".format(text),
                        description="{}'s github".format(text),
                        color=0xFF5733)
    await ctx.send(embed=embed)


@bot.command()
async def copy(ctx,*,text):
    await ctx.send(text)

#유튜브 기능 test----------------------------------------------------------

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send(str(bot.voice_clients[0].channel)+"채널에 연결 되었습니다.")

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()


@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 정지 된 상태입니다.")


@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 실행중입니다.")


@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    else:
        await ctx.send("이미 재생을 멈춘 상태입니다")

bot.run(key['token'])