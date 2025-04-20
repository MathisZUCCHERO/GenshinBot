import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

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

@bot.tree.command(name="test", description="Tester les embeds")
async def warnguy(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Test title",
        description="Test description",
        color=discord.Color.purple()
    )
    embed.add_field(name="Genshin", value="Créer un bot genshin", inline=False)
    embed.add_field(name="Wuthering Wave", value="Créer un bot WUWA", inline=False)
    embed.add_field(name="Minecraft", value="Créer un bot minecraft", inline=False)
    embed.set_footer(text="Test")
    embed.set_image(url="https://media.discordapp.net/attachments/1148642561498550353/1356774680559747132/D1_ifa_apti_template_FINI.png?ex=68062e23&is=6804dca3&hm=0a27b729600e05e364c815dd25ccf35b161e332a49e5d31736292c147d4b10fa&=&format=webp&quality=lossless&width=712&height=856")

    await interaction.response.send_message(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))
