import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hey pookie bear!')

    # Allow commands to still work when on_message is overridden
    await bot.process_commands(message)

bot.run(TOKEN)
