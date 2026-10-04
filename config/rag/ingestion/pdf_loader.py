from pathlib import Path
from pypdf import PdfReader


class PDFLoader:

    def __init__(self):
        self.data_folder = Path(__file__).parent.parent / "data"

    def load_all_pdfs(self):
        documents = []

        for pdf in self.data_folder.glob("*.pdf"):
            print(f"Reading {pdf.name}")

            reader = PdfReader(pdf)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            documents.append({
                "filename": pdf.name,
                "text": text
            })

        return documents