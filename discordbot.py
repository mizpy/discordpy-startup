import discord
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
import os
import traceback

#bot_logged = 0
client_logged = 0
prev_now = ''

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
    
# 20秒に一回ループ
@tasks.loop(seconds=20)
async def loop():
    # 現在の時刻
    global prev_now
    now = datetime.now().strftime('%H:%M')
    now_weekday = datetime.now().weekday()
    if (prev_now != now) and (client_logged == 1):
        prev_now = now
        print(now)
        print(now_weekday)
        # 時差は日本時間-9時間
        # 13:45->2:45
        # 17:45->8:45
        # 23:45->14:45
        #----演習系の設定----
        if (now == '02:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【演習】**正午前の演習おもらし注意報をお知らせしますっ！')  
        elif (now == '08:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【演習】**18時前の演習おもらし注意報をお知らせしますっ！')  
        elif (now == '14:45'):
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【演習】**深夜0時前の演習おもらし注意報をお知らせしますっ！')  
        #----講堂系の設定----
        elif (now == '14:50') and (now_weekday == 6):#日本時間の月曜0:00->世界標準時の日曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【講堂】**もうすぐ私の授業の時間よ！ちゃんと私に駆逐艦を預けてから寝なさい！（アマゾン）\n:dolphin:月曜日になったら大講堂で駆逐艦に授業を受けさせましょう:dolphin:') 
        elif (now == '14:50') and (now_weekday == 0):#日本時間の火曜0:00->世界標準時の月曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【講堂】**私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
        elif (now == '14:50') and (now_weekday == 1):#日本時間の水曜0:00->世界標準時の火曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【講堂】**ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:巡洋艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
        elif (now == '14:50') and (now_weekday == 3):#日本時間の金曜0:00->世界標準時の木曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【講堂】**私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
        elif (now == '14:50') and (now_weekday == 4):#日本時間の土曜0:00->世界標準時の金曜15:00
            print('send')
            channel = client.get_channel(channel_id)
            await channel.send('@everyone\n**【講堂】**ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:日曜日は授業がお休みです。今のうちに授業を受け直しましょう:dolphin:') 

#ループ処理実行
loop.start()
    
#bot.run(token)
client.run(token)
