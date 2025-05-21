import discord
from discord.ext import commands
from commands.subscribe import Subscribe
from commands.notify_latest import NotifyLatest
from commands.notify_past import NotifyPast
import os

TOKEN = os.environ.get("DISCORD_TOKEN")

# Bot定義（v2.0仕様）
class MyBot(commands.Bot):
    async def setup_hook(self):
        # コグ登録
        await self.add_cog(Subscribe(self))
        await self.add_cog(NotifyLatest(self))
        await self.add_cog(NotifyPast(self))
        # スラッシュコマンド同期
        await self.tree.sync()
        print("✅ コマンド同期完了")

intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の取得を許可

bot = MyBot(command_prefix="!", intents=intents)

if __name__ == "__main__":
    bot.run(TOKEN)

