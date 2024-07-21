"""
{
    "_id": "random generated ID",
    "productname": "Name of the Product",
    "productdescription": "Description of the Product",
    "productprice": (int) Price of the Product,
    "productimage": "Image URL of the Product",
}
"""
from core.crud import marketplace_collection, cart_collection
from secrets import token_urlsafe

class Marketplace:
    def __init__(self, productid:str):
        self.productid = productid

    
    async def get_product(self)-> dict:
        data = await marketplace_collection.find_one({"_id":self.productid})
        return data
    
    @staticmethod
    async def get_all_products()-> list:
        data = []
        async for document in marketplace_collection.find():
            data.append(document)
        return data

    @staticmethod
    async def add_product(productname:str, productdescription:str, productprice:int, productimage:str)-> dict:
        data = {
            "_id": f"PRODUCT-{token_urlsafe(16)}",
            "productname": productname,
            "productdescription": productdescription,
            "productprice": int(productprice),
            "productimage": productimage
        }
        await marketplace_collection.insert_one(data)
        return data

    async def delete_product(self)-> dict:
        data = await marketplace_collection.find_one_and_delete({"_id":self.productid})
        return data
    
    @staticmethod
    async def update_product(productid:str, *, args)-> dict:
        data = await marketplace_collection.find_one_and_update({"_id":productid}, {"$set":args})
        return data

    @staticmethod
    async def search_product(productname:str)-> list:
        data = []
        async for document in marketplace_collection.find({"productname":productname}):
            data.append(document)
        return data
    
    @staticmethod
    async def add_to_cart(productid:str, token:str)-> dict:
        data = await marketplace_collection.find_one({"_id":productid})
        await cart_collection.insert_one({
            "user": token,
            "product": data
        })
        return data
    
    @staticmethod
    async def get_cart(token:str)-> list:
        data = []
        async for document in cart_collection.find({"user":token}):
            data.append(document)
        return data
    
    @staticmethod
    async def buynow(token:str):
        await cart_collection.delete_many({"user":token})
            