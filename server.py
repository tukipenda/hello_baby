from app import app, db
from models import *
from views import *
app.logger.info("Here")

if __name__ == '__main__':
    app.run()