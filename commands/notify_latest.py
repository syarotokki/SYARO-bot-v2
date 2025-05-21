import discord
from discord import app_commands
from discord.ext import commands
from utils.youtube import fetch_latest_video

class NotifyLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_latest", description="最新のYouTube動画を通知します")
    async def notify_latest(self, interaction: discord.Interaction):
        # 特定のユーザーだけが使えるように制限
        if interaction.user.id != 1105948117624434728:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=False, thinking=True)

        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        if str(interaction.guild_id) not in config:
            await interaction.followup.send("このサーバーはまだ `/subscribe` で登録されていません。")
            return

        youtube_channel_id = config[str(interaction.guild_id)]["youtube_channel_id"]
        notify_channel_id = config[str(interaction.guild_id)]["notify_channel_id"]

        latest_video = fetch_latest_video(youtube_channel_id)
        if not latest_video:
            await interaction.followup.send("最新動画の取得に失敗しました。")
            return

        channel = self.bot.get_channel(int(notify_channel_id))
        if not channel:
            await interaction.followup.send("通知先チャンネルが見つかりません。")
            return

        if latest_video["is_live"]:
            message = f"🔴 **ライブ配信が始まりました！**\n**{latest_video['title']}**\n{latest_video['url']}\n開始時刻: <t:{latest_video['published_at_ts']}:F>"
        else:
            message = f"🆕 **新しい動画が投稿されました！**\n**{latest_video['title']}**\n{latest_video['url']}"

        await channel.send(message)
        await interaction.followup.send("最新動画を通知しました！")

async def setup(bot):
    await bot.add_cog(NotifyLatest(bot))

