from rag.retrieval.retriever import Retriever
from rag.llm.response_generator import ResponseGenerator


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.generator = ResponseGenerator()

    def ask(self, question, history=None):

        # Make sure history is available
        if history is None:
            history = []

        # Handle simple messages without running RAG/LLM
        simple_messages = {
            "hi": "Hello! How can I help you with Academia International College?",
            "hello": "Hello! How can I help you with Academia International College?",
            "hey": "Hey! How can I help you with Academia International College?",
            "thanks": "You're welcome!",
            "thank you": "You're welcome!",
            "bye": "Goodbye!",
            "goodbye": "Goodbye!"
        }

        cleaned_question = question.lower().strip()

        if cleaned_question in simple_messages:
            return simple_messages[cleaned_question]

        # --------------------------------
        # Limit conversation history
        # --------------------------------
        # Keep only the most recent 8 messages
        history = history[-8:]

        # --------------------------------
        # Build a better retrieval query
        # --------------------------------
        # Include recent conversation so follow-up
        # questions like "what about BCA?" have context.
        retrieval_query = question

        if history:
            previous_messages = []

            for message in history[-4:]:
                role = message.get("role", "")
                content = message.get("content", "")

                if role in ["user", "assistant"] and content:
                    previous_messages.append(
                        f"{role}: {content}"
                    )

            if previous_messages:
                retrieval_query = (
                    "\n".join(previous_messages)
                    + "\nuser: "
                    + question
                )

        # --------------------------------
        # Retrieve relevant documents
        # --------------------------------
        docs = self.retriever.retrieve(retrieval_query)

        # --------------------------------
        # Generate answer
        # --------------------------------
        answer = self.generator.generate(
            docs,
            question,
            history=history
        )

        return answer


# -----------------------------
# Test the pipeline
# -----------------------------
if __name__ == "__main__":

    pipeline = RAGPipeline()

    history = []

    while True:

        question = input("\nYou: ")

        if question.lower().strip() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer = pipeline.ask(
            question,
            history=history
        )

        print("\nBot:", answer)

        # Save conversation
        history.append({
            "role": "user",
            "content": question
        })

        history.append({
            "role": "assistant",
            "content": answer
        })