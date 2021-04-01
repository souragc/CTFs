import requests
import os
from exceptions.SongsPersistanceExceptions import SongNotSaveException
from exceptions.SongsPersistanceExceptions import SongNotFoundException

class SongPersistanceService():

    def __init__(self):
        self.__db_engine_port = 80
        self.__db_location = "db_engine_explotify"
        self.__base_url = f"http://{self.__db_location}:{self.__db_engine_port}/"
        self.__song_endpoint = self.__base_url + "songs"

    def save_song(self,song_object):
        new_song = requests.post(self.__song_endpoint,song_object)
        song_added = new_song.json()
        if song_added["_status"] != "OK":
            raise SongNotSaveException()

        return song_added["_id"]


    def get_song_by_id(self,id):
        song_query = f'where={{ "_id" :  "{ id }" }}'
        song_complete_url = self.__song_endpoint + "?" + song_query
        song = requests.get(song_complete_url)
        data_song = song.json()
        
        if data_song["_meta"]["total"] == 0:
            raise SongNotFoundException(f"The song with the id: {id} was not found")
    
        song_data = data_song["_items"][0]

        return song_data

    def get_song_by_id_from_username(self,id,username):
        song_query = f'where={{ "_id" :  "{ id }" , "username": "{ username }"}}'
        song_complete_url = self.__song_endpoint + "?" + song_query
        song = requests.get(song_complete_url)
        data_song = song.json()
        
        if data_song["_meta"]["total"] == 0:
            raise SongNotFoundException(f"The user {username} doesn't have a Song with the id : {id} ")
    
        song_data = data_song["_items"][0]

        return song_data

    def get_song_by_hash_from_username(self,hash_id,username):
        song_query = f'where={{ "hash_id" :  "{ hash_id }" , "username": "{ username }"}}'
        song_complete_url = self.__song_endpoint + "?" + song_query
        song = requests.get(song_complete_url)
        data_song = song.json()
        
        if data_song["_meta"]["total"] == 0:
            raise SongNotFoundException(f"The user {username} doesn't have a Song with the hash_id : {hash_id} ")
    
        song_data = data_song["_items"][0]

        return song_data

    def get_song_by_hash(self,hash_id):
        song_query = f'where={{ "hash_id" :  "{ hash_id }"}}'
        song_complete_url = self.__song_endpoint + "?" + song_query
        song = requests.get(song_complete_url)
        data_song = song.json()
        
        if data_song["_meta"]["total"] == 0:
            raise SongNotFoundException(f"The the hash_id : {hash_id} was not found")
    
        song_data = data_song["_items"][0]

        return song_data

    def get_all_songs_by_user(self,username):
        song_query = f'where={{ "username": "{ username }"}}'
        song_complete_url = self.__song_endpoint + "?" + song_query
        song = requests.get(song_complete_url)
        data_song = song.json()
        
        if data_song["_meta"]["total"] == 0:
            raise SongNotFoundException("The searched object was not found")
    
        song_data = data_song["_items"]

        return song_data