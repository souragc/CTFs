from Models import User
from flask import session
from exceptions.LoginExceptions import UserNotFoundException
from app import app
import os
class LoginService():

    __mandatory_fields=["username","password"]
    
    def login_user(self,user,password):
        user_db = User.query.filter(User.username==user)\
            .filter(User.password == password)\
            .first()


        
        if user_db is None:
            app.logger.error("User was not found in the DB")
            raise UserNotFoundException()
        session["logged_in"] = True
        session["user"] = user


    def check_login_properties(self,login_properties):
        for field in self.__mandatory_fields:
            if field not in login_properties or login_properties[field] == '' or login_properties[field] == None:
                return False
        return True

    

