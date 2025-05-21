import discord
from discord.ext import commands
from commands.subscribe import Subscribe
from commands.notify_latest import NotifyLatest
from commands.notify_past import NotifyPast
from keep_alive import keep_alive  # ← Flaskサーバー起動
import os

TOKEN = os.environ.get("DISCORD_TOKEN")

# Bot定義（discord.py v2 対応）
class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.add_cog(Subscribe(self))
        await self.add_cog(NotifyLatest(self))
        await self.add_cog(NotifyPast(self))
        await self.tree.sync()
        print("✅ コマンド同期完了")

intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(command_prefix="!", intents=intents)

if __name__ == "__main__":
    keep_alive()  # Flask HTTPサーバーを起動（Renderのポートスキャン対策）
    bot.run(TOKEN)
