#最初のログイン
# メッセージの表示
tellraw @s [\
{"text": "Multi HardCore Survivalにようこそ", "color": "yellow"}, "\n",\
{"text": "===========================================", color:"gold"}, "\n",\
{"text": ">> 仕様 <<", "color":"red", "hover_event":{"action":"show_text", value:{text:"今回のサーバーでは画面下部に死亡数が表示されます。\nこの死亡数が一定数を超えることでゲームが終了します。\nまた終了後は、ワールドが自動生成されますのでしばらくお待ちください。"}}}, "\n",\ 
{"text": ">> 注意 <<", "color":"red", "hover_event":{"action":"show_text", value:{text:"当サーバーではチートまたはチートとみなされる行為を許可していません。\n該当の行為を行った場合には、サーバーからのBANまたは、DiscordからのBANを行います。\nまたチートの判断は当サーバーが行うことから、Multi HardCore Survivalにおいてmodの利用は推奨されません。"}}}\
]

execute at @s run playsound entity.player.levelup master @s ~ ~ ~ 2 0.8
#タイムのセット
scoreboard players set @s Players.Login.SumTime 21