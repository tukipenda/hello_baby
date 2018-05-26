import os
from werkzeug.wsgi import SharedDataMiddleware
from hello_baby import app


application = SharedDataMiddleware(app, {
    '/static': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0')