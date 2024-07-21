"""
author: krishsharma0413

Create Token class for most authentication uses.
"""

from core.crud import users_collection, consumption_collection
from async_lru import alru_cache
from hashlib import sha256
from random import randint
from secrets import token_urlsafe


@alru_cache
async def fitcheck(token):
    data = await users_collection.find_one({"token": token})
    return data

class Token():
    """
    Fancy Class to get all information about the given token.
    """
    def __init__(self, token:str):
        self.token = token
        self.username = None
        self.avatar = None
        self.password = None
        self.email = None
        self.fullname = None
        self.authentication = False
        
    async def fit(self)->None:
        """
        Retrieve all the information about the token and save it within the class.
        """
        data = await fitcheck(self.token)
        if data:
            self.username = data["username"]
            self.password = data["password"]
            self.fullname = data["fullname"]
            self.email = data["_id"]
            self.avatar = data["avatar"]
            self.authentication = True

    async def change_avatar(self, avatar_url:str):
        """
        Change avatar for this token.
        """
        await users_collection.find_one_and_update({"token": self.token}, {"$set": {"avatar": avatar_url}})
        return True
    
    async def change_password(self, password:str):
        """
        Change password for this token.
        """
        await users_collection.find_one_and_update({"token": self.token}, {"$set": {"password": sha256(password.encode('utf-8')).hexdigest()}})
        return True

    @staticmethod
    async def add_user(
        fullname:str,
        email:str,
        password:str,
    ) -> bool:
        """
        Add user to the database.
                
        Parameters
        ----------
        - `name` (str): Name of the user.
        - `email` (str): email ID of the user.
        - `password` (str): password set by user.
        
        Returns
        -------
        - returns `False` if emailID already exists in database.
        - returns `True` after account generation.
        """
        exists = await users_collection.find_one({"_id": email.lower()})
        if exists:
            return False
        else:            
            token = token_urlsafe(16)
            await users_collection.insert_one({
                "_id": email.lower(),
                "token": token,
                "username": f"GREENVOLT-USER-{randint(10,10000)}-{token_urlsafe(4)}",
                "password": sha256(password.encode('utf-8')).hexdigest(),
                "fullname": fullname,
                "avatar": "/static/avatar/avatar.jpg"
            })
            
            await consumption_collection.insert_one({
                "_id": email.lower(),
                "coins": 0,
                "months": [0,0,0,0,0,0],
                "last_claim": None
            })
            
            return token

    @staticmethod
    async def get_username(username:str):
        data = await users_collection.find_one({
            "username": username
        })
        
        return data
    
    @staticmethod
    async def get_email(email:str):
        data = await users_collection.find_one({
            "_id": email
        })
        
        return data