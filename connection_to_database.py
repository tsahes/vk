from pymongo import MongoClient, DESCENDING
from creds import MONGODB_URL


client = MongoClient(MONGODB_URL)
db=client.vk_game
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)
questions_table = db.questions
games_table = db.games
