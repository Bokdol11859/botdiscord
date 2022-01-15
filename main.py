import bs4
import discord, asyncio, os
import youtube_dl
from discord.ext import commands
import json
import random
from collections import deque

#
import discord
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

bot = commands.Bot(command_prefix='!')
song_list = deque()
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
async def play(ctx, msg):
    global song_list
    try:
        channel = ctx.author.voice.channel
        if not bot.voice_clients:
            await channel.connect()
            await ctx.send(str(bot.voice_clients[0].channel) + "채널에 연결 되었습니다.")
        print('접속 완료')
        # if bot.voice_clients[0].is_stoped() and not song_list.empty():
        ydl_opts = {'format': 'bestaudio'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        print('ffmpeg')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")  # 한국어!
        print('selenium')
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        print('chrome_bin')
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options) #변경
        print('chromedriver')
        driver.get("https://www.youtube.com/results?search_query=" + msg)
        print('get')
        source = driver.page_source
        print('beautifulsoup')
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl
        print('노래 다운 완료')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        voice = bot.voice_clients[0]
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        embed=discord.Embed(title=entireText+"를 재생합니다.", #변경
                            color=0xFF0000) #변경
        print('재생 완료')
        await ctx.send(embed=embed) #변경
        await ctx.send(url) #변경
    except:
        song_list.append(msg)
        await ctx.send("플레이리스트에 추가 되었습니다.")

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

@bot.command()
async def next(ctx):
    try:
        if bot.voice_clients[0].is_playing():
            bot.voice_clients[0].stop()
            msg = song_list.popleft()
            ydl_opts = {'format': 'bestaudio'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
            options.add_argument("lang=ko_KR")  # 한국어!

            options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(service=os.environ.get("CHROMEDRIVER_PATH"), options=options) #변경
            driver.get("https://www.youtube.com/results?search_query=" + msg)
            source = driver.page_source
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            entireText = entireNum.text.strip()
            musicurl = entireNum.get('href')
            url = 'https://www.youtube.com' + musicurl

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            voice = bot.voice_clients[0]
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            await ctx.send("다음 노래를 재생합니다.")
            embed = discord.Embed(title=entireText + "를 재생합니다.",  # 변경
                                  color=0xFF0000)  # 변경
            await ctx.send(embed=embed)  # 변경
            await ctx.send(url)  # 변경
        else:
            msg = song_list.popleft()
            ydl_opts = {'format': 'bestaudio'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
            options.add_argument("lang=ko_KR")  # 한국어!

            options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(service=os.environ.get("CHROMEDRIVER_PATH"), options=options) #변경
            driver.get("https://www.youtube.com/results?search_query=" + msg)
            source = driver.page_source
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            entireText = entireNum.text.strip()
            musicurl = entireNum.get('href')
            url = 'https://www.youtube.com' + musicurl

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            voice = bot.voice_clients[0]
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            #,after=lambda e: asyncio.run_coroutine_threadsafe(autoNext, bot.loop)

            await ctx.send("다음 노래를 재생합니다.")
            embed = discord.Embed(title=entireText + "를 재생합니다.",  # 변경
                                  color=0xFF0000)  # 변경
            await ctx.send(embed=embed)  # 변경
    except:
        await ctx.send("뒤에 재생 할 음악이 존재하지 않습니다.")


@bot.command()
async def playlist(ctx):
    embed = discord.Embed(title=("현재 ["+str(len(song_list))+"]개의 곡이 플레이리스트에 담겨 있습니다.")
                          , color=0xff69b4)
    await ctx.send(embed=embed)
    for i in song_list:
        await ctx.send(i)

        
access_token = os.environ['token']
bot.run(access_token)
