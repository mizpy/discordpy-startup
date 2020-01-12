import discord
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
import os
import traceback

logged = 0

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
channel_id = os.environ['DISCORD_CHANNEL_ID']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event    
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    global logged
    logged = 1

@bot.command()
async def ping(ctx):
    print('pong')
    await ctx.send('pong')

@bot.command()
async def test_notice(ctx):
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    print(now)
    if logged == 1:
        print('send')
        channel = bot.get_channel(channel_id)
        await channel.send('演習おもらし注意報をお知らせしますっ！（テスト）')  
    
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    print(now)
    if logged == 1:
        # 時差は日本時間-9時間
        # 13:45->2:45
        # 17:45->8:45
        # 23:45->14:45
        if (now == '02:45') or (now == '08:45') or (now == '14:45'):
            print('send')
            channel = bot.get_channel(channel_id)
            await channel.send('演習おもらし注意報をお知らせしますっ！')  

#ループ処理実行
loop.start()
    
bot.run(token)
