import openai
import json


class GPT:
    def __init__(self, api_key=None):
        if api_key is None:
            self.client = openai.OpenAI()
        else:
            self.client = openai.OpenAI(api_key=api_key)

    def create_completion(self, messages, system_messages=None, tools=None, tool_choice=None, tool_argument=None, model='gpt-4o'):
        chat_messages = self.make_chat_messages(messages, system_messages)
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=chat_messages,
                tools=tools,
                tool_choice="auto" if tool_choice is None else {"type": "function", "function": {"name": tool_choice}}
            )
            print(completion)
            return self.handle_completion(completion, tool_argument)
        except openai.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.APIError as e:
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

    @staticmethod
    def make_chat_messages(messages, system_messages=None):
        if system_messages is None:
            system_messages = []
        chat_messages = [{
            'role': 'system',
            'content': message
        } for message in system_messages]
        for i, message in enumerate(messages):
            chat_messages.append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': message
            })
        return chat_messages

    @staticmethod
    def handle_completion(completion, argument=None):
        if completion.choices[0].finish_reason == 'tool_calls':
            return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)[argument]
        else:
            return completion.choices[0].message.content
