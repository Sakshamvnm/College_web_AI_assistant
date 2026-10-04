from pathlib import Path
from llama_cpp import Llama


class LocalLLM:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parents[2]

        model_path = (
            BASE_DIR
            / "models"
            / "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"
        )

        print(model_path)

        self.model = Llama(
            model_path=str(model_path),
            n_ctx=2048,
            n_threads=4,
            n_batch=128,
            verbose=False,
        )