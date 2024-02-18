import pytube
import discord
from pathlib import Path
import asyncio

PATH_DOWNLOAD = Path(".") / Path("tmpsongs")

class musicEngine:

    music_queue = []

    def __init__(self, enabled=False):
        self.enabled=enabled
        if (self.enabled):
            print("You have enabled youtube downloading api calls. Use Responsbily")

    async def search_music(self, search_query=None):
        if self.enabled and search_query:
            print("Currently in the works. Will need to implement YoutubeAPI")
            """
            search_results = None
            if search_results:
                for i in search_results:
                    print(i)
            """
    
    async def enqueue_song(self, link=None):
        try:
            if self.enabled and link and len(musicEngine.music_queue) <= 9:
                pytubeEngine = pytube.YouTube(link)
                video_stream = pytubeEngine.streams.get_lowest_resolution()
                tmp_video = video_stream.download(PATH_DOWNLOAD)
                musicEngine.music_queue.append(tmp_video)
                print(f"Downloaded Song: {link}")
                return True
        except pytube.exceptions.PytubeError as error:
            print(error)
            return False
    
    async def dequeue_song(self):
        if musicEngine.music_queue:
            popped_music = musicEngine.music_queue[0]
            del musicEngine.music_queue[0]
            return popped_music
        else:
            return None
    
    async def delete_song(self, song_location=None):
        
        if song_location and Path(song_location).exists():
            Path(song_location).unlink()
            print(f"File has successfully been removed: {song_location}")
        else:
            print("File does not exist.")
        
    async def song_embed(self):
        
        total_length = len(musicEngine.music_queue)
        custom_embed = discord.Embed(title=f"Music Player - Current Queue", color=0xfb86d7)
        
        if total_length > 0:
            for index, song in enumerate(musicEngine.music_queue):
                custom_embed.add_field(name=f"{index+1}: {Path(song).stem}", value="\u200b\n", inline=True)
            return custom_embed
        else:
            return None

    

if __name__ == "__main__":
    music = musicEngine(enabled=True)
