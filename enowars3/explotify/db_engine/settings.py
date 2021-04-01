#Schemas
songs_schema = {
    "username":{
        "type":"string"
    },
    "hash_id":{
        "type":"string"
    },
     "path":{
        "type":"string"
    },
    "filename":{
        "type":"string"
    },
    "all_path":{
        "type":"string"
    },
    "name_song":{
        "type":"string"
    }
    
}

#Config
MONGO_HOST = "explotify_db"
MONGO_DBNAME = "explotify_db"
MONGO_PORT = 27017
DOMAIN = {"songs": {
    "schema":songs_schema,
    'resource_methods': ['GET', 'POST'],
}}