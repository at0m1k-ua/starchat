from openai import OpenAI

from starchat.singleton import SingletonMeta


class CensorshipService(metaclass=SingletonMeta):
    def __init__(self):
        # self.__client = OpenAI()
        pass

    def is_harmful(self, message: str):
        return False
        response = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":
                    "You are a censorship bot, a part of a social network that filters any "
                    "content that can be harmful. Please answer with a single short word as "
                    "'false' or 'true', without braces or any other signs. You should detect "
                    "swear words and violence and write 'true' if it needs to be banned. "
                    "If the message is ok, write 'false'. You should apply censorship on "
                    "a text written in any language you can recognize."},
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message.content == 'true'
