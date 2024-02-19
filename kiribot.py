import discord
import discord.ext
import sympy as sym
import asyncio
from pathlib import Path
from apicalls import OsuData, embed_osu, musicEngine

class KiriBot:

    intents = discord.Intents.all() 
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)
    musicPlayer = musicEngine(enabled=True)
    
    def __init__(self, token):
        self.token = token
        KiriBot.client.run(self.token)
        print(f"[KiriBot] Initating Bot -> {token}")


@KiriBot.client.event
async def on_ready():
    await KiriBot.tree.sync(guild=None)
    activity = discord.Game(name="go touch grass", type=3)
    await KiriBot.client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    print("[KiriBot] Initalized Bot")

@KiriBot.tree.command(name="getallusers", description="lists out of all of the users in the server")
async def slash_command(interaction: discord.Interaction):
    result = interaction.guild_id
    await interaction.response.send_message(f"[Was Sent From -> ] Current Guild: {result}")
    all_members = []
    test = []
    for i in interaction.guild.members:
        test.append(i)
        all_members.append((i.name, i.display_name))
    
    print(all_members)
    print(test)
    await KiriBot.client.get_channel(interaction.channel_id).send(all_members)

@KiriBot.tree.command(name="getserverinfo", description="gets some basic server information")
async def getserverinfo(interaction: discord.Interaction):
    await interaction.response.send_message("Nothing yet.")

@KiriBot.tree.command(name='vc-up', description='literally joins the current voice channel you are currently in')
async def join_vc(interaction:discord.Interaction):
    await interaction.response.send_message(f"Please Hold. Attempting to Join {interaction.user}'s voice channel. (If Exists)")
    current_user = interaction.user.voice.channel
    await current_user.connect()
    await KiriBot.client.get_channel(interaction.channel_id).send(f"Joined Voice Channel: {current_user}")


@KiriBot.tree.command(name="differentiate", description="you can't do math confirmed")
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
        await interaction.response.send_message(f"Found music. Joining a voice call. Please Hold On.")
        current_user = interaction.guild.voice_client

        if not interaction.guild.voice_client or not current_user.is_connected():
            current_user = interaction.user.voice.channel
            current_user = await current_user.connect()
        
        while current_song:
            await KiriBot.client.get_channel(interaction.channel_id).send(f"Now Playing: {Path(current_song).stem}.")
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


@KiriBot.tree.command(name="cur_version", description="gets the current verison of the bot")
async def slash_command_two(interaction: discord.Interaction):    
    await interaction.response.send_message("2.0")

@KiriBot.tree.command(name="new_updates", description="gets the new update")
async def new_updates(interaction: discord.Interaction):
    await interaction.response.send_message("Latest Version added music functionality")


if __name__ == "__main__":
    print("Starting Bot")
    KiriBot("NTI5ODkyMDY3NTkwMjc1MTA0.GRANXX.9UgDpJlKmn_qef36IDLCb9D1I1qbLc1_kGblnY")