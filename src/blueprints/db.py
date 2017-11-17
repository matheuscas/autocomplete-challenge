from sanic.response import json
from sanic import Blueprint
from motor.motor_asyncio import AsyncIOMotorClient
import blueprints.load_words as load_words
import datetime

bp_db = Blueprint('db')

@bp_db.listener('before_server_start')
async def register_db(app, loop):
    mongo_client = AsyncIOMotorClient('localhost', 27017)
    app.config.db = mongo_client['desafio_dito']
    app.config.mongo = mongo_client
    await populateEvents(app)
    app.config.db.events.create_index([('event', 'text')])

@bp_db.listener('after_server_stop')
async def close_db(app, loop):
    app.config.mongo.close()

async def insert_nav_info(app, info):
    return app.config.db.nav_info.insert_one(info);

async def populateEvents(app):
    words = load_words.load_words()
    events = []
    for word in words:
        events.append({
            'event': word,
            'timestamp': datetime.datetime.now().isoformat().strip()
        })
    await app.config.db.events.drop()
    app.config.db.events.insert(events)
