from app import app
from app import db
from Models import *
from routes import routes
from app import migrate

app = app

db.create_all()
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run("0.0.0.0",2060,debug=False,threaded=True)
