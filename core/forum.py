"""
forum_collection = {
    "_id": "random forum ID",
    "author": "author email",
    "date": (int) epoch time,
    "title": "title of blog",
    "name": "author name",
    "description": "description of blog",
}

replies_collection = {
    "_id": "random reply ID",
    "forum_id": "forum ID",
    "author": "author email",
    "date": (int) epoch time,
    "reply": "reply content"
}
"""
from core.crud import forums_collection, replies_collection
from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')

class Forum:
    @staticmethod
    async def get_all_forums():
        forums = []
        async for forum in forums_collection.find():
            forums.append(forum)
            forum["count"] = await Forum.get_forum_replies_count(forum["_id"])
        forums = sorted(forums, key=lambda x:x["date"], reverse=True)
        
        return forums

    @staticmethod
    async def get_forum_by_id(forum_id):
        forum = await forums_collection.find_one({"_id": forum_id})
        return forum

    @staticmethod
    async def get_replies_by_forum_id(forum_id):
        replies = []
        async for reply in replies_collection.find({"forum_id": forum_id}):
            replies.append(reply)
        replies = sorted(replies, key=lambda x:x["date"], reverse=True)
        return replies

    @staticmethod
    async def create_forum(author, name, title, description):
        ex = int(datetime.now(ist).timestamp())
        forum = {
            "_id": f"POST-{ex}",
            "author": author,
            "name": name,
            "date": ex,
            "title": title,
            "description": description
        }
        await forums_collection.insert_one(forum)
        return forum

    @staticmethod
    async def create_reply(forum_id, author, reply):
        ex = int(datetime.now(ist).timestamp())
        reply = {
            "_id": f"REPLY-{ex}",
            "forum_id": forum_id,
            "author": author,
            "date": ex,
            "reply": reply
        }
        await replies_collection.insert_one(reply)
        return reply

    @staticmethod
    async def get_forum_replies_count(forum_id):
        count = await replies_collection.count_documents({"forum_id": forum_id})
        return count
    
    
    