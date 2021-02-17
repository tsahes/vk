from aiohttp import web
from routs import setup_routs


#APP
app = web.Application()

def setup_app(application: web.Application) -> None:
    setup_routs(application)


if __name__ == '__main__':
    setup_app(app)
    web.run_app(app)
