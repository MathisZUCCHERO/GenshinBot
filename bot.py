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

##region Info command
@bot.tree.command(name="info", description="Get the information card of a character")
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
        if current.lower() in val["name"].lower():
            names.append(val["name"].capitalize())
    return [
        discord.app_commands.Choice(name=name, value=name)
        for name in names
    ]
##endregion

def exist(name: str) -> bool:
    if collection.find_one({"name": name.lower()}) is None:
        return False
    return True

##region Add character
@bot.tree.command(name="add", description="Add new character to the database")
async def add(interaction: discord.Interaction, name: str, card_url: str):
    if not exist(name):
        collection.insert_one({"name": name.lower(), "url": card_url})
        await interaction.response.send_message("Personnage ajouter avec succès.")
        return
    await interaction.response.send_message("Ce personnage est déjà enregistré.")
##endregion

##region Update character
@bot.tree.command(name="update", description="Update card url of character in the database")
async def update(interaction: discord.Interaction, name: str, card_url: str):
    if exist(name):
        filter = {"name": name.lower()}
        new_value = { "$set": { "url": card_url } }
        collection.update_one(filter, new_value)
        await interaction.response.send_message("Personnage modifié avec succès.")
        return
    await interaction.response.send_message("Ce personnage n'existe pas, créé le avec la commande /add.")

@update.autocomplete('name')
async def name_autocomplete(
        interaction: discord.Interaction,
        current: str
) -> List[discord.app_commands.Choice[str]]:
    names = []
    for val in collection.find({'name': {'$ne': None}}):
        if current.lower() in val["name"].lower():
            names.append(val["name"].capitalize())
    return [
        discord.app_commands.Choice(name=name, value=name)
        for name in names
    ]
##endregion

bot.run(os.getenv('DISCORD_TOKEN'))
