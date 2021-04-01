class FormatChecker():

    __song_format_mandatory = ["web_lyrics","lyrics","name_song"]

    def check_create_song_format(self,dictionary):
        for field in self.__song_format_mandatory:
            if field not in dictionary or dictionary[field] == "" or dictionary[field] == None:
                return False
                
        return True
