import discord
import kiri_storage
import KiriLevel
import kiri_osu
import disputils
from discord.ext.commands.core import command
from discord.ext import commands
import sympy as sym


settings = {
    "save_location": ".",
    "api_key": "529892067590275104",
    "secret_key": "NTI5ODkyMDY3NTkwMjc1MTA0.GeU1kn._81IeccD-_9FCzGf-GYV4j1bcmOnGx00YG8P4Q",
    "bot_presence": "Kiriuwu >.<",
    "prefix": ">"
}


osu_client = {
    "oath_code": "gkK6SDfwopiUsVcIHj2Lu5p2EA15gdLnQBRwo5kL",
    "client_id": "21288"
}

#DO NOT TOUCH ANYTHING BELOW THIS POINT

class customembed:

    @staticmethod
    def osu_embed(player: str, osu_data_plays: list) -> list:
        
        list_of_embeds = []
        total_length = len(osu_data_plays)

        for play in range(len(osu_data_plays)):
            
            custom_embed = discord.Embed(title=f"Top OSU! plays ({player}):\n", color=0xfb86d7)
        
            for counter, play_count in enumerate(range(total_length)):
                play = osu_data_plays[play_count]
                custom_embed.add_field(name=f"{play.beatmap_name} ({play.beatmap_version}) - {play.difficulty} ★", value=f"{round(float(play.pp))}pp/ {play.accuracy}%", inline=False)

                if counter == 10:
                    total_length = play_count + 10
                    list_of_embeds.append(custom_embed)
                    break
        
        print(list_of_embeds)
        print("DONE")
        return list_of_embeds
    

    @staticmethod
    def osu_embed_test(player: str, osu_data_plays: list) -> list:
        

        total_length = len(osu_data_plays)

        custom_embed = discord.Embed(title=f"Top OSU! plays ({player}):\n", color=0xfb86d7)

        for play in range(len(osu_data_plays)):
            play = osu_data_plays[play]
            custom_embed.add_field(name=f"{play.beatmap_name} ({play.beatmap_version}) - {play.difficulty} ★", value=f"{play.rank}: {float(play.pp)} pp/ {float(play.accuracy) * 100:.2f}%", inline=False)
        
        return custom_embed


class MessageHandler:

    @staticmethod
    def bot_response(message, prefix: str, KiriSave: kiri_storage.KiriSave) -> str and bool:

        if message.content == prefix + "stats":
            return f"Here are the amount of messages you have sent {str(KiriSave.get_data(str(message.author.id)))}", False
        elif message.content == prefix + "version":
            return "Kiribot is currently running on 1.1 beta", False
        elif message.content == prefix + "updates":
            return "recently added chathooks", False
        elif message.content == prefix + "info":
            return str(message), False
        elif message.content == prefix + "me":
            user_data = KiriSave.get_data(str(message.author.id))
            return f"Here are your current stats ({message.author.name}):\n" + \
                   f"Rank: {str(KiriLevel.xp_converter.convert_rank(user_data))}\n" + \
                   f"Level: {str(KiriLevel.xp_converter.convert_level(user_data).level)}\n" + \
                   f"XP: {str(KiriLevel.xp_converter.convert_level(user_data).total_xp)}\n" + \
                   f"Until Next Level: {str(100 - int(KiriLevel.xp_converter.convert_level(user_data).remain_xp))}\n" + \
                   f"Talk more to earn more xp >.<\n", False

        elif message.content == prefix + "help":
            return f"Here are a list of currently supported commands:\n" + \
                   f"{prefix}stats - gets the stats\n" + \
                   f"{prefix}version - gets the version of the bot\n" + \
                   f"{prefix}updates - gets the last updates of the bot\n" + \
                   f"{prefix}info - for debugging purposes\n" + \
                   f"{prefix}me - get own data (it is saved on the server)\n" + \
                   f"> More commands are supported in the future.", False

        elif str(message.content).find(prefix + "osu_top_plays") != -1:
            try:
                print("RAN")
                player_name = str(message.content)[str(message.content).find(" ") + 1:].strip()
                osu_data = kiri_osu.OsuData(osu_client["oath_code"], osu_client["client_id"])
                osu_data_plays = osu_data.get_user_plays(player_name, limit=10, type="best")
                if osu_data and osu_data_plays:
                    return customembed.osu_embed_test(str(player_name), osu_data_plays), True
                else:
                    return "Invalid User", False
            except (IndexError) as error:
                print("KiriBot found error in finding name: " + str(error))
                return None, None

        return None, None


class KiriBot:

    bot = commands.Bot(command_prefix=settings["prefix"], intents=discord.Intents.all())
    KiriSave = None

    def __init__(self, settings):
        KiriBot.KiriSave = kiri_storage.KiriSave(settings["save_location"], settings["api_key"], settings["secret_key"])
        print("Successfully Set Up KiriBot")
        print(settings["prefix"])
        KiriBot.bot.run(settings["secret_key"])

    @bot.event
    async def on_ready():
        activity = discord.Game(name=settings["bot_presence"], type=3)
        await KiriBot.bot.change_presence(status=discord.Status.idle, activity=activity)
        print(f'[KiriBot] Connected!')
     
    @bot.command(name='ping', aliases=["PING", "secret:3"])
    async def ping(ctx):
        print("pinged")
        await ctx.send('pong')

    @bot.command(name="add", aliases=["ashkutalbraincells"])
    async def add(ctx, int_one, int_two):
        try:
            result = int(int_one) + int(int_two)
            await ctx.send(result)
        except ValueError as error:
            print(f"error: {error}")
            await ctx.send("Invalid Parameters :3")
    
    @bot.command(name="differentiate", aliases=["okboomer"])
    async def differentiate(ctx, *, message):

        equation = message
        equation = equation.replace("^", "**")
        new_equation = equation[:equation.find(" with respect to")].strip()
        respect_to = equation.strip()[-1:]
        print("with respect to", respect_to)
        print("equation", new_equation)
        alphabets = " ".join([i for i in new_equation if i.isalpha()])
        stralpha = f"{','.join([i for i in new_equation if i.isalpha()])}=sym.symbols('{alphabets}')"
        stralpha3 = f"derivative_result = sym.diff(new_equation, {respect_to})"
        print(stralpha)
        print(stralpha3)

        exec(stralpha)
        exec(stralpha3)
        await ctx.send(str(locals()["derivative_result"]).replace("**", "^"))

    @bot.event
    async def on_message(message):

        if message.author.id == KiriBot.bot.user.id:
            return

        print(f"[{message.author.name}#{message.author.discriminator}]: {message.content}")
        response, is_embed = MessageHandler.bot_response(message, settings["prefix"], KiriSave=KiriBot.KiriSave)
        KiriBot.KiriSave.update_data(str(message.author.id))

        if response and is_embed:

            if isinstance(response, list):
                print("IS PAG")
                paginator = disputils.BotEmbedPaginator(message, response)
                await paginator.run()
            else:
                print("IS NOT PAG")
                await message.channel.send(embed=response)

        elif response:
            await message.channel.send(response)
        
        await KiriBot.bot.process_commands(message)


if __name__ == "__main__":

    intents = discord.Intents.all()

    print("\n----------KiriBot----------\n")
    print("Here are your current Settings:\n")
    for setting in settings.items():
        print(f"[KiriBot Config] {setting[0]}: {setting[1]}\n")
    print("----------KiriBot----------\n")

    #Runs the Bot
    KiriBot(settings)
