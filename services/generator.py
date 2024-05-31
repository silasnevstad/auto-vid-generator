import os
from services.pexels import PexelsAPI
from services.tts import ElevenLabsTTS
from services.transcription import VoskTranscriber
from services.subtitles import SubtitleGenerator
from services.editor import VideoEditor
from services.reddit import Reddit
from services.prompts import fact_generator_prompt, fact_generator_tool
from services.gpt import GPT


class ShortsGenerator:
    def __init__(self):
        self.tts = ElevenLabsTTS()
        self.pexels = PexelsAPI()
        self.transcriber = VoskTranscriber()
        self.editor = VideoEditor()
        self.reddit = Reddit()
        self.gpt = GPT()

    def generate_video_from_script(self, output_folder, script, topic=None):
        output_path = os.path.join("../data/output", output_folder)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        os.makedirs(output_path, exist_ok=True)
        os.makedirs(os.path.join(output_path, 'data'), exist_ok=True)

        # Step 1: Generate TTS audio
        print("Step 1: Generating TTS audio")
        audio_bytes, alignment = self.tts.generate_audio_with_timestamps(script)
        if not audio_bytes:
            print("Failed to generate TTS audio.")
            return
        audio_path = os.path.join(output_path, 'data', 'audio.mp3')
        self.tts.save_audio(audio_bytes, audio_path)
        print(f"Audio generated successfully at {audio_path}")

        # Step 2: Transcribe audio for subtitles
        print("Step 2: Transcribing audio for subtitles")
        transcription_results = self.transcriber.transcribe_audio(audio_path)
        timestamps = self.transcriber.extract_timestamps(transcription_results)
        transcription_path = os.path.join(output_path, 'data', 'transcription.json')
        self.transcriber.save_transcription(transcription_results, transcription_path)

        # Step 3: Generate subtitle file
        print("Step 3: Generating subtitle file")
        subtitle_path = os.path.join(output_path, 'data', 'subtitles.ass')
        SubtitleGenerator.generate_ass(timestamps, subtitle_path)
        subtitles_duration = SubtitleGenerator.subtitles_duration(timestamps)
        print(f"Subtitles created successfully at {subtitle_path}, duration: {subtitles_duration}")

        # Step 4: Fetch stock video
        print("Step 4: Fetching stock video")
        video_path = os.path.join(output_path, 'data', 'video.mp4')
        self.pexels.download_video(topic if topic is not None else "nature", video_path,
                              min_duration=int(subtitles_duration) + 5)
        print(f"Video downloaded to {video_path}")

        # Step 5: Combine video, audio, and subtitles
        print("Step 5: Editing together short")
        final_path = os.path.join(output_path, 'final_video.mp4')
        if not self.editor.create_shorts_from_video_with_audio(
                video_path, audio_path, subtitles_duration + 5, subtitle_path, final_path):
            print("Failed to edit together short")
            return

        print(f"Video generated successfully at {final_path}")

    def generate_reddit_video_from_hot_posts(self, output_folder, subreddit):
        posts = self.reddit.get_hot_posts(subreddit)
        if not posts:
            print(f"Failed to fetch posts from subreddit: {subreddit}")
            return

        script = f"{posts[0]['title']}. {posts[0]['content']}"

        self.generate_video_from_script(output_folder, script)

    def generate_facts_video_with_background_topic(self, output_folder, topic=None):
        script = self.gpt.create_completion([fact_generator_prompt], tools=[fact_generator_tool], tool_argument="script")

        self.generate_video_from_script(output_folder, script, topic)


if __name__ == "__main__":
    generator = ShortsGenerator()
    generator.generate_facts_video_with_background_topic("example", "nature drone shot fast")
