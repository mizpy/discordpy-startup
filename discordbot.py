import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from discord.ext import tasks
import os
import traceback

JST = timezone(timedelta(hours=+9), 'JST')

#bot_logged = 0
client_logged = 0
prev_time = ''

#bot = commands.Bot(command_prefix='/')
client = discord.Client()

token = os.environ['DISCORD_BOT_TOKEN']
channel_id = int(os.environ['DISCORD_CHANNEL_ID'])

ment_begin_datetime_str = '2020/02/06 14:00'
ment_end_datetime_str = '2020/02/06 18:00'
ment_begin_datetime = datetime.strptime(ment_begin_datetime_str, '%Y/%m/%d %H:%M')
ment_end_datetime = datetime.strptime(ment_end_datetime_str, '%Y/%m/%d %H:%M')

#メンテナンス事前予告
ment_prev_msgs=[
    ['00:05', '@everyone\n**【メンテ】**次回のメンテナンスは' + ment_begin_datetime_str + '～' + ment_end_datetime_str + 'の予定です。'],
    ['12:05', '@everyone\n**【メンテ】**次回のメンテナンスは' + ment_begin_datetime_str + '～' + ment_end_datetime_str + 'の予定です。']
]

#曜日別メッセージリスト
mon_msgs=[
    ['00:00', '@everyone\n【講堂】『ぴんぽんぱんぽーん！アマゾン先生、アマゾン先生、講義の時間です。至急講堂までー。』\n…ZzZzZz……んんっ！？もう講義の時間っ！？指揮官に呼び出されるとか最悪ーっ！（アマゾン）\n:dolphin:月曜日は大講堂で駆逐艦に授業を受けさせましょう:dolphin:'],
    ['23:50', '@everyone\n【講堂】私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:']
]
tue_msgs=[
    ['00:00', '@everyone\n【講堂】ご主人、今日は夕張の授業の日だよ。頑張るからちゃんと見ててね！（夕張）\n:dolphin:火曜日は大講堂で巡洋艦に授業を受けさせましょう:dolphin:'],
    ['23:50', '@everyone\n【講堂】ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:巡洋艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:']
]
wed_msgs=[
    ['00:00', '@everyone\n【講堂】ペン姉さんの講義の時間だ、心して受けるがいい！指揮官、あとは私に任せておいて（ペンシルベニア）\n:dolphin:水曜日は大講堂で戦艦に授業を受けさせましょう:dolphin:']
]
thu_msgs=[
    ['00:00', '@everyone\n【講堂】指揮官、今日は私の授業の日ですわ。前回の宿題任務、ちゃんとやりましたか？（ラングレー）\n:dolphin:木曜日は大講堂で空母に授業を受けさせましょう:dolphin:']
]
fri_msgs=[
    ['00:00', '@everyone\n【講堂】『ぴんぽんぱんぽーん！アマゾン先生、アマゾン先生、講義の時間です。至急講堂までー。』\n…ZzZzZz……んんっ！？もう講義の時間っ！？指揮官に呼び出されるとか最悪ーっ！（アマゾン）\n:dolphin:金曜日は大講堂で駆逐艦に授業を受けさせましょう:dolphin:'],
    ['23:50', '@everyone\n【講堂】私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:']
]
sat_msgs=[
    ['00:00', '@everyone\n【講堂】ご主人、今日は夕張の授業の日だよ。頑張るからちゃんと見ててね！（夕張）\n:dolphin:土曜日は大講堂で巡洋艦に授業を受けさせましょう:dolphin:'],
    ['23:50', '@everyone\n【講堂】ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:日曜日は授業がお休みです。今のうちに授業を受け直しましょう:dolphin:']
]
sun_msgs=[
    ['23:50', '@everyone\n【講堂】そろそろ日付が変わりますね！私も授業受けたいな……あ、それよりもアマゾンさん、ちゃんと起きてるかな…？（谷風）\n:dolphin:月曜日になったら大講堂で駆逐艦に授業を受けさせましょう:dolphin:']
]

#曜日メッセージリスト
weekly_msgs=[mon_msgs, tue_msgs, wed_msgs, thu_msgs, fri_msgs, sat_msgs, sun_msgs]

#毎日メッセージリスト
dayly_msgs=[
    ['11:45', '@everyone\n【演習】正午前の演習おもらし注意報をお知らせしますっ！'],
    ['17:45', '@everyone\n【演習】18時前の演習おもらし注意報をお知らせしますっ！'],
    ['23:45', '@everyone\n【演習】深夜0時前の演習おもらし注意報をお知らせしますっ！']
]



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
    
# 5秒に一回ループ
@tasks.loop(seconds=5)
async def loop():
    # 現在の時刻
    global prev_time
    now_datetime = datetime.now(JST)
    now_date = now_datetime.strftime('%Y/%m/%d')
    now_time = now_datetime.strftime('%H:%M')
    now_weekday = now_datetime.weekday()
    
    if (prev_time != now_time) and (client_logged == 1):
        prev_time = now_time
        print(now_date, now_weekday, now_time)
        
        #----メンテメッセージ----
#        global ment_begin_datetime
#        global ment_end_datetime
#        if ((ment_begin_datetime - now_datetime) > datetime.timedelta()):
#            ment_begin_date = ment_begin_datetime.strftime('%Y/%m/%d')
#            ment_begin_time = ment_begin_datetime.strftime('%H:%M')
#            ment_end_date = ment_end_datetime.strftime('%Y/%m/%d')
#            ment_end_time = ment_end_datetime.strftime('%H:%M')
            
#            if (ment_begin_date.timedelta > now_date.timedelta):
#                for ment_prev_msg in ment_prev_msgs:
#                    print(' >ment prev check:', ment_prev_msg[0])
#                    if(ment_prev_msg[0] == now_time):
#                        print(' >>SEND:', ment_prev_msg[1])
#                        channel = client.get_channel(channel_id)
#                        await channel.send(ment_prev_msg[1])
#            else:
#            print(' >ment_begin_datetime_str:', ment_begin_datetime_str)
#            print(' >ment_end_datetime_str:', ment_end_datetime_str)
#            print(' >ment_begin_datetime:', ment_begin_datetime)
#            print(' >ment_end_datetime:', ment_end_datetime)
        for ment_prev_msg in ment_prev_msgs:
            print(' >ment today check:', ment_prev_msg[0], ment_prev_msg[1])
            if(ment_prev_msg[0] == now_time):
                print(' >>SEND:', ment_prev_msg[1])
                channel = client.get_channel(channel_id)
                await channel.send(ment_prev_msg[1])
        
        #----毎日メッセージ----
        for dayly_msg in dayly_msgs:
            print(' >dayly check:', dayly_msg[0])
            if(dayly_msg[0] == now_time):
                print(' >>SEND:', dayly_msg[1])
                channel = client.get_channel(channel_id)
                await channel.send(dayly_msg[1])
        
        #----曜日メッセージ----
        for weekly_msg in weekly_msgs[now_weekday]:
            print(' >weekly check:', now_weekday, weekly_msg[0])
            if(weekly_msg[0] == now_time):
                print(' >>SEND:', weekly_msg[1])
                channel = client.get_channel(channel_id)
                await channel.send(weekly_msg[1])

        
        
        #----演習系の設定----
#        if (now_time == '02:45'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【演習】**正午前の演習おもらし注意報をお知らせしますっ！')  
#        elif (now_time == '08:45'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【演習】**18時前の演習おもらし注意報をお知らせしますっ！')  
#        elif (now_time == '14:45'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【演習】**深夜0時前の演習おもらし注意報をお知らせしますっ！')  
        #----メンテ系の設定----
#        elif (now_time == '3:05'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**次回のメンテナンスは2/6（木）14:00～18:00の予定です。')
#        elif (now_time == '15:05'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**次回のメンテナンスは2/6（木）14:00～18:00の予定です。')
#        elif (now_time == '15:05'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**本日14:00からメンテナンスです。\nメンテナンス時間は14:00-18:00となっています。')  
#        elif (now_time == '00:00'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**本日14:00からメンテナンスです。\nメンテナンス時間は14:00-18:00となっています。')  
#        elif (now_time == '03:00'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**本日14:00からメンテナンスです。\nメンテナンス時間は14:00-18:00となっています。\n演習のおもらしなどにご注意くださいっ！')  
#        elif (now_time == '04:30'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**本日14:00からメンテナンスです。\nメンテナンス時間は14:00-18:00となっています。\n演習のおもらしなどにご注意くださいっ！')  
#        elif (now_time == '04:45'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【演習】**メンテ前の演習おもらし注意報をお知らせしますっ！')  
#        elif (now_time == '05:00'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**メンテナンスが開始されましたっ！（たぶん）\nメンテナンス時間は14:00-18:00となっています。')  
#        elif (now_time == '09:00'):
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【メンテ】**メンテナンス終了時間ですっ！\n時間通りに終わってるかな…？')  
      #----講堂系の設定----
#        elif (now_time == '14:50') and (now_weekday == 6):#日本時間の月曜0:00->世界標準時の日曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**そろそろ日付が変わりますね！私も授業受けたいな……あ、それよりもアマゾンさん、ちゃんと起きてるかな…？（谷風）\n:dolphin:月曜日になったら大講堂で駆逐艦に授業を受けさせましょう:dolphin:') 
#        elif (now_time == '14:50') and (now_weekday == 0):#日本時間の火曜0:00->世界標準時の月曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
#        elif (now_time == '14:50') and (now_weekday == 1):#日本時間の水曜0:00->世界標準時の火曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:巡洋艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
#        elif (now_time == '14:50') and (now_weekday == 4):#日本時間の金曜0:00->世界標準時の木曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**私の授業時間ももうすぐ終わり！…え？残業！？仕方ないわね…やってやるか…（アマゾン）\n:dolphin:駆逐艦にもっと授業を受けさせたい場合は今のうちに受け直しましょう:dolphin:') 
#        elif (now_time == '14:50') and (now_weekday == 5):#日本時間の土曜0:00->世界標準時の金曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**ご主人は巡洋艦の授業に満足してる？ふふふ、夕張はまだまだ授業したいぞ～（夕張）\n:dolphin:日曜日は授業がお休みです。今のうちに授業を受け直しましょう:dolphin:') 
      #----講堂系の設定----
#        elif (now_time == '15:00') and (now_weekday == 6):#日本時間の月曜0:00->世界標準時の日曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**『ぴんぽんぱんぽーん！アマゾン先生、アマゾン先生、講義の時間です。至急講堂までー。』\n…ZzZzZz……んんっ！？もう講義の時間っ！？指揮官に呼び出されるとか最悪ーっ！（アマゾン）\n:dolphin:月曜日は大講堂で駆逐艦に授業を受けさせましょう:dolphin:') 
#        elif (now_time == '15:00') and (now_weekday == 0):#日本時間の火曜0:00->世界標準時の月曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**ご主人、今日は夕張の授業の日だよ。頑張るからちゃんと見ててね！（夕張）\n:dolphin:火曜日は大講堂で巡洋艦に授業を受けさせましょう:dolphin:')
#        elif (now_time == '15:00') and (now_weekday == 1):#日本時間の水曜0:00->世界標準時の火曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**ペン姉さんの講義の時間だ、心して受けるがいい！指揮官、あとは私に任せておいて（ペンシルベニア）\n:dolphin:水曜日は大講堂で戦艦に授業を受けさせましょう:dolphin:')
#        elif (now_time == '15:00') and (now_weekday == 2):#日本時間の木曜0:00->世界標準時の水曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**指揮官、今日は私の授業の日ですわ。前回の宿題任務、ちゃんとやりましたか？（ラングレー）\n:dolphin:木曜日は大講堂で空母に授業を受けさせましょう:dolphin:') 
#        elif (now_time == '15:00') and (now_weekday == 3):#日本時間の金曜0:00->世界標準時の木曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**『ぴんぽんぱんぽーん！アマゾン先生、アマゾン先生、講義の時間です。至急講堂までー。』\n…ZzZzZz……んんっ！？もう講義の時間っ！？指揮官に呼び出されるとか最悪ーっ！（アマゾン）\n:dolphin:金曜日は大講堂で駆逐艦に授業を受けさせましょう:dolphin:') 
#        elif (now_time == '15:00') and (now_weekday == 4):#日本時間の土曜0:00->世界標準時の金曜15:00
#            print('send')
#            channel = client.get_channel(channel_id)
#            await channel.send('@everyone\n**【講堂】**ご主人、今日は夕張の授業の日だよ。頑張るからちゃんと見ててね！（夕張）\n:dolphin:土曜日は大講堂で巡洋艦に授業を受けさせましょう:dolphin:') 
            
#ループ処理実行
loop.start()
    
#bot.run(token)
client.run(token)
