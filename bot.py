import asyncio
from typing import List
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
database = client.get_database(os.getenv("DATABASE"))
collection = database.get_collection(os.getenv("COLLECTION"))

print("Lancement du bot...")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot allumé !")
    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced : {len(synced)}")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message : discord.Message):
    if message.author.bot:
        return
    if message.content == "ping":
        channel = message.channel
        author = message.author
        await author.send("pong")
    if message.content == "gen":
        gen_channel = bot.get_channel(883991837570916365)
        await gen_channel.send("Hello there !")

@bot.tree.command(name="youtube", description="Affiche ma chaine YTB")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien de ma chaine YTB: ")

@bot.tree.command(name="warnguy", description="Alerter une personne")
async def warnguy(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message("Alerte envoyé")
    await member.send("Bot creation in progress...")

##region Info command
@bot.tree.command(name="info", description="Tester les embeds")
async def info(interaction: discord.Interaction, name: str):
    embed = discord.Embed(
        title=name.capitalize(),
        color=discord.Color.purple()
    )
    picture = load_db(name)
    embed.set_image(url=picture["url"])
    await interaction.response.send_message(embed=embed)

def load_db(name):
    try:
        query = { "name": name.lower() }
        movie = collection.find_one(query)
        return movie
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)

@info.autocomplete('name')
async def name_autocomplete(
        interaction: discord.Interaction,
        current: str
) -> List[discord.app_commands.Choice[str]]:
    names = []
    for val in collection.find({'name': {'$ne': None}}):
        names.append(val["name"].capitalize())
    return [
        discord.app_commands.Choice(name=name, value=name)
        for name in names
    ]

##endregion

bot.run(os.getenv('DISCORD_TOKEN'))
