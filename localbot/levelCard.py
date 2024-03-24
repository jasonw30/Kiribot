import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

FONT_PATH = Path(".").parent / Path("fonts")
IMAGES_PATH = Path(".").parent / Path("images")
TEMP_IMAGES = Path(".").parent / Path("images/tmpimages")
BACKGROUND_CARD_PATH = IMAGES_PATH / Path("backgroundcard3.jpg")

async def generate_level_up_card(userData, discord_member, userName) -> discord.File:
    
    #default background image
    profile_picture = await download_user_image(discord_member=discord_member)
    background_card = Image.open(BACKGROUND_CARD_PATH)
    background_card.resize((807, 208))
    font_regular = ImageFont.truetype(FONT_PATH / Path("ComicNeue-Bold.ttf"), 50)
    draw = ImageDraw.Draw(background_card)
    
    avatar = Image.open(profile_picture)
    avatar = avatar.resize((115, 115))
    background_card.paste(avatar, (692, 0))
    bar_progress_fill = ((userData.exp / 100) / 100)
    progress_bar = Image.open(create_progress_bar(650, 40, bar_progress_fill))
    background_card.paste(progress_bar, (10, 125))

    draw.text((10, 10), f"{userName[:1].upper() + userName[1:]} [{get_rank_title(userData.exp)}]", fill=(255, 255, 255), font=font_regular)
    draw.text((10, 60), f"Level: {math.floor((userData.exp / 100))}", fill=(255, 255, 255), font=font_regular)

    level_card_path = TEMP_IMAGES / Path("level_card.png")
    background_card.save(level_card_path)
    file = discord.File(level_card_path)
    return file


async def download_user_image(discord_member: discord.Member):
    
    user_avatar = discord_member.avatar

    if user_avatar:
        file_location = TEMP_IMAGES / Path("avatar.jpg")
        await discord_member.avatar.save(file_location)
        return file_location

    return None

def draw_rounded_rectangle(draw, xy, fill=None, outline=None, width=0, radius=8):
    x0, y0, x1, y1 = xy
    draw.arc((x0, y0, x0+2*radius, y0+2*radius), 180, 270, fill=fill, width=width)
    draw.arc((x1-2*radius, y0, x1, y0+2*radius), 270, 360, fill=fill, width=width)
    draw.arc((x0, y1-2*radius, x0+2*radius, y1), 90, 180, fill=fill, width=width)
    draw.arc((x1-2*radius, y1-2*radius, x1, y1), 0, 90, fill=fill, width=width)
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill, width=width)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill, width=width)

def create_progress_bar(width, height, progress_percentage, bar_color=(255, 192, 203), background_color=(255, 255, 255), border_color=(0, 0, 0), border_width=2):
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (width-1, height-1)], outline=border_color, width=border_width)
    progress_width = int((width - 2 * border_width) * progress_percentage)
    draw_rounded_rectangle(draw, (0, 0, width-1, height-1), fill=background_color, outline=border_color, width=border_width)
    draw.rectangle([(border_width, border_width), (border_width + progress_width, height - border_width)], fill=bar_color)
    img_path = TEMP_IMAGES / Path("TmpProgressBar.jpg")
    img.save(TEMP_IMAGES / Path("TmpProgressBar.jpg"))

    return img_path

def get_rank_title(current_xp):
    if current_xp > 100:
        return "Godly"
    elif current_xp > 50:
        return "Superb"
    elif current_xp > 25:
        return "Outstanding"
    elif current_xp > 10:
        return "Active"
    elif current_xp > 5:
        return "Rookie"
    else:
        return "Novice"



    