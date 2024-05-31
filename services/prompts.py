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
                         f'a snappy delivery on the fact. Use the {fact_generator_tool} tool to generate the script.'
                         'Do not use any punctuation other than periods.')
