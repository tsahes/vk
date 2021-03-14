from aiohttp import web
from routes import setup_routes
import os


#APP
#app = web.Application()

def setup_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    return app


if __name__ == '__main__':
    app = setup_app()
    web.run_app(app, port=int(os.environ.get("PORT", 5000)))
