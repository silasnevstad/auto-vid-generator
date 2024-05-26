import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel


class VoskTranscriber:
    def __init__(self, model_path="../models/vosk-model-en-us-0.22", logs_enabled=False):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at path: {model_path}")
        self.model = Model(model_path)
        if not logs_enabled:
            SetLogLevel(-1)

    def transcribe_audio(self, audio_path):
        wav_path = self.convert_to_wav(audio_path)
        wf = wave.open(wav_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 44100]:
            raise ValueError("Audio file must be WAV format mono PCM.")

        recognizer = KaldiRecognizer(self.model, wf.getframerate())
        recognizer.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                results.append(json.loads(recognizer.Result()))
            else:
                results.append(json.loads(recognizer.PartialResult()))

        results.append(json.loads(recognizer.FinalResult()))
        return results

    @staticmethod
    def convert_to_wav(audio_path):
        wav_path = audio_path.replace(".mp3", ".wav")

        # check if converted WAV file already exists
        if os.path.exists(wav_path):
            return wav_path

        command = [
            "ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return wav_path

    @staticmethod
    def extract_timestamps(transcription_results):
        timestamps = []
        for result in transcription_results:
            if 'result' in result:
                for word in result['result']:
                    timestamps.append({
                        "word": word['word'],
                        "start": word['start'],
                        "end": word['end']
                    })
        return timestamps

    @staticmethod
    def save_transcription(transcription_results, output_path):
        with open(output_path, 'w') as f:
            json.dump(transcription_results, f)
