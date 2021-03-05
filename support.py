from pymongo import DESCENDING
import motor.motor_asyncio

#for debugging purposes
from connection_to_vk import api
import random

mongo_collection = motor.motor_asyncio.AsyncIOMotorCollection


async def insert_document(collection: mongo_collection, data: dict) -> str:
    """ Function to insert a document into a collection and
    return the document's id.
    """
    result = await collection.insert_one(data)
    return result.inserted_id


async def find_document(collection: mongo_collection, elements: dict={}, multiple: bool=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r async for r in results]
    else:
        return await collection.find_one(elements)


async def get_questions(collection: mongo_collection, limit: int=100, offset: int=0, theme: str=None) -> list:
    if theme:
        results = collection.find({"$and": [{"text": {'$exists': True}},
                                            {"theme": theme}]},
                                  {"_id" : False}
                                  ).sort('order', DESCENDING
                                         ).limit(limit).skip(offset)
    else:
        results = collection.find({"text": {'$exists': True}}
                                  ).sort([('theme', DESCENDING), ('order', DESCENDING)]
                                         ).limit(limit).skip(offset)
    res_list = [r async for r in results]
    return res_list


async def get_themes(collection, limit=100, offset=0):
    result = await collection.distinct('theme')
    last = offset+limit if offset+limit < len(result) else len(result)
    return result[offset:last]


async def get_question_order(collection, question):
    last_question = await get_questions(collection, limit=1, theme=question['theme'])
    last_question = list(last_question)
    if len(last_question) > 0:
        return last_question[0]['order'] + 1
    else:
        return 1


async def get_game_order(collection, group_id):
    group_games = await collection.count_documents({'group_id' : group_id})
    return group_games + 1


async def get_played_themes(collection, group_id):
    result = collection.find({'group_id': group_id,
                              'game_finished': True}).distinct('theme')
#                             {'theme': True})
    api.messages.send(peer_id=group_id, random_id=random.getrandbits(64),
                      message=str(result))
#    return [r async for r in result]
    return result

# Not needed yet
async def find_game(collection, id):
    result = collection.find({'$and': [{'group_id': id},
                                       {'game_finished': False}]})
    return [r async for r in result]

def gen_question_id(theme, ind=1):
    return theme + str(ind)

def gen_game_id(group_id, ind):
    game_id = str(group_id)+'-'+str(ind)
    return game_id