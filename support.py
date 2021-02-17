from pymongo import MongoClient, ASCENDING, DESCENDING


def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection, elements={}, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def get_questions(collection, limit=100, offset=0, theme=None):
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
    res_list = [r for r in results]
    return res_list[offset:]


def get_question_order(collection, question):
    last_question = get_questions(collection, limit=1, theme=question['theme'])
    if len(last_question) > 0:
        return last_question[0]['order'] + 1
    else:
        return 1