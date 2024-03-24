import requests
import configparser
from pathlib import Path
import discord
import math
from datetime import datetime

config = configparser.ConfigParser()
config.read(Path(".").parent / Path("configuration.ini"))
ENABLED = bool(config.get('API', 'AnimeList-API'))

API_URL = 'https://api.jikan.moe/v4/anime/'
MANGA_API_URL = "https://api.jikan.moe/v4/manga/"


class MangaQueryResult:

    def __init__(self, mal_id, url, images, approved, titles, title, title_english, title_japanese, title_synonyms,
                 manga_type, chapters, volumes, status, publishing, published, score, scored_by, rank, popularity,
                 members, favorites, synopsis, background, authors, serializations, genres, explicit_genres,
                 themes, demographics):
    
        self.mal_id = mal_id
        self.url = url
        self.images = images
        self.approved = approved
        self.titles = titles
        self.title = title
        self.title_english = title_english
        self.title_japanese = title_japanese
        self.title_synonyms = title_synonyms
        self.manga_type = manga_type
        self.chapters = chapters
        self.volumes = volumes
        self.status = status
        self.publishing = publishing
        self.published = published
        self.score = score
        self.scored_by = scored_by
        self.rank = rank
        self.popularity = popularity
        self.members = members
        self.favorites = favorites
        self.synopsis = synopsis
        self.background = background
        self.authors = authors
        self.serializations = serializations
        self.genres = genres
        self.explicit_genres = explicit_genres
        self.themes = themes
        self.demographics = demographics

class AnimeQueryResult:

    def __init__(self, mal_id, url, images, trailer, approved, titles, title, title_english, title_japanese, title_synonyms,
                 anime_type, source, episodes, status, airing, aired, duration, rating, score, scored_by, rank, popularity,
                 members, favorites, synopsis, background, season, year, broadcast, producers, licensors, studios,
                 genres, explicit_genres, themes, demographics):

        self.mal_id = mal_id
        self.url = url
        self.images = images
        self.trailer = trailer
        self.approved = approved
        self.titles = titles
        self.title = title
        self.title_english = title_english
        self.title_japanese = title_japanese
        self.title_synonyms = title_synonyms
        self.anime_type = anime_type
        self.source = source
        self.episodes = episodes
        self.status = status
        self.airing = airing
        self.aired = aired
        self.duration = duration
        self.rating = rating
        self.score = score
        self.scored_by = scored_by
        self.rank = rank
        self.popularity = popularity
        self.members = members
        self.favorites = favorites
        self.synopsis = synopsis
        self.background = background
        self.season = season
        self.year = year
        self.broadcast = broadcast
        self.producers = producers
        self.licensors = licensors
        self.studios = studios
        self.genres = genres
        self.explicit_genres = explicit_genres
        self.themes = themes
        self.demographics = demographics


class animeListAPI:

    def __init__(self, enabled=ENABLED):
        print("Initated myanimelist api")
        self.enabled = enabled

    def get_anime_search(self, search_query) -> list[AnimeQueryResult]:

        return_results = []

        if self.enabled:
            parameters = {'q': str(search_query)}
            results = requests.get(url=API_URL, params=parameters)

            if results.status_code == 200:
                returned_query = results.json()

                for anime_result in returned_query['data']:

                    animeQuery = AnimeQueryResult(
                        mal_id=anime_result['mal_id'],
                        url=anime_result['url'],
                        images=anime_result['images'],
                        trailer=anime_result['trailer'],
                        approved=anime_result['approved'],
                        titles=anime_result['titles'],
                        title=anime_result['title'],
                        title_english=anime_result['title_english'],
                        title_japanese=anime_result['title_japanese'],
                        title_synonyms=anime_result['title_synonyms'],
                        anime_type=anime_result['type'],
                        source=anime_result['source'],
                        episodes=anime_result['episodes'],
                        status=anime_result['status'],
                        airing=anime_result['airing'],
                        aired=anime_result['aired'],
                        duration=anime_result['duration'],
                        rating=anime_result['rating'],
                        score=anime_result['score'],
                        scored_by=anime_result['scored_by'],
                        rank=anime_result['rank'],
                        popularity=anime_result['popularity'],
                        members=anime_result['members'],
                        favorites=anime_result['favorites'],
                        synopsis=anime_result['synopsis'],
                        background=anime_result['background'],
                        season=anime_result['season'],
                        year=anime_result['year'],
                        broadcast=anime_result['broadcast'],
                        producers=anime_result['producers'],
                        licensors=anime_result['licensors'],
                        studios=anime_result['studios'],
                        genres=anime_result['genres'],
                        explicit_genres=anime_result['explicit_genres'],
                        themes=anime_result['themes'],
                        demographics=anime_result['demographics'],
                    )

                    return_results.append(animeQuery)

        return return_results

    
    def get_anime_search_by_id(self, search_query=None) -> MangaQueryResult:

        if self.enabled:
            
            if search_query:
                results = requests.get(url=API_URL + search_query)
            else:
                results = requests.get(url="https://api.jikan.moe/v4/random/anime")

            if results.status_code == 200:
                returned_query = results.json()

                anime_result = returned_query['data']

                animeQuery = AnimeQueryResult(
                        mal_id=anime_result['mal_id'],
                        url=anime_result['url'],
                        images=anime_result['images'],
                        trailer=anime_result['trailer'],
                        approved=anime_result['approved'],
                        titles=anime_result['titles'],
                        title=anime_result['title'],
                        title_english=anime_result['title_english'],
                        title_japanese=anime_result['title_japanese'],
                        title_synonyms=anime_result['title_synonyms'],
                        anime_type=anime_result['type'],
                        source=anime_result['source'],
                        episodes=anime_result['episodes'],
                        status=anime_result['status'],
                        airing=anime_result['airing'],
                        aired=anime_result['aired'],
                        duration=anime_result['duration'],
                        rating=anime_result['rating'],
                        score=anime_result['score'],
                        scored_by=anime_result['scored_by'],
                        rank=anime_result['rank'],
                        popularity=anime_result['popularity'],
                        members=anime_result['members'],
                        favorites=anime_result['favorites'],
                        synopsis=anime_result['synopsis'],
                        background=anime_result['background'],
                        season=anime_result['season'],
                        year=anime_result['year'],
                        broadcast=anime_result['broadcast'],
                        producers=anime_result['producers'],
                        licensors=anime_result['licensors'],
                        studios=anime_result['studios'],
                        genres=anime_result['genres'],
                        explicit_genres=anime_result['explicit_genres'],
                        themes=anime_result['themes'],
                        demographics=anime_result['demographics'],
                    )
                print(animeQuery.__dict__)

                return animeQuery

        return None
    

    def get_manga_search_by_id(self, search_query=None) -> MangaQueryResult:

        if self.enabled:
        
            if search_query:
                results = requests.get(url=MANGA_API_URL + search_query)
            else:
                results = requests.get(url="https://api.jikan.moe/v4/random/manga")

            if results.status_code == 200:
                returned_query = results.json()

                manga_result = returned_query['data']

                mangaQuery = MangaQueryResult(
                    mal_id=manga_result['mal_id'],
                    url=manga_result['url'],
                    images=manga_result['images'],
                    approved=manga_result['approved'],
                    titles=manga_result['titles'],
                    title=manga_result['title'],
                    title_english=manga_result['title_english'],
                    title_japanese=manga_result['title_japanese'],
                    title_synonyms=manga_result['title_synonyms'],
                    manga_type=manga_result['type'],
                    chapters=manga_result['chapters'],
                    volumes=manga_result['volumes'],
                    status=manga_result['status'],
                    publishing=manga_result['publishing'],
                    published=manga_result['published'],
                    score=manga_result['score'],
                    scored_by=manga_result['scored_by'],
                    rank=manga_result['rank'],
                    popularity=manga_result['popularity'],
                    members=manga_result['members'],
                    favorites=manga_result['favorites'],
                    synopsis=manga_result['synopsis'],
                    background=manga_result['background'],
                    authors=manga_result['authors'],
                    serializations=manga_result['serializations'],
                    genres=manga_result['genres'],
                    explicit_genres=manga_result['explicit_genres'],
                    themes=manga_result['themes'],
                    demographics=manga_result['demographics'],
                )

                print(mangaQuery.__dict__)

                return mangaQuery

        return None

    def get_manga_search(self, search_query) -> list[AnimeQueryResult]:

        return_results = []

        if self.enabled:
            parameters = {'q': str(search_query)}
            results = requests.get(url=MANGA_API_URL, params=parameters)

            if results.status_code == 200:
                returned_query = results.json()

                for manga_result in returned_query['data']:

                    mangaQuery = MangaQueryResult(
                        mal_id=manga_result['mal_id'],
                        url=manga_result['url'],
                        images=manga_result['images'],
                        approved=manga_result['approved'],
                        titles=manga_result['titles'],
                        title=manga_result['title'],
                        title_english=manga_result['title_english'],
                        title_japanese=manga_result['title_japanese'],
                        title_synonyms=manga_result['title_synonyms'],
                        manga_type=manga_result['type'],
                        chapters=manga_result['chapters'],
                        volumes=manga_result['volumes'],
                        status=manga_result['status'],
                        publishing=manga_result['publishing'],
                        published=manga_result['published'],
                        score=manga_result['score'],
                        scored_by=manga_result['scored_by'],
                        rank=manga_result['rank'],
                        popularity=manga_result['popularity'],
                        members=manga_result['members'],
                        favorites=manga_result['favorites'],
                        synopsis=manga_result['synopsis'],
                        background=manga_result['background'],
                        authors=manga_result['authors'],
                        serializations=manga_result['serializations'],
                        genres=manga_result['genres'],
                        explicit_genres=manga_result['explicit_genres'],
                        themes=manga_result['themes'],
                        demographics=manga_result['demographics'],
                    )

                    return_results.append(mangaQuery)

        return return_results


    @staticmethod
    def anime_search_embed(search_query_results: list[AnimeQueryResult], search_query_string: str):
        
        split_per_embed = 10
        split_size = math.ceil(int(len(search_query_results) / split_per_embed)) #10 per page
        print(split_size, len(search_query_results))
        all_embeds = []
        page_counter = 0

        for _ in range(split_size):
            page_counter += 1
            embed = discord.Embed(title=f"Anime Search: {search_query_string}", description=f"Showing {page_counter} out of {split_size} pages.", color=0xfb86d7)
            for result in (search_query_results[(page_counter * split_per_embed):((page_counter * split_per_embed) + 10)]):
                embed.add_field(name=result.titles[0]["title"], value=f"https://myanimelist.net/anime/{result.mal_id}", inline=False)
            all_embeds.append(embed)
        
        return all_embeds
    
    @staticmethod
    def anime_info_embed(response: AnimeQueryResult, bot_icon=None):
        
        if response.title_english and response.title_japanese:
            embed = discord.Embed(title=f"{response.title_english} / {response.title_japanese}",
                            url=f"https://myanimelist.net/anime/{response.mal_id}",
                            description=f"**__Synopsis__**:\n\n{response.synopsis}",
                            colour=0xf352ff,
                            timestamp=datetime.now())
        elif response.title_english and not response.title_japanese:
            embed = discord.Embed(title=f"{response.title_english}",
                                        url=f"https://myanimelist.net/anime/{response.mal_id}",
                                        description=f"**__Synopsis__**:\n\n{response.synopsis}",
                                        colour=0xf352ff,
                                        timestamp=datetime.now())
        elif response.title_japanese and not response.title_english:
            embed = discord.Embed(title=f"{response.title_japanese}",
                                        url=f"https://myanimelist.net/anime/{response.mal_id}",
                                        description=f"**__Synopsis__**:\n\n{response.synopsis}",
                                        colour=0xf352ff,
                                        timestamp=datetime.now())

        embed.set_author(name="MyAnimeList", url="https://myanimelist.net/", icon_url="https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAiC8a86sHufn_jOI-JGtoCQ")

        if response.score:
            embed.add_field(name=f"Rating (Score): {response.score}/10", value="", inline=False)
        if response.rank:
            embed.add_field(name=f"Ranked: #{response.rank}", value="", inline=False)
        if response.members:
            embed.add_field(name=f"Members: {response.members}", value="", inline=False)
        if response.popularity:
            embed.add_field(name=f"Popularity: #{response.popularity}", value="", inline=False)
        if response.aired and 'string' in response.aired:
            embed.add_field(name=f"Aired: {response.aired['string']}", value="", inline=False)
        if response.season:
            embed.add_field(name=f"Season/Year: {response.season[:1].upper() + response.season[1:]} {response.year}", value="", inline=False)
        if response.status:
            embed.add_field(name=f"Status: {response.status}", value="", inline=False)
        if response.genres:
            embed.add_field(name=f"Genres: {', '.join([genre['name'] for genre in response.genres])}", value='', inline=False)

        embed.set_thumbnail(url=f"{response.images['jpg']['image_url']}")
        embed.set_footer(text="Generated by KiriBot", icon_url=bot_icon)

        return embed

    @staticmethod
    def manga_info_embed(response: MangaQueryResult, bot_icon=None):
        
        if response.title_english and response.title_japanese:
            embed = discord.Embed(title=f"{response.title_english} / {response.title_japanese}",
                            url=f"https://myanimelist.net/manga/{response.mal_id}",
                            description=f"**__Synopsis__**:\n\n{response.synopsis}",
                            colour=0xf352ff,
                            timestamp=datetime.now())
        elif response.title_english and not response.title_japanese:
            embed = discord.Embed(title=f"{response.title_english}",
                                        url=f"https://myanimelist.net/manga/{response.mal_id}",
                                        description=f"**__Synopsis__**:\n\n{response.synopsis}",
                                        colour=0xf352ff,
                                        timestamp=datetime.now())
        elif response.title_japanese and not response.title_english:
            embed = discord.Embed(title=f"{response.title_japanese}",
                                        url=f"https://myanimelist.net/manga/{response.mal_id}",
                                        description=f"**__Synopsis__**:\n\n{response.synopsis}",
                                        colour=0xf352ff,
                                        timestamp=datetime.now())

        embed.set_author(name="MyAnimeList", url="https://myanimelist.net/", icon_url="https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAiC8a86sHufn_jOI-JGtoCQ")

        if response.score:
            embed.add_field(name=f"Rating (Score): {response.score}/10", value="", inline=False)
        if response.rank:
            embed.add_field(name=f"Ranked: #{response.rank}", value="", inline=False)
        if response.members:
            embed.add_field(name=f"Members: {response.members}", value="", inline=False)
        if response.popularity:
            embed.add_field(name=f"Popularity: #{response.popularity}", value="", inline=False)
        if response.status:
            embed.add_field(name=f"Status: {response.status}", value="", inline=False)
        if response.volumes:
            embed.add_field(name=f"Volumes: {response.volumes}", value="", inline=False)
        if response.chapters:
            embed.add_field(name=f"Chapters: {response.chapters}", value="", inline=False)
        if response.status:
            embed.add_field(name=f"Status: {response.status}", value="", inline=False)
        if response.published and 'string' in response.published:
            embed.add_field(name=f"Published: {response.published['string']}", value="", inline=False)
        if response.authors:
            embed.add_field(name=f"Authors: {', '.join([auth['name'] for auth in response.authors])}", value='', inline=False)
        if response.genres:
            embed.add_field(name=f"Genres: {', '.join([genre['name'] for genre in response.genres])}", value='', inline=False)
        embed.set_thumbnail(url=f"{response.images['jpg']['image_url']}")
        embed.set_footer(text="Generated by KiriBot", icon_url=bot_icon)

        return embed
    
    @staticmethod
    def manga_search_embed(search_query_results: list[MangaQueryResult], search_query_string: str):
        
        split_per_embed = 10
        split_size = math.ceil(int(len(search_query_results) / split_per_embed)) #10 per page
        print(split_size, len(search_query_results))
        all_embeds = []
        page_counter = 0

        for _ in range(split_size):
            page_counter += 1
            embed = discord.Embed(title=f"Manga Search: {search_query_string}", description=f"Showing {page_counter} out of {split_size} pages.", color=0xfb86d7)
            for result in (search_query_results[(page_counter * split_per_embed):((page_counter * split_per_embed) + 10)]):
                embed.add_field(name=result.titles[0]["title"], value=f"https://myanimelist.net/manga/{result.mal_id}", inline=False)
            all_embeds.append(embed)
        
        return all_embeds
        