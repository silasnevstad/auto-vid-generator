import os
from services.pexels import PexelsAPI
from services.tts import ElevenLabsTTS
from services.transcription import VoskTranscriber
from services.subtitles import SubtitleGenerator
from services.editor import VideoEditor


def generate_video_from_text(text, name):
    output_path = os.path.join("../data/output", name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    pexels = PexelsAPI()
    tts = ElevenLabsTTS()
    transcriber = VoskTranscriber()
    editor = VideoEditor()

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, 'data'), exist_ok=True)

    # TODO: Get topic from text
    topic = "nature"

    # Step 1: Fetch stock video
    print("Step 1: Fetching stock video")
    video_path = os.path.join(output_path, 'data', 'video.mp4')
    pexels.download_video(topic, video_path)
    print(f"Video downloaded to {video_path}")

    # Step 2: Generate TTS audio
    print("Step 2: Generating TTS audio")
    audio_bytes, alignment = tts.generate_audio_with_timestamps(text)
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
    print(f"Subtitles created successfully at {subtitle_path}")

    # Step 5: Combine video, audio, and subtitles
    print("Step 5: Combining video, audio, and subtitles")
    combined_output_path = os.path.join(output_path, 'data', 'combined_video.mp4')
    # TODO: No audio???
    success = editor.combine_audio_video(video_path, audio_path, combined_output_path)
    if not success:
        print("Error: Combining audio and video was unsuccessful")
        return

    scaled_output_path = os.path.join(output_path, 'data', 'combined_video_scaled.mp4')
    if not editor.scale_and_crop(combined_output_path, scaled_output_path):
        print("Error: Styling video was unsuccessful")
        return

    # TODO: Chunk words into groups for subtitles
    subtitles_output_path = os.path.join(output_path, 'data', 'combined_video_scaled_with_subtitles.mp4')
    success = editor.add_subtitles(scaled_output_path, subtitle_path, subtitles_output_path)
    if not success:
        print("Error: Adding subtitles was unsuccessful")
        return

    # TODO: Fix fade effects
    final_output_path = os.path.join(output_path, 'final_video.mp4')
    if not editor.add_fade_effects(scaled_output_path, audio_path, final_output_path):
        print("Error: Adding fade effects was unsuccessful")
        return

    print(f"Video generated successfully at {final_output_path}")


if __name__ == "__main__":
    text = "Welcome to auto-shorts-generator."
    generate_video_from_text(text, "example")
