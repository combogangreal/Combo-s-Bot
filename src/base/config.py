"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
import json
from src.base import database
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_token() -> str:
    """Gets the bot token from the router path in router.json file
    
    Returns
    ---------
    @returns str: The bot token.
    """
    with open("./src/base/router.json", "r") as file:
        json_data = json.load(file)
        token_path = json_data["token"]
        with open(token_path, "r") as file:
            token = file.read()
            return token

def get_mongo_key_path() -> str:
    """Gets the mongo key path from the router path in router.json file
    
    Returns
    ---------
    @returns str: The mongo key path.
    
    """
    with open("./src/base/router.json", "r") as file:
        json_data = json.load(file)
        mongo_path = json_data["mongo-key"]
        return mongo_path
    
def get_mongo_uri() -> str:
    """Gets the mongo uri from the router path in router.json file

    Returns
    ---------
    @returns str: The mongo uri.

    """
    with open("./src/base/router.json", "r") as file:
        json_data = json.load(file)
        mongo_path = json_data["mongo-uri"]
        with open(mongo_path, "r") as file:
            mongo_uri = file.read()
            return mongo_uri
        
CLIENT = MongoClient(get_mongo_uri(), tls=True, tlsCertificateKeyFile=get_mongo_key_path(), server_api=ServerApi('1'))
DATABASE = database.MongoDBUtility(CLIENT, "CombosBot")
TOKEN = get_token()