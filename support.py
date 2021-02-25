from pymongo import DESCENDING


async def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return await collection.insert_one(data).inserted_id


async def find_document(collection, elements={}, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r async for r in results]
    else:
        return await collection.find_one(elements)


async def get_questions(collection, limit=100, offset=0, theme=None):
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
    last = offset+limit if offset+limit < len(result) else -1
    return result[offset:last]


async def get_question_order(collection, question):
    last_question = await get_questions(collection, limit=1, theme=question['theme'])
    if len(last_question) > 0:
        return last_question[0]['order'] + 1
    else:
        return 1


async def get_game_order(collection, game):
    group_games = await collection.count_documents({'group_id' : game['group_id']})
    return group_games + 1


async def get_played_themes(collection, id):
    result = collection.find({'$and': {'group_id': id,
                                        'game_finished': True}},
                             {'theme': {'$exists': True}})
    return [r async for r in result]


# Not needed yet
async def find_game(collection, id):
    result = collection.find({'$and': [{'group_id': id},
                                       {'game_finished': False}]})
    return [r async for r in result]

def gen_question_id(theme, ind=1):
    return theme + str(ind)