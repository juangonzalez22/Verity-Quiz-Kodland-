import os
from threading import Thread
from flask import Flask, render_template
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='assets')

@app.route('/')
def home():
    invite_url = os.getenv("DISCORD_INVITE_URL", "#")
    github_url = os.getenv("GITHUB_URL", "#")
    return render_template('index.html', invite_url=invite_url, github_url=github_url)

def run():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def setup_hook():
    await bot.load_extension('cogs.quiz_cog')

@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user}')

if __name__ == '__main__':
    keep_alive()
    bot.run(os.getenv('DISCORD_TOKEN'))