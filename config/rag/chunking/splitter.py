import re


class TextSplitter:

    def __init__(self, chunk_size=1200, overlap=150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):

        # Clean excessive whitespace
        text = re.sub(r"\s+", " ", text).strip()

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            # Move forward while keeping overlap
            start += self.chunk_size - self.overlap

        return chunks