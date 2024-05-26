import requests
import base64
import subprocess
from config.settings import ELEVEN_LABS_API_KEY, FFMPEG_PATH


class ElevenLabsTTS:
    # TODO: Experiment with different voices
    def __init__(self, voice_id="21m00Tcm4TlvDq8ikWAM"):
        self.api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
        self.headers = {
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY
        }

    def generate_audio_with_timestamps(self, text, model_id="eleven_multilingual_v2", stability=0.5,
                                       similarity_boost=0.75):
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        response = requests.post(self.api_url, json=data, headers=self.headers)

        if response.status_code != 200:
            print(f"Error encountered, status: {response.status_code}, content: {response.text}")
            return None

        response_dict = response.json()

        audio_bytes = base64.b64decode(response_dict["audio_base64"])
        alignment = response_dict["alignment"]

        return audio_bytes, alignment

    @staticmethod
    def save_audio(audio_bytes, filename):
        with open(filename, 'wb') as f:
            f.write(audio_bytes)

    @staticmethod
    def slow_down_audio(input_path, output_path, factor=1.25):
        # TODO: FIX ME
        if factor < 0.5 or factor > 2.0:
            raise ValueError("Factor must be between 0.5 and 2.0")

        command = [
            FFMPEG_PATH, '-i', input_path, '-filter:a', f"atempo={1/factor}", '-vn', output_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
