"""
{
    "_id": "user email ID",
    "coins": (int) 0,
    "months":[
        (int),
        (int),
        (int),
        (int),
    ]
}
"""
from core.crud import consumption_collection, users_collection

class Coins:
    
    def __init__(self, email) -> None:
        self.email = email
        
    async def get_coins(self) -> int:
        data = await consumption_collection.find_one({"_id":self.email})
        return data["coins"]
    
    async def get_months(self) -> list:
        data = await consumption_collection.find_one({"_id":self.email})
        return data["months"]
    
    async def add_coins(self, coins:int) -> None:
        await consumption_collection.update_one({"_id":self.email}, {"$inc":{"coins":coins}})
        
    async def add_months(self, months:int) -> None:
        await consumption_collection.update_one({"_id":self.email}, {"$push":{"months":months}})
        
    async def remove_coins(self, coins:int) -> None:
        await consumption_collection.update_one({"_id":self.email}, {"$inc":{"coins":-coins}})
        
    async def get_average(self) -> float:
        data = await consumption_collection.find_one({"_id":self.email})
        # get average of months for the last 6 months
        return sum(data["months"][-6:])/6
    
    async def get_last_claim(self) -> str:
        data = await consumption_collection.find_one({"_id":self.email})
        return data["last_claim"]
    
    async def get_leaderboard(self) -> list:
        data = consumption_collection.find()
        ret = []
        async for x in data:
            x['name'] = (await users_collection.find_one({"_id":x["_id"]}))["fullname"]
            x['avg'] = sum(x["months"][-6:])//6
            if x['avg'] == 0:
                continue
            ret.append(x)
        return sorted(ret, key=lambda x:x['avg'])