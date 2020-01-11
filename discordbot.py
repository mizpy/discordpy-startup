import discord
from discord.ext import commands
from datetime import datetime
from discord.ext import tasks
import os
import traceback

#bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
channel_id = os.environ['DISCORD_CHANNEL_ID']

#@bot.event
#async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)

#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    print(now)
#    if (now == '10:46') or (now == '11:46') or (now == '12:46') or (now == '13:46'):
        channel = client.get_channel(channel_id)
        await channel.send('テスト投稿です！')  

#ループ処理実行
loop.start()

#bot.run(token)
client.run(token)
