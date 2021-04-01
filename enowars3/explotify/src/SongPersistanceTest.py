import unittest
from services import song_persistance_service
from exceptions.SongsPersistanceExceptions import SongNotFoundException
class SongPersistanceTest(unittest.TestCase):


    def test_song_save(self):
        song = song_persistance_service.save_song({"name":"Testing song new"})
        print(song)

    def test_get_song_by_id(self):
        with self.assertRaises(SongNotFoundException):
            song_persistance_service.get_song_by_id(3)
        song = song_persistance_service.get_song_by_id("5cdf2e35f0c3f3f089b50f3d")
        print(song)



if __name__ == "__main__":
     unittest.main()