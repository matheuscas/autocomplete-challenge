from sanic.response import json
from sanic import Blueprint
from motor.motor_asyncio import AsyncIOMotorClient

bp_db = Blueprint('db')

@bp_db.listener('before_server_start')
async def register_db(app, loop):
    mongo_client = AsyncIOMotorClient('localhost', 27017)
    app.config.db = mongo_client['desafio_dito']
    app.config.mongo = mongo_client
    app.config.db.events.create_index([('event', 'text')]);

@bp_db.listener('after_server_stop')
async def close_db(app, loop):
    app.config.mongo.close()

async def insert_nav_info(app, info):
    return app.config.db.nav_info.insert_one(info);
