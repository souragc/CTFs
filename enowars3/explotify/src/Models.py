from app import db

class Song(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title =  db.Column(db.String)
    length = db.Column(db.String)
    artist = db.Column(db.String)
    disk_number = db.Column(db.Integer)
    lyrics = db.Column(db.String)
    path_song = db.Column(db.String)


    def __init__(self,**kwargs):
        if "path_song" in kwargs:
            del kwargs["path_song"]
        super(Song, self).__init__(**kwargs)

        

    def to_dict(self):
        return {
            "title":self.title,
            "length":self.length,
            "artist":self.artist,
            "disk_number":self.disk_number,
            "lyrics":self.lyrics
        }


class User(db.Model):

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String,unique=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    mobile_number = db.Column(db.Integer)
    temp_folder = db.Column(db.String)
    music_folder = db.Column(db.String)
    


    def to_dict(self):
        return {
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "mobile_number":self.mobile_number,
            "temp_folder":self.temp_folder,
            "music_folder":self.music_folder
        }
