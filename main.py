import discord
from discord.ext import commands
import os
import json
import asyncio

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# スラッシュコマンド用に拡張
from discord import app_commands
tree = bot.tree

# 起動時にすべてのコマンドを読み込む
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Cog読み込み
async def load():
    await bot.wait_until_ready()
    await bot.add_cog(Subscribe(bot))
    await bot.add_cog(NotifyLatest(bot))
    await bot.add_cog(NotifyPast(bot))

# 各コマンドのインポート
from commands.subscribe import Subscribe
from commands.notify_latest import NotifyLatest
from commands.notify_past import NotifyPast

bot.loop.create_task(load())

# Botトークン（環境変数）
bot.run(os.environ["DISCORD_TOKEN"])
