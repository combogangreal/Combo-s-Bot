"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
from discord.ext.commands import Cog
from discord.ui import View, button, Button
from discord import Embed, app_commands, Interaction, ButtonStyle, utils
from datetime import datetime

from src.bot.bot import ComboBot
from src.bot import check
from src.base import config

class VerifyButton(View):
    """Verify button"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Verify", custom_id="verify_button",style=ButtonStyle.green, emoji="✅")
    async def verify_button(self, interaction: Interaction, button: Button):
        if not check.is_verified(interaction.user.id):
            config.DATABASE.find_document_and_update("ComboData", {"_id": interaction.user.id}, {"verified": True, "verified_at": datetime.now()})
            role = interaction.guild.get_role(1194857675025027112)
            await interaction.user.add_roles(role, reason="Verified")
            embed = Embed(title="Verified", description=f"You have been successfully been verified in Combo's Services")
            embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.send("You are already verified")
            await interaction.response.defer()
            return

class Verification(Cog):
    """Verification cog"""
    def __init__(self, bot: ComboBot):
        self.bot = bot
        
    @app_commands.command(name="sendverify", description="Sends the verify embed to the channel")
    async def sendverify(self, ctx: Interaction):
        """Sends the verify embed to the channel"""
        embed = Embed(title="Verify", description="Click the button below to verify yourself", color=0x00ff00)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.response.send_message(embed=embed, view=VerifyButton())
        
async def setup(bot: ComboBot):
    """Setup function for the cog"""
    await bot.add_cog(Verification(bot))