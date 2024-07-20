from typing import Union

import motor.motor_asyncio
from dotenv import dotenv_values
from hashlib import sha256

config = dotenv_values("config.env")
client = motor.motor_asyncio.AsyncIOMotorClient(config["mongo_url"])
db = client["ieee-httf"]
users_collection = db["users"]
forums_collection = db["forums"]
blogs_collection = db["blogs"]
replies_collection = db["replies"]
marketplace_collection = db["marketplace"]

async def validate_login(email:str, password:str)-> Union[bool, str]:
    """
    to bypass login page and get token, this is required.
    
    Returns
    -------
    - returns `False` if the email and password is not found in database.
    - returns `str` containing the token for this email & password.
    """
    print(email, password, sha256(password.encode("utf-8")).hexdigest())
    data = await users_collection.find_one({"_id":email.lower(), "password":sha256(password.encode("utf-8")).hexdigest()})
    if data:
        return data["token"]
    else:
        return False
