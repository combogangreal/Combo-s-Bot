"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
from src.base import config

def is_verified(user: int) -> bool:
    """Checks if the user is verified
    
    Arguments
    ---------
    user (int): The user ID
    
    Returns
    -------
    bool: True if the user is verified, False otherwise
    
    """
    query = config.DATABASE.find_one_document("ComboData", {"_id": user})
    return query["verified"]