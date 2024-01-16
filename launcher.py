"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
import asyncio
from src.bot import bot
from src.base import config

c_bot = bot.ComboBot()

asyncio.run(c_bot.start(token=config.TOKEN, reconnect=True))