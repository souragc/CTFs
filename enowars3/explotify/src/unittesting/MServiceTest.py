import unittest
from services_app.music_service import MService
from pydub import AudioSegment
class MServerTest(unittest.TestCase):

    service_music = MService()
    audio = AudioSegment.from_file("distopianM/distopian.mp3")


    def test_split_segment_normal_2(self):
        max_time = 12000
        splitted_audio = self.audio[0:max_time]
        number_of_segments = 3500
        list_of_segments = self.service_music.split_segment(splitted_audio,number_of_segments)
        self.assertEqual(number_of_segments,len(list_of_segments))

    def test_split_segment_normal(self):
        max_time = 12000
        splitted_audio = self.audio[0:max_time]
        number_of_segments = 4
        list_of_segments = self.service_music.split_segment(splitted_audio,number_of_segments)
        self.assertEqual(number_of_segments,len(list_of_segments))


    def test_split_segment_bigger_than(self):
        max_time = 12000
        splitted_audio = self.audio[0:max_time]
        number_of_segments = 13000
        list_of_segments = self.service_music.split_segment(splitted_audio,number_of_segments)
        self.assertEqual(max_time,len(list_of_segments))

    def test_convert_lyrics_voice(self):
        lyrics = "Hellow People"
        words = lyrics.split(" ")
        count_words = len(words)
        list_of_voice = self.service_music.convert_lyrics_to_voice("Hellow People")
        self.assertEqual(count_words,len(list_of_voice))

    def test_get_segments_from_raw_data(self):
        lyrics = "Hello People, I am trying to get it right"
        list_of_voice = self.service_music.convert_lyrics_to_voice(lyrics)
        segment = self.service_music.segment_from_raw_data(list_of_voice[0])
        self.assertTrue(isinstance(segment,AudioSegment))
        self.assertEqual(segment.sample_width,2)
        self.assertEqual(segment.frame_rate,24000)
        self.assertEqual(segment.channels,1)
        self.assertEqual(segment.duration_seconds,0.96)

    def test_inject_silence_to_segments(self):
        lyrics = "Hello"
        list_of_voice = self.service_music.convert_lyrics_to_voice(lyrics)
        segment = self.service_music.segment_from_raw_data(list_of_voice[0])
        duration = segment.duration_seconds * 1000
        silence_duration = 4000
        listed = self.service_music.inject_silence_to_segments([segment],silence_duration)
        new_segment = listed[0]
        self.assertAlmostEqual(new_segment.duration_seconds * 1000,duration + silence_duration * 2,delta=1)

    def test_generate_song_from_lyrics(self):
         lyrics = "secrethere"
         self.service_music.generate_song(lyrics,"secret.mp3")

    


if __name__=="__main__":
    unittest.main()