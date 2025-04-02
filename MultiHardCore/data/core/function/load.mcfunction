# 死亡数カウント用
scoreboard objectives add DeathCount deathCount {"text":"死亡数","color":"red"}
scoreboard players set $sum DeathCount 0

# 時間カウント用
scoreboard objectives add TimeCount dummy {"text":"時間","color":"yellow"}


gamerule sendCommandFeedback false
gamerule doImmediateRespawn true

scoreboard objectives add Players.Login.SumTime dummy {"text":"ログイン時間","color":"yellow"}