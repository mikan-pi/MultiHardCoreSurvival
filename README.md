# Multi HardCore Survival Tool

このリポジトリはマルチハードコアサバイバル用のツールです

## 仕様

Minecraft Version : 1.21.5

Python Version : 1.12.x

このリポジトリでは現在設定されている死亡可能回数を超えると、ワールドの再生成を行います。

## Use it

### 構造

 - multi_hard_core
   - このディレクトリは[ServerBot](https://github.com/sleeping-mikan/server-bot-v2)の拡張機能です 該当リポジトリを参照して、環境構築を行ってください
 - MultiHardCore
   - このディレクトリはMinecraft1.21.5用のデータパックです 通常のデータパック導入に乗っ取って導入してください
 - multihardcore
   - このディレクトリはMinecraft1.21.5用のリソースパックです 通常のリソースパックのように導入するか、サーバーリソースパックとして導入してください

### 設定

MultiHardCoreにはいくつかの設定が存在します。

 - 死亡可能回数
   - discordで/extension-multi_hard_core set-thresholdコマンドを用いて設定してください
 - リザルトチャンネル
   - mylti_hard_coreを実行した後一度終了をし、サーバーを実行していない状況でdiscord.send_channelにチャンネルidを設定してください