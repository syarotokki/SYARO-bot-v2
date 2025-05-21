import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from utils import fetch_latest_video

CONFIG_FILE = "config.json"

class NotifyLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_latest", description="最新のYouTube動画を通知します（手動）")
    async def notify_latest(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = str(interaction.guild_id)

        # config.json 読み込み
        if not os.path.exists(CONFIG_FILE):
            await interaction.followup.send("⚠ 設定ファイルが見つかりません。先に /subscribe を実行してください。", ephemeral=True)
            return

        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        if guild_id not in config:
            await interaction.followup.send("⚠ このサーバーにはまだ通知設定がありません。/subscribe で登録してください。", ephemeral=True)
            return

        channel_id = int(config[guild_id]["channel_id"])
        youtube_channel_id = config[guild_id]["youtube_channel_id"]

        video = fetch_latest_video(youtube_channel_id)
        if not video:
            await interaction.followup.send("⚠ 最新動画の取得に失敗しました。", ephemeral=True)
            return

        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(f"📺 新しい動画が投稿されました！\n{video['title']}\n{video['url']}")
            await interaction.followup.send("✅ 通知を送信しました。", ephemeral=True)
        else:
            await interaction.followup.send("⚠ 通知先チャンネルが見つかりません。", ephemeral=True)
