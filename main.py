import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not GIPHY_API_KEY:
        print("Warning: GIPHY_API_KEY missing in .env, running without GIFs.")

async def main():
    async with bot:
        await bot.load_extension("cogs.quiz_cog")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())