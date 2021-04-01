import unittest
from services import lyrics_service

class LyricsServiceTest(unittest.TestCase):


    def test_lyrics_generate_website(self):
        source_info,text_generated,lyrics_website = lyrics_service.generate_lyrics_from_website("")


if __name__=="__main__":
    unittest.main()