from .pdf_loader import PDFLoader
from .web_loader import WebsiteLoader
from .text_cleaner import TextCleaner
from rag.chunking.chunk_utils import chunk_documents


class IngestionPipeline:

    def run(self):

        # ==============================
        # 1. LOAD PDFs
        # ==============================

        print("\n" + "=" * 60)
        print("LOADING PDF DOCUMENTS")
        print("=" * 60)

        pdf_loader = PDFLoader()
        pdf_documents = pdf_loader.load_all_pdfs()

        print(f"PDF documents loaded: {len(pdf_documents)}")


        # ==============================
        # 2. LOAD WEBSITE
        # ==============================

        print("\n" + "=" * 60)
        print("LOADING WEBSITE")
        print("=" * 60)

        website_loader = WebsiteLoader()

        website_documents = website_loader.load_website(
            max_pages=150
        )

        print(f"Website pages loaded: {len(website_documents)}")


        # ==============================
        # 3. COMBINE DOCUMENTS
        # ==============================

        documents = pdf_documents + website_documents

        print("\n" + "=" * 60)
        print("DOCUMENT SUMMARY")
        print("=" * 60)

        print(f"Total documents: {len(documents)}")


        # ==============================
        # 4. CLEAN + ADD SOURCE METADATA
        # ==============================

        cleaned_documents = []

        for doc in documents:

            cleaned_doc = {
                "filename": doc["filename"],
                "text": TextCleaner.clean(doc["text"])
            }

            # Website document
            if "url" in doc:

                cleaned_doc["url"] = doc["url"]
                cleaned_doc["source_type"] = "website"

            # PDF document
            else:

                cleaned_doc["source_type"] = "pdf"

            cleaned_documents.append(cleaned_doc)


        # ==============================
        # 5. CREATE CHUNKS
        # ==============================

        print("\n" + "=" * 60)
        print("CREATING CHUNKS")
        print("=" * 60)

        chunks = chunk_documents(cleaned_documents)

        print(f"Generated {len(chunks)} chunks")


        # ==============================
        # 6. SHOW SAMPLE CHUNKS
        # ==============================

        print("\n" + "=" * 60)
        print("SAMPLE CHUNKS")
        print("=" * 60)

        for chunk in chunks[:5]:

            print("-" * 60)

            print("File:", chunk.get("filename"))
            print("Source:", chunk.get("source_type"))

            if chunk.get("source_type") == "website":
                print("URL:", chunk.get("url"))

            print("Chunk ID:", chunk.get("chunk_id"))

            print("\nText:")
            print(chunk["text"][:500])

        print("\n" + "=" * 60)
        print("INGESTION COMPLETE")
        print("=" * 60)

        return chunks


# ==========================================
# RUN DIRECTLY
# ==========================================

if __name__ == "__main__":

    pipeline = IngestionPipeline()

    chunks = pipeline.run()

    print("\nFinal chunk count:", len(chunks))