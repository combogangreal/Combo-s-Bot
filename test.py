"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
from src.base import config

query = config.DATABASE.find_one_document("ComboData", {"_id": 912775780730294292})
print(query["verified"])