import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import logging

# Load variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
NEWS_KEY = os.getenv("NEWS_KEY")
APITUBE_KEY = os.getenv("APITUBE_KEY")

# ---- Setup logging ----
logging.basicConfig(
    filename='discord.log',
    level = logging.DEBUG, #Highest level of logging
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)
# -----------------------

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
async def sports(ctx, *, query: str = "sports"): #was going to use gpt but then remembered args and kwargs exist
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_KEY}"
    )

    response = requests.get(url).json()
    articles = response.get("articles", [])

    if not articles:
        await ctx.send(f"No sports news found for **{query}** 🤷‍♂️")
        return

    article = articles[0]

    title = article.get("title", "No title available")
    desc = article.get("description", "No description available")
    link = article.get("url")
    image = article.get("urlToImage")
    
    #still need to read up on embeds
    embed = discord.Embed(
        title=title,
        url=link,
        description=desc,
        color=0x2ecc71
    )

    if image:
        embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command()
async def gaming(ctx, limit: int = 2):
    url = "https://api.apitube.io/v1/news/everything"
    params = {
        "topic.id": "video_games_news",
        "per_page": limit,
        "api_key": APITUBE_KEY
    } 
    response = requests.get(url, params=params).json()#I just know it uploads the info into json format.
    articles = response.get("data", response.get("articles", []))
    if not articles:
        await ctx.send("No gaming news found 🤷‍♂️")
        return

    msg = "**🎮 Latest Gaming News**\n\n"
    for art in articles[:limit]:
        title = art.get("title")
        link = art.get("url")
        msg += f"- {title}\n  {link}\n\n"
    #Work but currently finds no gaming news.
    await ctx.send(msg)

#Work on embeds later.

bot.run(TOKEN)
