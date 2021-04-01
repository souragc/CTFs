from app import db


class Planet(db.Model):
    id = db.Column('dateaseId', db.Integer, primary_key=True)
    planetId = db.Column(db.String(100))
    name = db.Column(db.String(100))
    declination = db.Column(db.String(100))
    rightAscension = db.Column(db.String(100))
    location = db.Column(db.String(100))
    flag = db.Column(db.String(100))

    def __init__(self, name, declination, right_ascension, flag=""):
        self.name = name
        self.declination = declination
        self.rightAscension = right_ascension
        self.flag = flag

    def to_dict(self):
        return {
            "planetId": self.planetId,
            "name": self.name,
            "declination": self.declination,
            "rightAscension": self.rightAscension,
            "location": self.location,
            "flag": self.flag
        }
