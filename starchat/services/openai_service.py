import os

from openai import OpenAI

from starchat.singleton import SingletonMeta


class OpenAiService(metaclass=SingletonMeta):
    def __init__(self):
        self.is_available = os.environ.get('OPENAI_API_KEY') is not None
        if not self.is_available:
            return

        self.__client = OpenAI()

    def process(self, request):
        if not self.is_available:
            raise IOError('OpenAI API is not available (no key specified)')

        response = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=request
        )
        response_content = response.choices[0].message.content
        print(response_content)
        return response_content
