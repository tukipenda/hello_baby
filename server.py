import os
from werkzeug.wsgi import SharedDataMiddleware
from hello_baby import app


application = SharedDataMiddleware(app, {
    '/static': os.path.join(os.path.dirname(__file__), 'static')
})
