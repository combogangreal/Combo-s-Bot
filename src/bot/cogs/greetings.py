"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
import asyncio
from discord.ext.commands import Cog
from discord.ui import View, button, Button
from discord import Embed, Interaction, Member, ButtonStyle, utils

from src.bot.bot import ComboBot
from src.base import config

class NudgeButton(View):
    """Nudge button for the small welcome message
    
    Arguments
    ---------
    member (discord.Member): The member that joins
    """
    def __init__(self, member: Member):
        super().__init__(timeout=None)
        self.member = member
    
    @button(label="Nudge", custom_id="nudge_button", style=ButtonStyle.green, emoji="👆")
    async def nudge_button(self, interaction: Interaction, button: Button):
        config.DATABASE.update_document("ComboData", {"_id": interaction.user.id}, {"nudged": True})
        channel = utils.get(interaction.guild.channels, id=config.Ids.CHAT_CHANNEL_ID.value)
        await channel.send(f"{self.member.mention} was nudged by {interaction.user.mention}")
        await interaction.response.defer()
        return

def get_small_wmsg(member: Member) -> Embed:
    """Gets the small embed message for the #universal-chat channel
    
    Arguments
    ---------
    member (discord.Member): The member that has joined
    
    Returns
    -------
    Embed: The embed message to be sent
    
    """
    embed = Embed(title="Welcome", description=f"Everybody make sure to welcome, {member.mention}", color=0x00FF00)
    embed.set_thumbnail(url=member.avatar.url)
    return embed
    
def get_big_wmsg(member: Member) -> Embed:
    """Gets the big embed message for the #welcome channel
    
    Arguments
    ---------
    member (discord.Member): The member that has joined
    
    Returns
    -------
    Embed: The embed message to be sent
    
    """
    embed = Embed(title="Welcome Message", description=f"Welcome, {member.mention}, to Combo's Services where you can order many types of development projects from us. Please check out <#{config.Ids.VERIFY_CHANNEL_ID.value}> to verify, then go to <#{config.Ids.ORDER_CHANNEL_ID.value}> to purchase, or <#{config.Ids.CHAT_CHANNEL_ID.value}> to chat with everybody!", color=0x00FF00)
    embed.set_thumbnail(url=member.avatar.url)
    return embed

class Greetings(Cog):
    """Greetings cog"""
    def __init__(self, bot: ComboBot):
        self.bot = bot
    
    @Cog.listener()
    async def on_member_join(self, member: Member):
        """Calls when a member joins the server"""
        await self.bot.update_db()
        guild = utils.get(self.bot.guilds, id=config.Ids.GUILD_ID.value)
        for _member in guild.members:
            query = config.DATABASE.find_one_document("ComboData", {"_id": _member.id})
            if query["nudged"]:
                query["nudged"] = False
        role = guild.get_role(config.Ids.UNVERIFIED_ROLE_ID.value)
        await member.add_roles(role, reason="Just Joined")
        welcome_channel = guild.get_channel(config.Ids.WELCOME_CHANNEL_ID.value)
        chat_channel = guild.get_channel(config.Ids.CHAT_CHANNEL_ID.value)
        await welcome_channel.send(embed=get_big_wmsg(member))
        msg = await chat_channel.send(embed=get_small_wmsg(member), view=NudgeButton(member))
        await asyncio.sleep(30)
        await msg.edit(view=None)
            
    @Cog.listener()
    async def on_member_remove(self, member: Member):
        """Calls when a member leaves the server"""
        query = config.DATABASE.find_one_document("ComboData", {"_id": member.id})
        if query["ban_time"] is None or query["mute_time"] is None:
            config.DATABASE.delete_document("ComboData", {"_id": member.id})
        
async def setup(bot: ComboBot):
    await bot.add_cog(Greetings(bot))