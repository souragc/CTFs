from services_app.user_service import UserService
from services_app.music_service import MService
from services_app.login_service import LoginService
from services_app.file_upload_service import FileUploadService
from services_app.lyrics_generator_service import LyricsGeneratorService
from services_app.format_checker_service import FormatChecker
from services_app.song_service import SongPersistanceService

file_upload_service = FileUploadService()
login_service = LoginService()
music_service = MService()
user_service = UserService()
lyrics_service = LyricsGeneratorService()
format_checker_service = FormatChecker()
song_persistance_service = SongPersistanceService()

