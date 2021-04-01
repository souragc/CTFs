from app import db, app
from routes import routes

db.create_all()
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
