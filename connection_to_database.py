from pymongo import MongoClient, DESCENDING
import motor.motor_asyncio
#from motor import MotorClient
from creds import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
#client = MongoClient(MONGODB_URL)
db = client.vk_game
# Issue the serverStatus command and print the results
#serverStatusResult = await db.command("serverStatus")
#pprint(serverStatusResult)
questions_table = db.questions
games_table = db.games
