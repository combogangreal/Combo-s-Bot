"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
import os
import asyncio
from discord import Intents, Activity, ActivityType
from loguru import logger
from discord.ext.commands import Bot
from cogwatch import watch
from src.base import config
from datetime import datetime

class ComboBot(Bot):
    """Main bot class"""
    def __init__(self):
        super().__init__(command_prefix="!", intents=Intents.all())
    
    async def load_cogs(self):
        """Loads all the cogs from the ./src/bot/cogs folder"""
        for filename in os.listdir("./src/bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"src.bot.cogs.{filename[:-3]}")
                logger.info(f"Loaded cog {filename[:-3]}")
                
    async def update_db(self):
        """Updates the database with all the new data"""
        for guild in self.guilds:
            for member in guild.members:
                if not config.DATABASE.find_one_document("ComboData", {"_id": member.id}):
                    config.DATABASE.insert_document("ComboData", {"_id": member.id, "username": member.name, "joined_at": member.joined_at, "verified": member.bot, "verified_at": datetime.now() if member.bot else None, "bot": member.bot, "ban_time": 0, "mute_time": 0, "blacklisted": False, "warns": {}, "punishments": {}})
                    logger.info(f"Added {member.name} to the database")
                
    async def setup_hook(self) -> None:
        """Setup hook event for the bot"""
        await self.load_cogs()
        await self.tree.sync()
        logger.info("Setup hook completed")
        
    @watch(path="src/bot/cogs")
    async def on_ready(self):
        """Bot ready event"""
        await self.update_db()
        logger.info("Database updated")
        
        for guild in self.guilds:
            for member in guild.members:
                data = config.DATABASE.find_one_document("ComboData", {"_id": member.id})
                if data["mute_time"] > 0:
                    mute_time = data["mute_time"]
                    await member.timeout(until=mute_time, reason="Muted after bot restart")
                if data["ban_time"] > 0:
                    ban_time = data["ban_time"]
                    await member.ban(reason="Banned after bot restart")    
                    asyncio.sleep(ban_time)         
                    await member.unban(reason="Unbanned after bot restart")
        
        guild = self.get_guild(id=1194856906133614643)
        activity = Activity(name=f"{guild.member_count}", type=ActivityType.watching)
        await self.change_presence(activity=activity)
        logger.info("Presence updated")
        
        self.logger.info("Bot ready")