import asyncio
import uvloop
from sanic import Sanic
from sanic import response
from sanic.response import text, json
from sanic.exceptions import ServerError
from blueprints import db

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)
app.register_blueprint(db.bp_db)
app.static('/styles.css', './public/static/styles.css');

@app.route("/")
async def index(request):
    return await response.file('public/index.html')

@app.post("/event")
async def set_nav_info(request):
    try:
        payload = {'event': request.json['event'], 'timestamp': request.json['timestamp']}
        await db.insert_nav_info(app, payload)
        return json({'response': 'ok'});
    except KeyError as error:
        raise ServerError(str(error), status_code=404)

@app.get("/events/search")
async def search_events(request):
    cursor = app.config.db.events.find({ 'event': {"$regex": request.args['term'][0], '$options': 'i'} })
    results = []
    for document in await cursor.to_list(length=10):
        results.append(document['event'])
    return json(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)