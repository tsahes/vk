from aiohttp import web
from routes import setup_routes
import os


#APP
app = web.Application()

def setup_app(application: web.Application) -> None:
    setup_routes(application)


if __name__ == '__main__':
    setup_app(app)
    web.run_app(app, port=int(os.environ.get("PORT", 5000)), host='127.0.0.1')
