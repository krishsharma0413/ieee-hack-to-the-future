"""
{
    "_id": "random generated ID",
    "productname": "Name of the Product",
    "productdescription": "Description of the Product",
    "productprice": (int) Price of the Product,
    "productimage": "Image URL of the Product",
}
"""
from core.crud import marketplace_collection
from secrets import token_urlsafe

class Marketplace:
    def __init__(self, productid:str):
        self.productid = productid.lower()

    
    async def get_product(self)-> dict:
        data = await marketplace_collection.find_one({"_id":self.productid})
        return data
    
    async def get_all_products(self)-> list:
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
