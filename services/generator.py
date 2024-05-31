import os
from services.pexels import PexelsAPI
from services.tts import ElevenLabsTTS
from services.transcription import VoskTranscriber
from services.subtitles import SubtitleGenerator
from services.editor import VideoEditor
from services.prompts import fact_generator_prompt, fact_generator_tool
from services.gpt import GPT


def generate_facts_video_with_background_topic(topic, name):
    output_path = os.path.join("../data/output", name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    pexels = PexelsAPI()
    tts = ElevenLabsTTS()
    transcriber = VoskTranscriber()
    editor = VideoEditor()
    gpt = GPT()

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, 'data'), exist_ok=True)

    # Get script from GPT
    print("Step 0: Generating script")
    script = gpt.create_completion([fact_generator_prompt], tools=[fact_generator_tool], tool_argument="script")
    print(f"Generated script: {script}")

    # Step 1: Fetch stock video
    print("Step 1: Fetching stock video")
    video_path = os.path.join(output_path, 'data', 'video.mp4')
    pexels.download_video(topic, video_path)
    print(f"Video downloaded to {video_path}")

    # Step 2: Generate TTS audio
    print("Step 2: Generating TTS audio")
    audio_bytes, alignment = tts.generate_audio_with_timestamps(script)
    if not audio_bytes:
        print("Failed to generate TTS audio.")
        return
    audio_path = os.path.join(output_path, 'data', 'audio.mp3')
    tts.save_audio(audio_bytes, audio_path)
    print(f"Audio generated successfully at {audio_path}")

    # Step 3: Transcribe audio for subtitles
    print("Step 3: Transcribing audio for subtitles")
    transcription_results = transcriber.transcribe_audio(audio_path)
    timestamps = transcriber.extract_timestamps(transcription_results)
    transcription_path = os.path.join(output_path, 'data', 'transcription.json')
    transcriber.save_transcription(transcription_results, transcription_path)
    print(f"Successfully transcribed audio.")

    # Step 4: Generate subtitle file
    print("Step 4: Generating subtitle file")
    subtitle_path = os.path.join(output_path, 'data', 'subtitles.ass')
    SubtitleGenerator.generate_ass(timestamps, subtitle_path)
    subtitles_duration = SubtitleGenerator.subtitles_duration(timestamps)
    print(f"Subtitles created successfully at {subtitle_path}, duration: {subtitles_duration}")

    # Step 5: Combine video, audio, and subtitles
    print("Step 5: Editing together short")
    final_path = os.path.join(output_path, 'final_video.mp4')
    if not editor.create_shorts_from_video_with_audio(
            video_path, audio_path, subtitles_duration + 5, subtitle_path, final_path):
        print("Failed to edit together short")
        return

    print(f"Video generated successfully at {final_path}")


if __name__ == "__main__":
    generate_facts_video_with_background_topic("nature", "example")
