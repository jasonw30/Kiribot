import discord
import discord.ext
from discord.ext import tasks
import sympy as sym
import asyncio
from pathlib import Path
from apicalls import OsuData, embed_osu, musicEngine
from localbot import UserDataManager

LAST_UPDATED = "3/13/2024"


@tasks.loop(seconds=300) #5 minute configuration
async def data_saving():
    UserDataManager.async_save()

class KiriBot:

    intents = discord.Intents.all() 
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)
    musicPlayer = musicEngine(enabled=True)
    
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


@KiriBot.tree.command(name="getserverinfo", description="Gets some basic server information")
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


@KiriBot.tree.command(name='talk', description='talks for you')
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
    print(f"[END] The user currently has {userData.exp}")
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


@KiriBot.tree.command(name='getuserinfo', description='gets the userInformation')
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
    result = await KiriBot.musicPlayer.enqueue_song(link)
    try:
        if result:
            await interaction.response.send_message(f"Successfully enqueued song: {link}")
        else:
            await interaction.response.send_message(f"Problem with enqueueing the song.")
    except discord.app_commands.errors.CommandInvokeError as e:
        print(e)
        await interaction.response.send_message(f"An error has occured, but likely is added {link} check the queue.")

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


@KiriBot.tree.command(name="cur_ver", description="gets the current verison of the bot")
async def slash_command_two(interaction: discord.Interaction):    
    await interaction.response.send_message(f"Last Updated: {LAST_UPDATED}")


@KiriBot.tree.command(name="stats", description="gets the user own stats")
async def stats(interaction: discord.Interaction):
    userData = UserDataManager.get_user_stats(interaction.user.id)
    await interaction.response.send_message(f"Your current exp {userData.exp} and your current ${userData.money}")
