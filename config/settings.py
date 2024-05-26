import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')
FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'