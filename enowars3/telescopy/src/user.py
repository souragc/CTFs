from app import db
from sqlalchemy import Column, String


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username,password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }

