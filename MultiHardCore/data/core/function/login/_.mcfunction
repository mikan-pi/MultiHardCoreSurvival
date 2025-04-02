#最初のログイン
# メッセージの表示
tellraw @s [\
{"text": "Multi HardCore Survivalにようこそ", "color": "yellow"}, "\n",\
{"text": ">> 仕様 <<", "color":"green", "hover_event":{"action":"show_text", value:{text:"今回のサーバーでは画面下部に死亡数が表示されます。\nこの死亡数が一定数を超えることでゲームが終了します。\nまた終了後は、ワールドが自動生成されますのでしばらくお待ちください。"}}}\ 
]

execute at @s run playsound entity.player.levelup master @s ~ ~ ~ 2 0.8
#タイムのセット
scoreboard players set @s Players.Login.SumTime 21