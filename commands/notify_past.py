import discord
from discord import app_commands
from discord.ext import commands
import json
from utils.youtube import get_past_videos
import os

DEVELOPER_ID = 1105948117624434728  # あなたのDiscordユーザーID

class NotifyPast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_past", description="過去の動画をすべて通知します（開発者専用）")
    async def notify_past(self, interaction: discord.Interaction):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("このコマンドは開発者専用です。", ephemeral=True)
            return

        await interaction.response.defer()
        
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            await interaction.followup.send("config.json が見つかりません。")
            return

        guild_id = str(interaction.guild.id)
        if guild_id not in config:
            await interaction.followup.send("このサーバーは /subscribe で登録されていません。")
            return

        channel_id = config[guild_id]["notification_channel_id"]
        youtube_channel_id = config[guild_id]["youtube_channel_id"]

        videos = get_past_videos(youtube_channel_id)
        if not videos:
            await interaction.followup.send("過去の動画が見つかりませんでした。")
            return

        videos.reverse()  # ← 最新の動画が後に通知されるように反転

        notify_channel = self.bot.get_channel(int(channel_id))
        if not notify_channel:
            await interaction.followup.send("通知チャンネルが見つかりません。")
            return

        for video in videos:
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            is_live = video["snippet"]["liveBroadcastContent"] == "live"
            if is_live:
                start_time = video["snippet"].get("publishedAt", "不明な時間")
                message = f"🔴 ライブ配信が始まりました：**{title}**\n開始時刻：{start_time}\n{url}"
            else:
                message = f"📺 新しい動画が公開されました：**{title}**\n{url}"

            await notify_channel.send(message)

        await interaction.followup.send("過去の動画を通知しました。")
