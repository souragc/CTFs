import random
from app import app
from exceptions.FileUploadExceptions import NotSupportedException

class FileUploadService():
    
    __ALLOWED_EXTENSIONS = ["mp3"]



    def save_file(self,file,path_to_save):
        name_file = random.randint(0,41235)
        allowed = self.__check_extensions(file.filename)
        
        if allowed:
            path_end_file = f"{path_to_save}/{str(name_file)}.mp3"
            file.save(path_end_file)
            return path_end_file
        else:
            app.logger.error(f"The file {file.filename} has an unsupported exception")
            raise NotSupportedException("The file extension is not supported")
    




    def __check_extensions(self,filename):
        extension = filename.split(".")
        if extension[1] in self.__ALLOWED_EXTENSIONS:
            return True
        else:
            return False



