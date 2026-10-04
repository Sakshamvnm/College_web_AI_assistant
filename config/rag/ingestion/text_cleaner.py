import re


class TextCleaner:

    @staticmethod
    def clean(text):

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"\n+", "\n", text)

        return text.strip()