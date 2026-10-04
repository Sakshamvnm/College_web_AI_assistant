from .splitter import TextSplitter


def chunk_documents(documents):

    splitter = TextSplitter()

    final_chunks = []

    for doc in documents:

        chunks = splitter.split(doc["text"])

        for i, chunk in enumerate(chunks):

            chunk_data = {
                "filename": doc["filename"],
                "chunk_id": i,
                "text": chunk,
                "source_type": doc.get("source_type", "pdf")
            }

            # Preserve website URL
            if doc.get("source_type") == "website":
                chunk_data["url"] = doc.get("url")

            final_chunks.append(chunk_data)

    return final_chunks