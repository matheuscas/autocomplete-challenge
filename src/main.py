import asyncio
import uvloop
from sanic import Sanic
from sanic.response import text, json
from blueprints import db

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)
app.register_blueprint(db.bp_db)

@app.route("/")
async def index(request):
    return text('Desafio Dito')

@app.post("/navigation/info")
async def set_nav_info(request):
    await db.insert_nav_info(app, {'event': request.json['event'], 'timestamp': request.json['timestamp']})
    return json({'response': 'ok'});

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)