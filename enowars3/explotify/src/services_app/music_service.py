import string
import random
import os
from pydub import AudioSegment
from gtts import gTTS
from io import BytesIO
from io import StringIO
import secrets
import time
from espeakng import ESpeakNG
from cachetools import cached, LRUCache


class MService():

    
    def __repr__(self):
        return "MService"

    def __init__(self, *args, **kwargs):
        self.__espeak = ESpeakNG()
        self.__espeak.speed = 150
        self.generate_song("a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0",export_path="cache.mp3")




    default_path = "distopianM"
    __hard_code_path = "sounds_db"
    __prefix = "-transform.wav"
    __suffix = "vocal-"
    __distopian_music = "distopianM"
    try:
        __distopian_segment = AudioSegment.from_file(default_path + "/distopian.mp3")
    except:
        raise FileNotFoundError("Default music was not found!")

    def generate_song(self,lyrics,base_music=default_path,export_path="/",name_file="out",export_format="mp3"):

        base_music_audio = None

        if not os.path.exists(base_music):
            raise FileNotFoundError("The base music was not found")

        if base_music == self.default_path:
            base_music_audio = self.__distopian_segment[0:240000]
        else:
            base_music_audio = AudioSegment.from_file(base_music)

        lyrics = lyrics.lower()

        sounds_lyrics = self.convert_lyrics_to_voice(lyrics)

        number_of_segments = len(sounds_lyrics)
        
        segments_music = self.split_segment(base_music_audio,number_of_segments)  


        segments_lyrics = sounds_lyrics
        
        segments_lyrics = self.inject_silence_to_segments(segments_lyrics,1500)

        concatenated_segments = self.concatenate_segments(segments_lyrics,segments_music)

        concatenated_segments.export(f"{export_path}", format=export_format)




    def concatenate_segments(self,segment_voice,segment_music):
        empty_segment = AudioSegment.empty()
        
        if len(segment_voice) >= len(segment_music):
            low = len(segment_music)
            high = len(segment_voice)
            high_list = segment_voice
        else:
            low = len(segment_voice)
            high = len(segment_music)
            high_list = segment_music
            
        
        for x in range(0,low):
            empty_segment = empty_segment + segment_voice[x] + segment_music[x]
        
        for x in range(low,high):
            empty_segment = empty_segment + high_list[x]

        return empty_segment


    def inject_silence_to_segments(self,segments,duration_silence_ms=1500):
        list_of_segments_with_silence = []
        silence = AudioSegment.silent(duration=duration_silence_ms)
        for x in range(len(segments)):
            list_of_segments_with_silence.append(silence + segments[x] + silence)
        return list_of_segments_with_silence
        
    @cached(cache=LRUCache(maxsize=150))
    def __get_text_as_raw_voice(self,text):
        wav_generated = self.__espeak.synth_wav(text)
        song_as_bytes = BytesIO(wav_generated)
        process = self.segment_from_raw_data(song_as_bytes)
        return process

    def convert_lyrics_to_voice(self,lyrics):
        words = lyrics.split(" ")
        list_of_words_as_sound = [self.__get_text_as_raw_voice(word) for word in words]
        return list_of_words_as_sound
        
    def segment_from_raw_data(self,raw_data):
        raw_segment = AudioSegment.from_file(raw_data)
        raw_data.close()
        return raw_segment
    
    def split_segment(self,segment,number_of_segments):
        list_of_partitions = []
        miliseconds_segment = int(segment.duration_seconds * 1000)
        if(number_of_segments > miliseconds_segment):
            number_of_segments = miliseconds_segment
        equality = miliseconds_segment // number_of_segments
        sorted_list = [x for x in range(equality,miliseconds_segment + 1,equality)]
        sorted_list.append(miliseconds_segment)
        sorted_list.sort()
        low_begin = 0
        for part in sorted_list:
            list_of_partitions.append(segment[low_begin:part])
            low_begin = part

        return list_of_partitions
            

            
        
        