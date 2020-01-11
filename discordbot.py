#coding:UTF-8
import discord
from datetime import datetime
from discord.ext import tasks

logged = 0

TOKEN = "NjY1NTg0MTYzMjQzNjg3OTU2.XhohOQ.gg9rtHy-mkFPO1k5fcQszWwEyQQ" #トークン
CHANNEL_ID = 665527939160473622 #チャンネルID
# 接続に必要なオブジェクトを生成
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global logged
    logged = 1
    print(logged)
    
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    print(now)
    print(logged)
    #if now == '02:21':
    if logged == 1:
        print('send')
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('テスト投稿です！')  

#ループ処理実行
loop.start()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
