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

ment_begin_datetime_str = os.environ['MENTE_BEGIN_PARAM']
ment_end_datetime_str = os.environ['MENTE_END_PARAM']
ment_begin_datetime = datetime.strptime(ment_begin_datetime_str, '%Y/%m/%d %H:%M')
ment_end_datetime = datetime.strptime(ment_end_datetime_str, '%Y/%m/%d %H:%M')

ment_begin_prev_15min_datetime = ment_begin_datetime - timedelta(minutes=15)
ment_begin_prev_30min_datetime = ment_begin_datetime - timedelta(minutes=30)
ment_begin_prev_60min_datetime = ment_begin_datetime - timedelta(minutes=60)
ment_begin_prev_120min_datetime = ment_begin_datetime - timedelta(minutes=120)
ment_begin_prev_240min_datetime = ment_begin_datetime - timedelta(minutes=240)

ment_begin_time = ment_begin_datetime.strftime('%H:%M')
ment_end_time = ment_end_datetime.strftime('%H:%M')

#メンテナンス事前予告
ment_prev_msgs=[
    ['00:05', '@everyone\n【メンテ】次回のメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。'],
    ['12:05', '@everyone\n【メンテ】次回のメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。']
]

#メンテナンス当日予告
ment_today_msgs=[
    ['00:05', '@everyone\n【メンテ】本日はメンテナンス日です。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。'],
    ['06:05', '@everyone\n【メンテ】本日はメンテナンス日です。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。'],
    ['12:05', '@everyone\n【メンテ】本日はメンテナンス日です。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。']
]

#メンテナンス直前予告
ment_soon_msgs=[
    [ment_begin_prev_240min_datetime.strftime('%Y/%m/%d'), ment_begin_prev_240min_datetime.strftime('%H:%M'), '@everyone\n【メンテ】4時間後の' + ment_begin_time + 'からメンテナンスです。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。'],
    [ment_begin_prev_120min_datetime.strftime('%Y/%m/%d'), ment_begin_prev_120min_datetime.strftime('%H:%M'), '@everyone\n【メンテ】2時間後の' + ment_begin_time + 'からメンテナンスです。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。'],
    [ment_begin_prev_60min_datetime.strftime('%Y/%m/%d'), ment_begin_prev_60min_datetime.strftime('%H:%M'), '@everyone\n【メンテ】1時間後の' + ment_begin_time + 'からメンテナンスです。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。\n演習のおもらしなどにご注意くださいっ！'],
    [ment_begin_prev_30min_datetime.strftime('%Y/%m/%d'), ment_begin_prev_30min_datetime.strftime('%H:%M'), '@everyone\n【メンテ】30分後の' + ment_begin_time + 'からメンテナンスです。\nメンテナンスは ' + ment_begin_datetime_str + ' ～ ' + ment_end_datetime_str + ' の予定です。\n演習のおもらしなどにご注意くださいっ！'],
    [ment_begin_prev_15min_datetime.strftime('%Y/%m/%d'), ment_begin_prev_15min_datetime.strftime('%H:%M'), '@everyone\n【演習】メンテ前の演習おもらし注意報をお知らせしますっ！'],
    [ment_begin_datetime.strftime('%Y/%m/%d'), ment_begin_datetime.strftime('%H:%M'), '@everyone\n【メンテ】メンテナンスが開始されましたっ！（たぶん）\nメンテナンスは ' + ment_end_datetime_str + ' までの予定です。'],
    [ment_end_datetime.strftime('%Y/%m/%d'), ment_end_datetime.strftime('%H:%M'), '@everyone\n【メンテ】メンテナンス終了時間ですっ！\n時間通りに終わってるかな…？']
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
    ['23:45', '@everyone\n【演習】深夜0時前の演習おもらし注意報をお知らせしますっ！'],
    ['06:00', '@everyone\n【離島支援作戦】6時になりました。追加の部隊派遣をお願いしますっ！'],
    ['12:00', '@everyone\n【離島支援作戦】正午になりました。追加の部隊派遣をお願いしますっ！'],
    ['18:00', '@everyone\n【離島支援作戦】18時になりました。追加の部隊派遣をお願いしますっ！'],
    ['21:00', '@everyone\n【離島支援作戦】21時になりました。追加の部隊派遣をお願いしますっ！']
]

#生放送メッセージリスト
third_anniv_msgs=[
    ['00:05', '@everyone\n【３周年記念２５時間生放送】00:10〜01:15 アズレン格付け検定 https://youtu.be/a6Zuu6m80W4'],
    ['01:25', '@everyone\n【３周年記念２５時間生放送】01:30～03:30 大人のアズレン https://youtu.be/a6Zuu6m80W4'],
    ['03:40', '@everyone\n【３周年記念２５時間生放送】03:45～04:45 アズレン×ホロライブ ～白上あくあマリン～ https://youtu.be/a6Zuu6m80W4'],
    ['04:55', '@everyone\n【３周年記念２５時間生放送】05:00～05:50 指揮官の声を聴かせて https://youtu.be/a6Zuu6m80W4'],
    ['05:55', '@everyone\n【３周年記念２５時間生放送】06:00～06:30 朝アズNEWS https://youtu.be/ac5_qCF6AVg'],
    ['06:35', '@everyone\n【３周年記念２５時間生放送】06:40～07:30 挑戦！リアル饅頭クイズバトル！ https://youtu.be/ac5_qCF6AVg'],
    ['07:40', '@everyone\n【３周年記念２５時間生放送】07:45～08:45 若手超人にクローズアップ！ https://youtu.be/ac5_qCF6AVg'],
    ['09:00', '@everyone\n【３周年記念２５時間生放送】09:05～10:35 激突！ガチンコ艦船バトル https://youtu.be/ac5_qCF6AVg'],
    ['10:50', '@everyone\n【３周年記念２５時間生放送】10:55～11:55 アズールレーンクロスウェーブ コラボスペシャル https://youtu.be/ac5_qCF6AVg'],
    ['12:10', '@everyone\n【３周年記念２５時間生放送】12:15～13:15 三笠大先輩と学ぶ世界の艦船 出張版 https://youtu.be/AmYrelLerzU'],
    ['13:30', '@everyone\n【３周年記念２５時間生放送】13:35〜14:35 アズレンステーション 最終回SP https://youtu.be/AmYrelLerzU'],
    ['14:55', '@everyone\n【３周年記念２５時間生放送】15:00～16:00 びそくぜんしんっ！ アニメ制作秘話 https://youtu.be/AmYrelLerzU'],
    ['16:15', '@everyone\n【３周年記念２５時間生放送】16:20～17:50 アズトーーク https://youtu.be/AmYrelLerzU'],
    ['17:55', '@everyone\n【３周年記念２５時間生放送】18:00〜19:00 親ばかトーク炸裂 ～うちの娘（フィギュア）が一番かわいい！～ https://youtu.be/AmYrelLerzU'],
    ['19:05', '@everyone\n【３周年記念２５時間生放送】19:10〜20:10 祝３周年！アズレン公式生放送 第二夜 ～まだまだあります最新情報～ https://youtu.be/AmYrelLerzU'],
    ['20:10', '@everyone\n【３周年記念２５時間生放送】20:15～21:00 グランドフィナーレ https://youtu.be/AmYrelLerzU'],
]

#1日限定告知
one_day_only_msgs=[
    ['00:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['01:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['02:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['03:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['04:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['05:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['06:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['07:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['08:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['09:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['10:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['11:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['12:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['13:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['14:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['15:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['16:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['17:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['18:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['19:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['20:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['21:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['22:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['23:00', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
    ['23:45', '@everyone\n【アンケートにご協力ください】兵站に関するアンケートです。（締切：12/23 23:59） https://discord.com/channels/665512195919970305/665512196436000771/791174907249164298'],
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

        #----生放送メッセージ----
        if((now_datetime.date() == datetime.strptime('2020/09/13','%Y/%m/%d').date())):
            print(' >third_anniv_msg check:')
            for third_anniv_msg in third_anniv_msgs:
                print(' >third_anniv check:', third_anniv_msg[0], third_anniv_msg[1])
                if(third_anniv_msg[0] == now_time):
                    print(' >>SEND:', third_anniv_msg[1])
                    channel = client.get_channel(channel_id)
                    await channel.send(third_anniv_msg[1])
                    
        #----1日限定告知----
        if((now_datetime.date() == datetime.strptime('2020/12/23','%Y/%m/%d').date())):
            print(' >one_day_only_msgs check:')
            for one_day_only_msg in one_day_only_msgs:
                print(' >one_day_only check:', one_day_only_msg[0])
                if(one_day_only_msg[0] == now_time):
                    print(' >>SEND:', one_day_only_msg[1])
                    channel = client.get_channel(channel_id)
                    await channel.send(one_day_only_msg[1])

        #----メンテ直前メッセージ----
        for ment_soon_msg in ment_soon_msgs:
            print(' >ment soon check:', ment_soon_msg[0], ment_soon_msg[1])
            if(ment_soon_msg[0] == now_date) and (ment_soon_msg[1] == now_time):
                print(' >>SEND:', ment_soon_msg[2])
                channel = client.get_channel(channel_id)
                await channel.send(ment_soon_msg[2])

        #----メンテ事前メッセージ----
        if(ment_begin_datetime.date() > now_datetime.date()):
            for ment_prev_msg in ment_prev_msgs:
                print(' >ment prev check:', ment_prev_msg[0], ment_prev_msg[1])
                if(ment_prev_msg[0] == now_time):
                    print(' >>SEND:', ment_prev_msg[1])
                    channel = client.get_channel(channel_id)
                    await channel.send(ment_prev_msg[1])
                    
        #----メンテ当日メッセージ----
        elif((ment_begin_datetime.date() == now_datetime.date()) and (now_datetime.date() == ment_begin_prev_240min_datetime.date())):
            if(now_datetime.time() < ment_begin_prev_240min_datetime.time()):
                for ment_today_msg in ment_today_msgs:
                    print(' >ment today check:', ment_today_msg[0], ment_today_msg[1])
                    if(ment_today_msg[0] == now_time):
                        print(' >>SEND:', ment_today_msg[1])
                        channel = client.get_channel(channel_id)
                        await channel.send(ment_today_msg[1])
                            
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

#ループ処理実行
loop.start()
    
#bot.run(token)
client.run(token)
