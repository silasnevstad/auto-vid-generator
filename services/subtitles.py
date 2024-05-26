from datetime import timedelta


class SubtitleGenerator:
    @staticmethod
    def generate_ass(timestamps, output_path, font='Futura', font_size=30,
                     primary_color='&H00F5F5F5', secondary_color='&H00F5F5F5',
                     outline_color='&H00000000', back_color='&H00000000', bold=-1,
                     italic=0, underline=0, strikeout=0, scale_x=100, scale_y=100,
                     spacing=0, angle=0, border_style=1, outline=3, shadow=2,
                     alignment=2, margin_l=10, margin_r=10, margin_v=40, encoding=0):
        # TODO: Group words into logical chunks
        header = f"""[Script Info]
PlayResY: 600
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{font_size},{primary_color},{secondary_color},{outline_color},{back_color},{bold},{italic},{underline},{strikeout},{scale_x},{scale_y},{spacing},{angle},{border_style},{outline},{shadow},{alignment},{margin_l},{margin_r},{margin_v},{encoding}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        events = ""
        for index, timestamp in enumerate(timestamps):
            start = timedelta(seconds=timestamp['start'])
            end = timedelta(seconds=timestamp['end'])
            start_str = SubtitleGenerator.format_time(start)
            end_str = SubtitleGenerator.format_time(end)
            events += f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{timestamp['word']}\n"

        with open(output_path, 'w') as f:
            f.write(header + events)

    @staticmethod
    def format_time(t):
        total_ms = int(t.total_seconds() * 1000)
        hours, remainder = divmod(total_ms, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, milliseconds = divmod(remainder, 1000)
        return f"{hours:01}:{minutes:02}:{seconds:02}.{milliseconds // 10:02}"
