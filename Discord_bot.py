import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
# Load variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
NEWS_KEY = os.getenv("NEWS_KEY")

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

    if message.content.startswith('!hello'):
        await message.channel.send('Hey pookie bear!')

    await bot.process_commands(message)

@bot.command()
async def sports(ctx):
    url = f"https://newsapi.org/v2/everything?q=sports&sortBy=publishedAt&apiKey={NEWS_KEY}"
    response = requests.get(url).json()

    # Get first headline
    article = response["articles"][0]
    title = article["title"]
    link = article["url"]

    await ctx.send(f"**Sports Update:** {title}\n🔗 {link}")

@bot.command()
async def games(ctx):
    await ctx.send("Gaming news coming soon!")

bot.run(TOKEN)
