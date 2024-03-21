#enable mod privilege check in configuration.ini
import discord.utils
import configparser
from . import MongoDB
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path(".").parent / Path("configuration.ini"))
DATASAVE = config.get('MongoDB - localBot', 'Link')
DATABASE = config.get('MongoDB - localBot', 'Database')
COLLECTION = config.get('MongoDB - localBot', 'Collection')
ADMIN_MANAGE_ENABLED = bool(config.get('MongoDB - localBot', 'Enabled'))

class AdminManager:

    mongoDB = MongoDB(DATASAVE, DATABASE, COLLECTION)
    
    @staticmethod
    def getAdmins():
        admin_list = []
        results = AdminManager.mongoDB.retreive_all_data()
        for admin in results:
            admin_list.append(admin['user_id'])
        
        return admin_list
        
    @staticmethod
    def addAdmin(admin_id):
        cur_admins = AdminManager.getAdmins()
        if admin_id not in cur_admins:
            AdminManager.mongoDB.save_data({'user_id': admin_id})
            return f"Admin {admin_id} is successfully added."
        else:
            return f"Admin {admin_id} is already an admin."
    
    @staticmethod
    def removeAdmin(admin_id):
        cur_admins = AdminManager.getAdmins()
        if admin_id in cur_admins:
            AdminManager.mongoDB.delete_query(str(admin_id))
            return f"Admin {admin_id} is successfully removed."
        else:
            return f"Admin {admin_id} is not an admin."
    
    @staticmethod
    def resetAdmin():
        AdminManager.mongoDB.remove_collection()

class AdminCommands:

    def __init__(self):
        self.enabled = ADMIN_MANAGE_ENABLED

    async def mute_user(self, discord_interaction, admin_user, mute_user, reason):

        if str(admin_user) in AdminManager.getAdmins():
        
            guild = discord_interaction.guild
            mute_user = guild.get_member(int(mute_user))
            role = discord.utils.get(guild.roles, name="muted")
            
            if role is None:
                guild = discord_interaction.guild
                await guild.create_role(name="muted")
                await role.edit(position=2)
                for channel in discord_interaction.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        await channel.set_permissions(role, send_messages=False)
            
                print("Successfully created muted role.")

            role = discord.utils.get(mute_user.roles, name="muted")
            add_role = discord.utils.get(guild.roles, name="muted")

            await mute_user.add_roles(add_role, reason=reason)
            return f"The {mute_user} has successfully been muted."
        else:
            return f"Not an administrator."
    
    async def unmute_user(self, discord_interaction, admin_user, mute_user, reason=None):

        if str(admin_user) in AdminManager.getAdmins():
        
            guild = discord_interaction.guild
            mute_user = guild.get_member(int(mute_user))
            role = discord.utils.get(guild.roles, name="muted")
            
            if role is None:
                guild = discord_interaction.guild
                await guild.create_role(name="muted")
                role = discord.utils.get(guild.roles, name="muted")
                await role.edit(position=2)
                for channel in discord_interaction.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        await channel.set_permissions(role, send_messages=False)
            
                print("Successfully created muted role.")

            role = discord.utils.get(mute_user.roles, name="muted")
            remove_role = discord.utils.get(guild.roles, name="muted")

            await mute_user.remove_roles(remove_role, reason=reason)
            return f"The {mute_user} has successfully been unmuted."
        else:
            return f"Not an administrator."

    def kick_user(self, ctx, admin_user, kick_user):
        pass

    def kick_voice_chat():
        pass

    def give_user_role(self, ctx, admin_user, give_user_id):
        pass

    def remove_user_role(self, ctx, admin_user, remove_user_id):
        pass

    def user_id_of():
        pass