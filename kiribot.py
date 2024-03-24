import discord
import discord.ext
from discord.ext import tasks
import sympy as sym
import asyncio
from pathlib import Path
from apicalls import OsuData, embed_osu, musicEngine, animeListAPI
from localbot import UserDataManager, AdminCommands, AdminManager, generate_level_up_card
from datetime import datetime

LAST_UPDATED = "3/23/2024"


@tasks.loop(seconds=300) #5 minute configuration
async def data_saving():
    UserDataManager.async_save()
    UserDataManager.async_reset_cache()

class KiriBot:

    intents = discord.Intents.all() 
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)
    musicPlayer = musicEngine(enabled=True)
    adminEngine = AdminCommands()
    myAnimeList = animeListAPI()
    
    def __init__(self, token):
        print(f"[KiriBot] Initating Bot -> {token}")
        self.token = token
        KiriBot.client.run(self.token)    

@KiriBot.client.event
async def on_ready():
    await KiriBot.tree.sync(guild=None)
    activity = discord.Game(name="touching grass...", type=3)
    await KiriBot.client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    data_saving.start()
    print("[KiriBot] Initalized Bot")


@KiriBot.tree.command(name="get_server_info", description="Gets some basic server information")
async def getserverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if guild:
        embed = discord.Embed(title="Server Information", color=discord.Color.blurple())
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Server Owner", value=guild.owner, inline=False)
        embed.add_field(name="Total Members", value=guild.member_count, inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("This command must be used in a server.")


@KiriBot.tree.command(name='bot_talk', description='talks for you')
async def talk(interaction:discord.Interaction, message:str, id: str):
    if interaction and message and id:
        await KiriBot.client.get_channel(int(id)).send(f"{message}")
        await interaction.response.send_message(">.<")
    else:
        await interaction.response.send_message("Invalid Inputs.")

@KiriBot.client.event
async def on_message(message):
    # Check if the message was sent by a user and not a bot (including your own bot)
    if message.author.bot:
        return

    userData = UserDataManager.get_user_stats(str(message.author.id))
    UserDataManager.update_exp(userData, userData.exp + 1)
    UserDataManager.update_money(userData, userData.money + 1)
    UserDataManager.save_user_stats(userData)

    print(f"{message.author} -> {message.content} (Channel: {message.channel})")


@KiriBot.tree.command(name="calculus-differentiate", description="does calculus")
async def differentiate(interaction: discord.Interaction, equation: str, respect_to: str):
    equation = equation.replace("^", "**")
    print("with respect to", respect_to)
    print("equation", equation)
    alphabets = " ".join([i for i in equation if i.isalpha()])
    stralpha = f"{','.join([i for i in equation if i.isalpha()])}=sym.symbols('{alphabets}')"
    stralpha3 = f"derivative_result = sym.diff(equation, {respect_to})"
    print(stralpha)
    print(stralpha3)

    exec(stralpha)
    exec(stralpha3)
    await interaction.response.send_message(str(locals()["derivative_result"]).replace("**", "^"))

@KiriBot.tree.command(name='get_user_info', description='gets the userInformation')
async def get_user_info(interaction: discord.Interaction, user: discord.Member):
    get_query = None #get_results(user.id)
    if get_query:
        pass
        await interaction.response.send_message("This is about to be implemented.")
    else:
        await interaction.response.send_message("There is an issue fetching user data. Please Try again.")

@KiriBot.tree.command(name="get_osu_top_plays", description="Gets the top 10 plays for the user")
async def get_osu_top_plays(interaction: discord.Interaction, player: str) -> list:
    osu_data = OsuData()
    osu_data_plays = osu_data.get_user_plays(player, limit=10, type="best")

    if osu_data and osu_data_plays:
        send_this = embed_osu(player, osu_data_plays)
        await interaction.response.send_message(embed=send_this)
    else:
        await interaction.response.send_message("Error has occured. Either Player does not exist or Timed Out.")
        
@KiriBot.tree.command(name="enqueue_song", description="Adds a song to the queue")
async def enqueue_song(interaction:discord.Interaction, link: str):
    await interaction.response.send_message(f"Enqueued song: {link}")
    result = await KiriBot.musicPlayer.enqueue_song(link)

@KiriBot.tree.command(name="show_queue", description="gets all of the song in the queue currently")
async def show_queue(interaction:discord.Interaction):
    result = await KiriBot.musicPlayer.song_embed()
    try:
        if result:
            await interaction.response.send_message(embed=result)
        else:
            await interaction.response.send_message("No music currently in the queue")
    except discord.app_commands.errors.CommandInvokeError as e:
        print(e)
        await interaction.response.send_message(f"An error has occured with discord. Please try again.")


@KiriBot.tree.command(name="play_music", description="plays the music and joins the current vc you are in, if there is a queue.")
async def play_music(interaction:discord.Interaction):
    current_song = await KiriBot.musicPlayer.dequeue_song()
    if current_song:

        current_user = interaction.guild.voice_client

        if not interaction.guild.voice_client or not current_user.is_connected():
            current_user = interaction.user.voice.channel
            current_user = await current_user.connect()
        
        while current_song:
            await interaction.response.send_message(interaction.channel_id).send(f"Now Playing: {Path(current_song).stem}.")
            current_user.play(discord.FFmpegPCMAudio(current_song))

            while current_user.is_playing():
                await asyncio.sleep(1)
            
            current_song = await KiriBot.musicPlayer.dequeue_song()

    else:
        await interaction.response.send_message("There are no songs in the queue.")


@KiriBot.tree.command(name="skip_current_song", description="skips the current song that is currently playing")
async def skip_current_song(interaction:discord.Interaction):
    current_user = interaction.guild.voice_client
    if current_user and current_user.is_connected():
        current_user.stop()
    
    await interaction.response.send_message(f"If there is a song that is currently playing right now, it will be skipped.")


@KiriBot.tree.command(name="current_version", description="gets the current verison of the bot")
async def slash_command_two(interaction: discord.Interaction):    
    await interaction.response.send_message(f"Last Updated: {LAST_UPDATED}")

@KiriBot.tree.command(name="stats", description="gets the user own stats")
async def stats(interaction: discord.Interaction):
    userData = UserDataManager.get_user_stats(interaction.user.id)
    level_card = await generate_level_up_card(userData, interaction.guild.get_member(interaction.user.id), interaction.user.display_name)
    await interaction.response.send_message(f"Your current exp {userData.exp} and your current ${userData.money}", file=level_card)

@KiriBot.tree.command(name='translate', description='translates')
async def translate(interaction: discord.Interaction, message: str, language: str):
    await interaction.response.send_message(f"This is coming soon. Need to implement the API")

@KiriBot.tree.command(name='mute_user', description='mutes user')
async def mute(interaction: discord.Interaction, user_id: str, reason: str):
    response = await KiriBot.adminEngine.mute_user(interaction, interaction.user.id, user_id, reason)
    await interaction.response.send_message(f"{response}, {reason}")

@KiriBot.tree.command(name='unmute_user', description='unmutes user')
async def unmute(interaction: discord.Interaction, user_id: str, reason: str):
    response = await KiriBot.adminEngine.unmute_user(interaction, interaction.user.id, user_id)
    await interaction.response.send_message(f"{response}, {reason}")

@KiriBot.tree.command(name='admin_list', description='lists out all of the admins')
async def list_admins(interaction: discord.Interaction):
    response = AdminManager.getAdmins()
    await interaction.response.send_message(f"{response}")

@KiriBot.tree.command(name='admin_add', description='adds an admin to the list')
async def admin_add(interaction: discord.Interaction, user_id: str):
    response = AdminManager.addAdmin(user_id)
    await interaction.response.send_message(f"{response}")

@KiriBot.tree.command(name='admin_remove', description='removes an admin to the list')
async def admin_remove(interaction: discord.Interaction, user_id: str):
    response = AdminManager.removeAdmin(user_id)
    await interaction.response.send_message(f"{response}")

@KiriBot.tree.command(name='reset_admins', description='resets all admins')
async def admin_remove(interaction: discord.Interaction):
    response = AdminManager.resetAdmin()
    await interaction.response.send_message(f"{response}")

@KiriBot.tree.command(name='get_anime_search', description='returns a list of anime')
async def get_anime_search(interaction: discord.Interaction, search_query: str):
    response = KiriBot.myAnimeList.get_anime_search(search_query)
    embed_list = KiriBot.myAnimeList.anime_search_embed(response, search_query)
    
    if embed_list:
        await pagination(interaction=interaction, embed_list=embed_list)
    else:
        await interaction.response.send_message("Found no results.")

@KiriBot.tree.command(name='get_manga_search', description='returns a list of manga')
async def get_manga_search(interaction: discord.Interaction, search_query: str):
    response = KiriBot.myAnimeList.get_manga_search(search_query)
    embed_list = KiriBot.myAnimeList.manga_search_embed(response, search_query)

    if embed_list:
        await pagination(interaction=interaction, embed_list=embed_list)
    else:
        await interaction.response.send_message("Found no results.")


@KiriBot.tree.command(name='get_anime_info', description='returns anime info given id')
async def get_anime_info(interaction: discord.Interaction, search_id_query: str):
    print(f"Searching for {search_id_query}")
                    
    response = KiriBot.myAnimeList.get_anime_search_by_id(search_id_query)

    if response:
        await interaction.response.send_message(embed=KiriBot.myAnimeList.anime_info_embed(response, KiriBot.client.user.avatar))
    else:
        await interaction.response.send_message("Unable to find the query.")

@KiriBot.tree.command(name='generate_random_anime', description='generates a random anime')
async def generate_random_anime(interaction: discord.Interaction):
    response = KiriBot.myAnimeList.get_anime_search_by_id()
    if response:
        await interaction.response.send_message(embed=KiriBot.myAnimeList.anime_info_embed(response, KiriBot.client.user.avatar))
    else:
        await interaction.response.send_message("Failed to generate a random anime")
    
@KiriBot.tree.command(name='get_manga_info', description='returns manga info given id')
async def get_anime_info(interaction: discord.Interaction, search_id_query: str):
    print(f"Searching for {search_id_query}")
                    
    response = KiriBot.myAnimeList.get_manga_search_by_id(search_id_query)

    if response:
        await interaction.response.send_message(embed=KiriBot.myAnimeList.manga_info_embed(response, KiriBot.client.user.avatar))
    else:
        await interaction.response.send_message("Unable to find the query.")

@KiriBot.tree.command(name='generate_random_manga', description='generates a random manga')
async def generate_random_anime(interaction: discord.Interaction):
    response = KiriBot.myAnimeList.get_manga_search_by_id()
    if response:
        await interaction.response.send_message(embed=KiriBot.myAnimeList.manga_info_embed(response, KiriBot.client.user.avatar))
    else:
        await interaction.response.send_message("Failed to generate a random anime")


async def pagination(interaction, embed_list):
    current_page = 0
    await interaction.response.send_message(embed=embed_list[current_page])
    message = await interaction.original_response()
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def callback_check(reaction, user):
        if str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡️":
            return str(reaction.emoji), user
        
    while True:

        reaction, user = await interaction.client.wait_for("reaction_add", timeout=60, check=callback_check)
        
        if str(reaction.emoji) == "➡️":
            current_page = min(current_page + 1, len(embed_list))
        elif str(reaction.emoji) == "⬅️":
            current_page = max(current_page - 1, 0)

        await message.edit(embed=embed_list[current_page])
