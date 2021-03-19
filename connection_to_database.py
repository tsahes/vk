import motor.motor_asyncio
import os

MONGODB_URL = os.environ.get('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.vk_game

test = os.environ.get('TEST')
if test == '0':
    questions_table = db.questions
    games_table = db.games
elif test == '1':
    questions_table = db.test_questions
    games_table = db.test_games
