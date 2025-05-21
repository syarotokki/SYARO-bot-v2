import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_FILE = "config.json"

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subscribe", description="YouTubeチャンネルの通知先を登録します")
    @app_commands.describe(channel="通知を送信するDiscordチャンネル", youtube_channel_id="YouTubeのチャンネルID")
    async def subscribe(self, interaction: discord.Interaction, channel: discord.TextChannel, youtube_channel_id: str):
        await interaction.response.defer(ephemeral=True)

        guild_id = str(interaction.guild_id)

        # config.json 読み込み
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            config = {}

        config[guild_id] = {
            "channel_id": str(channel.id),
            "youtube_channel_id": youtube_channel_id
        }

        # 保存
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        await interaction.followup.send(
            f"✅ 登録しました：\n- 通知先: {channel.mention}\n- YouTubeチャンネルID: `{youtube_channel_id}`",
            ephemeral=True
        )
