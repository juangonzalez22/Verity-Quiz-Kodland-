import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

app = Flask('')

@app.route('/')
def home():
    invite_url = os.getenv("DISCORD_INVITE_URL", "#")
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Bot Quiz Discord</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            a {{
                display: inline-block;
                margin-top: 15px;
                padding: 10px 20px;
                background-color: #5865F2;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Bot Quiz Discord</h2>
            <p>El bot está activo y operativo.</p>
            <a href="{invite_url}">Invitar al servidor</a>
        </div>
    </body>
    </html>
    '''

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