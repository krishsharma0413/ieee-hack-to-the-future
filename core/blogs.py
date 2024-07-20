"""
{
    "_id": "blog ID",
    "path": "path to HTML file",
    "date": (int) epoch time,
    "img": "https:// url of image",
    "title": "title of blog",
    "description": "description of blog",
}
"""
from core.crud import blogs_collection

class Blog:
    
    @staticmethod
    async def get_all_blogs():
        return await blogs_collection.find().to_list(1000)
    
    @staticmethod
    async def get_blog_by_id(blog_id:str):
        return await blogs_collection.find_one({"_id":blog_id})
    
    @staticmethod
    async def create_blog(blog:dict):
        await blogs_collection.insert_one(blog)