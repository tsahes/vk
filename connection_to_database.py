import motor.motor_asyncio
import os

MONGODB_URL = os.environ.get('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.vk_game

questions_table = db.questions
games_table = db.games
