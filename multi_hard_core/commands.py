import discord
import re
from datetime import datetime
import asyncio
import os
import shutil

# メインに存在するコマンド群をimport(import from __main__ if want to add discord commands) 
from __main__ import extension_commands_group as tree
# もし、管理しているサーバープロセスに対して操作をしたいならget_process functionをimport(import get_process function from __main__ if want to control server process)
from __main__ import get_process
# もし、ログを出力したいならloggerをimport(logger is imported from __main__ if want to print log)
from __main__ import extension_logger
# サーバーのディレクトリ/サーバーの名前/botのディレクトリ/botの名前をimport(import from __main__ if want to get server directory/server name/bot directory)
from __main__ import server_path,server_name,now_path,now_file
# 起動時間をimport(import from __main__ if want to get start time)
from __main__ import time
# 直近のログを取得(get recent log)
from __main__ import get_log
# 各コマンドで権限データをセット/確認したい場合
from __main__ import COMMAND_PERMISSION
# logger補助関数 await print_user(logger,user: discord.user) で利用者のログを残す
from __main__ import print_user

from __main__ import append_tasks_func, write_server_in, get_log, core_stop,is_running_server, core_start,client

from discord.ext import tasks

threshold = 1
send_channel = None
import json

from .utils import nbt

start_time = time

extension_logger.info("base: " + os.path.dirname(__file__))

# ファイルが既にある場合そのthresholdを読み込む
if os.path.exists(os.path.join(os.path.dirname(__file__),"data.json")):
    with open(os.path.join(os.path.dirname(__file__),"data.json"), "r") as f:
        j = json.load(f)
        threshold = j["threshold"]
        send_channel = j["discord"]["send_channel"]
else:
    with open(os.path.join(os.path.dirname(__file__),"data.json"), "w") as f:
        json.dump({
            "threshold":threshold,
            "discord":{
                "send_channel": None
            }
        },f)

@tree.command(name="set-threshold", description="許容する死亡回数を設定します")
async def set_threshold(interaction: discord.Interaction, newthreshold: int):
    global threshold
    threshold = newthreshold
    await interaction.response.send_message(f"許容する死亡回数を{threshold}に設定しました")

    with open(os.path.join(os.path.dirname(__file__),"data.json"), "w") as f:
        json.dump({"threshold":threshold, "discord":{"send_channel": send_channel}},f)

def get_timestamp(day: str, time_str: str) -> int:
    """ 'YYYY-MM-DD' と 'HH:MM:SS' 形式の文字列を UNIX タイムスタンプに変換 """
    dt = datetime.strptime(f"{day} {time_str}", "%Y-%m-%d %H:%M:%S")  # 修正: datetime.strptime を正しく使用
    return int(dt.timestamp())


def properties_to_dict(filename):
    properties = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith(' ') or line.startswith('\t'):
                    line = line[1:]
                key, value = line.split('=', 1)
                properties[key] = value
    return properties
# server.propertiesからlevel-nameを読み込む
file = properties_to_dict(os.path.join(server_path,"server.properties"))
level_name = file["level-name"]
def seed():
    d_nbt = nbt(file_path=os.path.join(server_path,level_name,"level.dat")).to_dict()
    try:
        seed = d_nbt[""]["Data"]["WorldGenSettings"]["seed"]
    except:
        seed = d_nbt[""]["Data"]["RandomSeed"]
    extension_logger.info("seed : " + str(seed))
    return seed

async def send_discord():
    try:
        global time
        extension_logger.info("send result chnanel : " + str(send_channel))
        if send_channel is None:
            return
        channel = client.get_channel(send_channel)
        extension_logger.info("send result chnanel : " + str(channel))
        if channel is None:
            return
        old_timestamp = datetime.strptime(time, "%Y-%m-%d_%H_%M_%S").timestamp()
        new_timestamp = datetime.now().timestamp()
        time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        embed = discord.Embed(title="Multi HardCore Survival", description="ending server", color=discord.Color.red())
        embed.add_field(name="今回の記録", value="経過時間：{:.2f}秒\nseed：".format(new_timestamp - old_timestamp)+str(seed()), inline=False)  # 修正: new_timestamp - old_timestamp を使用
        await channel.send(embed=embed)
    except Exception as e:
        extension_logger.error(e)

def get_time(log: list):
    return log[0][9:], log[1][:-4]

last_death_timestamp = 0
start_time = datetime.now().timestamp()

@tasks.loop(seconds=10)
async def loop():
    global last_death_timestamp
    try:
        result, reason = write_server_in(f"execute run scoreboard players set $threshold DeathCount {threshold}")
        if not result:
            return
        await asyncio.sleep(0.5)
        result, reason = write_server_in("scoreboard players get $sum DeathCount")
        if not result:
            return
        await asyncio.sleep(0.5)
        logs = get_log().copy()
        for log in logs:
            # 空白の数を圧縮
            log = re.sub(r"\s+", " ", log)
            log = log.split(" ")
            timestamp = get_timestamp(*get_time(log))
            if timestamp < last_death_timestamp:
                continue
            last_death_timestamp = timestamp
            # 要素を入れる
            element = log[4:]
            if log[-1].startswith("[死亡数]") and log[-4] == "$sum":   
                extension_logger.info(f"scoreboard got -> {log[-2]}") 
                if int(element[-2]) >= threshold:
                    await send_discord()
                    await restart_server()
    except Exception as e:
        extension_logger.error(e)

async def restart_server():
    global last_death_timestamp, start_time
    core_stop()
    while True:
        if is_running_server(extension_logger):
            await asyncio.sleep(1)
        else:
            # サーバーが起動していない場合の次に進む
            break
    # データを削除
    for target_path in os.listdir(os.path.join(server_path,"world")):
        if target_path.endswith("datapacks"): continue
        target_path = os.path.join(server_path,"world",target_path)
        extension_logger.info(f"delete {target_path}")
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        elif os.path.isfile(target_path):  # ファイルなら `del` を使う
            os.remove(target_path)
    # 2分経過していなければ、2分までの秒数を出力
    if get_timestamp(*get_time(get_log()[-1].split(" "))) - start_time < 120:
        extension_logger.info(f"restart server in {120 - (get_timestamp(*get_time(get_log()[-1].split(' '))) - start_time)} seconds")
        await asyncio.sleep(120 - (get_timestamp(*get_time(get_log()[-1].split(' '))) - start_time))
    else:
        extension_logger.info(f"restart server")
        
    # ここまでのログを無効に
    last_death_timestamp = get_timestamp(*get_time(get_log()[-1].split(" ")))
    start_time = last_death_timestamp
    # 再起動
    core_start()




append_tasks_func(loop)