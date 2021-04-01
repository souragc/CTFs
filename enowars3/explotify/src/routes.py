
import random
import string
import base64
import json
import hashlib
from flask import Blueprint, render_template, abort,Response,redirect , url_for , session
from Models import Song
from app import db
from app import app
from flask import request
from flask import jsonify,send_from_directory
from services import user_service
from services import music_service
from functools import wraps
from services import login_service
from services import file_upload_service
from services import lyrics_service
from services import format_checker_service
from services import song_persistance_service
from app import app


routes = Blueprint("routes",__name__)


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('routes.login_manager'))

    return wrap 

mandatory_att = ["title","length","artist","lyrics","disk_number"]



@routes.route("/song/lyrics/<string:lyrics>")
def search_by_lyrics(lyrics):
    song_with_lyrics = Song.query.filter(Song.lyrics == lyrics).first()
    return jsonify(song_with_lyrics.to_dict())

@routes.route("/")
@is_logged_in
def entry_point():
    return render_template("index.html")

@routes.route("/index")
@is_logged_in
def entry_point_index():
    return render_template("index.html")

@routes.route("/login",methods=["GET","POST"])
def login_manager():

    if request.method=="GET":
        return render_template("login.html")

    if request.method=="POST":
        result_form = request.form.to_dict()
        
        check_prop = login_service.check_login_properties(result_form)
        if check_prop == True:
            try:
                login_service.login_user(user=result_form["username"],password=result_form["password"])
                return redirect(url_for("routes.entry_point"))
            except Exception as e:
                app.logger.error(e)
                return render_template("login.html",info={"error_description":"User not found"})
        else:
            return render_template("login.html",info={"error_description":"Not valid data to login"})
        

@routes.route("/register",methods=["GET","POST"])
def create_user_manager():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        result_form = request.form.to_dict()
        check_requirements = user_service.check_user_properties(result_form)
        if check_requirements is True:
            try:
                user_service.create_user(**result_form)
                return redirect(url_for("routes.login_manager"))
            except Exception as e:
                return render_template("register.html", info={"error_description":"Error adding user to the DB","error":e})
        else:
            return render_template("register.html",info={"error_description":"The Data is incomplete!"})
    else:
        return render_template("register.html",info={"error_description":"Error adding user to the DB"})
            

@routes.route("/song/<string:hash_id>/download",methods=["GET"])
@is_logged_in
def song_manager_downloader(hash_id):

    username = session["user"]    
    option = request.args.get('search_option')
    if option != "hash_id" and option != "id":
        return jsonify({"error_description":"The search option is invalid"})
    try:
        if option == "hash_id":
            song = song_persistance_service.get_song_by_hash_from_username(hash_id,username)
            app.logger.debug(song)
            app.logger.debug("Esto es song path : " + song["path"])
            app.logger.debug("Esto es song filename : " +  song["filename"])
            return send_from_directory(directory=song["path"], filename=song["filename"]),200
        
        if option == "id":
             song = song_persistance_service.get_song_by_id_from_username(hash_id,username)
             return send_from_directory(directory=song["path"], filename=song["filename"]),200
    except Exception as e:
        return jsonify({"error_description":str(e)})

@routes.route("/user/me")
@is_logged_in
def get_user_info():
    username = session["user"]
    user = user_service.get_username_info(username)
    return jsonify(user),200

@routes.route("/song/<string:hash_id>",methods=["GET"])
@is_logged_in
def song_manager_getter(hash_id):
    username = session["user"]
    option = request.args.get('search_option')
    if option != "hash_id" and option != "id":
        return jsonify({"error_description":"The search option is invalid"}),500
    try:
        if option == "hash_id":
            song = song_persistance_service.get_song_by_hash_from_username(hash_id,username)
            return jsonify(song)
        
        if option == "id":
             song = song_persistance_service.get_song_by_id_from_username(hash_id,username)
             return jsonify(song)
    except Exception as e:
        return jsonify({"error_description":str(e)}),404


@routes.route("/song",methods=["GET","POST"])
@is_logged_in
def songs_manager():
    
    if request.method == "GET":

        username = session["user"]
        try:
            all_songs = song_persistance_service.get_all_songs_by_user(username)
        except:
            return render_template("songs.html")
        user_info = user_service.get_username_info(username)
        return render_template("songs.html",songs=all_songs,user=user_info)

    if request.method == "POST":

        lyrics = None
        response = {"state":"success"}

        result = request.form.to_dict()


        check_input = format_checker_service.check_create_song_format(result)

        if check_input is not True:
            return jsonify({"error_description" : "The data is invalid!"})

        user = session["user"]

        user_file_path = user_service.get_music_folder_from_user(user)
        temp_file_path = user_service.get_temp_folder_from_user(user)

        random_file_name = random.randint(0,412350)
        generated_song_path = f"{user_file_path}/{random_file_name}.mp3"
        end_file_name = f"{random_file_name}.mp3"

        name_song = result["name_song"]

        if result["web_lyrics"].lower() == "false":
            lyrics = result["lyrics"]
        else:
            try:
                source,web_lyrics,web_possible = lyrics_service.generate_lyrics_from_website(result["lyrics"])
                lyrics = web_lyrics
                response["web_lyrics"] = web_possible
                response["source_used"] = source.decode("utf-8")
            except Exception as e:
                return jsonify({"error_description" : str(e)}),500

        try:
            
            if request.files is not None and "custom_song" in request.files:
                uploaded_file_base_path = file_upload_service.save_file(request.files["custom_song"],temp_file_path)
                music_service.generate_song(lyrics,export_path=generated_song_path,base_music=uploaded_file_base_path)
            else:
                music_service.generate_song(lyrics,export_path=generated_song_path)
        except Exception as e:
            return jsonify({"error_description":str(e)}),500
        
        hash_file = sha256_checksum(generated_song_path)

        song_persistance_service.save_song({"username":user,"hash_id":hash_file,
        "path":user_file_path,"filename":end_file_name,
        "all_path":generated_song_path,"name_song":name_song})

        #response["lyrics_used"] = lyrics
        response["id_hash"] = hash_file
        
        return jsonify(response),200
        
        
