import discord
from discord.ext import commands
import os
import asyncio
import dotenv
dotenv.load_dotenv("./data/.env")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("📦 Syncing slash commands...")
    await bot.tree.sync()
    print("✅ Slash commands synced!")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load {cog_name}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))  # replace with your actual token or load from .env

if __name__ == "__main__":
    asyncio.run(main())
