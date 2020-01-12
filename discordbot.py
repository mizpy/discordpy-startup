import discord
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
import os
import traceback

#bot_logged = 0
client_logged = 0

#bot = commands.Bot(command_prefix='/')
client = discord.Client()

token = os.environ['DISCORD_BOT_TOKEN']
channel_id = int(os.environ['DISCORD_CHANNEL_ID'])

#@bot.event
#async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)

#@bot.event    
#async def on_ready():
#    print('bot Logged in as')
#    print(bot.user.name)
#    print(bot.user.id)
#    print('------')
#    global bot_logged
#    bot_logged = 1

@client.event
async def on_ready():
    print('client Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global client_logged
    client_logged = 1    
    
#@bot.command()
#async def ping(ctx):
#    print('pong')
#    await ctx.send('pong')

#@bot.command()
#async def test_notice(ctx):
#    # 現在の時刻
#    now = datetime.now().strftime('%H:%M')
#    print(now)
#    if (bot_logged == 1) and (client_logged == 1):
#        print('send')
#        channel = client.get_channel(channel_id)
#        await channel.send('演習おもらし注意報をお知らせしますっ！（テスト）')  
    
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    now_weekday = datetime.now().weekday()
    print(now)
    print(now_weekday)
    if client_logged == 1:
        # 時差は日本時間-9時間
        # 13:45->2:45
        # 17:45->8:45
        # 23:45->14:45
        if (now == '02:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('正午前の演習おもらし注意報をお知らせしますっ！')  
        elif (now == '08:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('18時前の演習おもらし注意報をお知らせしますっ！')  
        elif (now == '14:45') and (now_weekday == 5):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('24時前の演習おもらし注意報をお知らせしますっ！\n明日は日曜日なので、大講堂の更新も忘れずにっ！')  
        elif (now == '14:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('24時前の演習おもらし注意報をお知らせしますっ！')  
        elif (now == '15:45') and (now_weekday == 6):#日本時間の月曜0:00->世界標準時の日曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('日付が変わって月曜日になりました。\n大講堂で授業を受けさせましょうっ！')  

#ループ処理実行
loop.start()
    
#bot.run(token)
client.run(token)
