from Models import User
from Models import db
from app import app
from exceptions.UserExceptions import CreateUserExcepiton
import os
class UserService():

    __mandatory_fields = ["username","password","last_name","first_name","mobile_number"]


    def get_temp_folder_from_user(self,username):
        user = User.query.filter(User.username == username).first()
        if user is not None:
            return user.temp_folder

    def get_music_folder_from_user(self,username):
        user = User.query.filter(User.username == username).first()
        if user is not None:
            return user.music_folder
        
    def get_username_info(self,username):
        user = User.query.filter(User.username == username).first()
        return user.to_dict()

    def create_user(self,**kwargs):
        try:
            
            kwargs["temp_folder"] = app.config["MUSIC_FOLDER"] + "/" + kwargs["username"] + "/temp"
            kwargs["music_folder"] = app.config["MUSIC_FOLDER"] + "/" + kwargs["username"]

            new_user = User(**kwargs)
            exist_folder = self.__user_music_folder_exist(new_user.username)
            if(not exist_folder):
                self.__create_user_folder(new_user.username)
            
            exist_temp = self.__user_music_temp_folder_exist(new_user.username)
            if(not exist_temp):
                self.__create_temp_user_folder(new_user.username)
           
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            app.logger.error("Error trying to create an user: " , e)
            db.session.rollback()
            raise CreateUserExcepiton("Problems creating user")
    
    def check_user_properties(self,user_dict_repr):
        for field in self.__mandatory_fields:
            
            if field not in user_dict_repr or user_dict_repr[field] is None or user_dict_repr[field] == '':
                return False

        return True
        
    def __create_user_folder(self,username):
        os.makedirs(app.config["MUSIC_FOLDER"] + "/" + username)

    

    def __user_music_folder_exist(self,username):
        if os.path.exists(app.config["MUSIC_FOLDER"] + "/" + username):
            return True
        else:
            return False


    def __create_temp_user_folder(self,username):
        os.makedirs(app.config["MUSIC_FOLDER"] + "/" + username + "/temp")

    def __user_music_temp_folder_exist(self,username):
        if os.path.exists(app.config["MUSIC_FOLDER"] + "/" + username + "/temp"):
            return True
        else:
            return False
