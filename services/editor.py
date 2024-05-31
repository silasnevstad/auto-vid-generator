import os
import subprocess
from config.settings import FFMPEG_PATH


class VideoEditor:
    def __init__(self, logs_enabled=False):
        self.logs_enabled = logs_enabled

    def combine_audio_video(self, video_path, audio_path, output_path):
        if not self.__verify_files_exist([video_path, audio_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__process_command([
            FFMPEG_PATH, '-i', video_path, '-i', audio_path, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
            '-strict', 'experimental', output_path
        ], output_path)


    def add_subtitles(self, video_path, subtitle_path, output_path):
        if not self.__verify_files_exist([video_path, subtitle_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__process_command([
            FFMPEG_PATH, '-i', video_path, '-vf', f"subtitles={subtitle_path}", output_path
        ], output_path)

    def add_background_music(self, video_path, audio_path, output_path):
        if not self.__verify_files_exist([video_path, audio_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__process_command([
            FFMPEG_PATH, '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
            output_path
        ], output_path)

    def scale_and_crop(self, video_path, output_path):
        if not self.__verify_files_exist([video_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__run_command([
            FFMPEG_PATH, '-i', video_path, '-vf', "scale=-1:1920, crop=1080:1920:656.25:0, fps=30", '-an', output_path
        ])

    def trim_video(self, video_path, duration, output_path):
        if not self.__verify_files_exist([video_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__process_command([
            FFMPEG_PATH, '-i', video_path, '-t', str(duration), '-c', 'copy', output_path
        ], output_path)

    def add_fade_effects(self, video_path, audio_path, output_path):
        if not self.__verify_files_exist([video_path, audio_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__run_command([
            FFMPEG_PATH, '-i', video_path, '-i', audio_path, '-t', '55.95', '-vf',
            "fade=in:0:d=0.5,fade=out:1783.5:d=0.5,subtitles=output.srt", output_path
        ])

    def create_shorts_from_video_with_audio(self, video_path, audio_path, duration, subtitles_path, output_path):
        if not self.__verify_files_exist([video_path, audio_path, subtitles_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__run_command([
            FFMPEG_PATH, '-i', video_path, '-i', audio_path, '-t', str(duration), '-vf',
            f"scale=-1:1920,"
            f"crop=1080:1920:656.25:0,"
            f"subtitles={subtitles_path},"
            f"fade=in:st=0:d=0.5,fade=out:st={duration - 0.5}:d=0.5",
            '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
            output_path
        ])

    def create_video_from_image(self, image_path, output_path):
        if not self.__verify_files_exist([image_path]):
            return False
        self.__ensure_directory_exists(output_path)
        return self.__process_command([
            FFMPEG_PATH, '-loop', '1', '-i', image_path, '-t', '60', '-vf',
            "fps=30, zoompan=z='min(zoom+0.001,1.5)':d=1800:x='iw/2-(iw/zoom/2)':y='ih/2-("
            "ih/zoom/2)':s=1080x1920:fps=30",
            output_path
        ], output_path)

    def __run_command(self, command):
        try:
            if self.logs_enabled:
                subprocess.run(command, check=True)
            else:
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(command)}' failed with error: {e}")
            return False
        return True

    def __process_command(self, command, output_path):
        if self.__already_exists(output_path):
            return False
        return self.__run_command(command)

    @staticmethod
    def __already_exists(output_path):
        if os.path.exists(output_path):
            print(f"Output file '{output_path}' already exists.")
            return True
        return False

    @staticmethod
    def __verify_files_exist(paths):
        for path in paths:
            if not os.path.exists(path):
                print(f"Error: File '{path}' does not exist.")
                return False
        return True

    @staticmethod
    def __ensure_directory_exists(file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
