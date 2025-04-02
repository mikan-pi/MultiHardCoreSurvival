
#最初のログイン
execute as @a unless score @s Players.Login.SumTime matches 20.. run function core:login/_

scoreboard players add $tick TimeCount 1

# 死亡数の集計
execute as @a if score @s DeathCount matches 1.. run function core:death/count

# 現在の死亡数を表示
title @a actionbar [{"text": "現在の死亡数："}, {"score": {"name": "$sum", objective: "DeathCount"}},{"text":"/"},{"score":{"name": "$threshold", objective: "DeathCount"}}]
