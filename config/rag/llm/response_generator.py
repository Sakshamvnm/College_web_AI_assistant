from rag.llm.prompt_builder import PromptBuilder
from rag.llm.local_llm import LocalLLM


class ResponseGenerator:

    def __init__(self):
        self.llm = LocalLLM()

    def generate(self, docs, question, history=None):

        if history is None:
            history = []

        # Keep only recent conversation
        history = history[-8:]

        # Build context for the LLM.
        # Source metadata is kept internally but NOT shown to the user.
        context_parts = []

        for doc in docs:

            source_type = doc.get("source_type", "unknown")
            filename = doc.get("filename", "unknown")

            if source_type == "website":
                source = f"Website: {doc.get('url', 'unknown')}"
            elif source_type == "pdf":
                source = f"PDF: {filename}"
            else:
                source = filename

            context_parts.append(
                f"[SOURCE: {source}]\n"
                f"{doc['text'][:1200]}"
            )

        context = "\n\n".join(context_parts)

        # Build the prompt with conversation history
        prompt = PromptBuilder.build(
            context,
            question,
            history=history
        )

        # Generate answer using the local Qwen model
        output = self.llm.model.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.2,
            top_p=0.9,
        )

        # Extract only the actual answer
        answer = output["choices"][0]["message"]["content"].strip()

        return answer