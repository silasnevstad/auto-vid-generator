fact_generator_tool = {
    "type": "function",
    "function": {
        "name": "fact_shorts_script",
        "description": "Returns a script for a TTS model for a shorts video (a tiktok/instagram 15 second video).",
        "parameters": {
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "Strictly the speakers content, nothing else.",
                },
            },
            "required": ["script"],
        },
    }
}

fact_generator_prompt = ('You are a social media short form content writer, think of facts and return a TTS script, '
                         'a snappy delivery on the fact. Do not use any punctuation other than periods.')

script_cleaner_tool = {
    "type": "function",
    "function": {
        "name": "make_video_with_clean_script",
        "description": "Makes a video given a clean script",
        "parameters": {
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "The cleaned script (y/o to years old, 1st to first, etc).",
                },
            },
            "required": ["script"],
        },
    }

}

script_cleaner_prompt = ('Clean the following script for a TTS model. Remove anything a TTS model would mess up or is '
                         'irrelevant, be intelligent about it. For example, "My (28F) little sister (15F)" should be '
                         '"My 15 year old little sister".')
