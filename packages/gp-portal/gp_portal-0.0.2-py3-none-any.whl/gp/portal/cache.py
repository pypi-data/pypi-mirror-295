from flask_caching import Cache

cache = Cache()

def init_app(app, config):
    cache.init_app(app, config)