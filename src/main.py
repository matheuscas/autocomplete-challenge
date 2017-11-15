import asyncio
import uvloop
from sanic import Sanic
from sanic.response import text

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)

@app.route("/")
async def test(request):
    return text('Desafio Dito')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)