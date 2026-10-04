class PromptBuilder:

    @staticmethod
    def build(context, question, history=None):

        if history is None:
            history = []

        # Keep only the most recent 8 messages
        history = history[-8:]

        # Build conversation history
        history_parts = []

        for message in history:

            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":
                history_parts.append(f"User: {content}")

            elif role == "assistant":
                history_parts.append(f"Assistant: {content}")

        conversation = "\n".join(history_parts)

        return f"""
You are the official AI assistant of Academia International College.

IMPORTANT RULES:

1. Answer ONLY questions related to Academia International College.

2. If the question is completely unrelated to Academia International College,
reply exactly:
"I can only answer questions related to Academia International College."

3. Use ONLY the information provided in the context.

4. Do not invent, guess, or add information that is not in the context.

5. Use the conversation history to understand follow-up questions.

6. The conversation history is only for understanding what the user means.
It is NOT a source of factual information.

7. Give a SHORT and DIRECT answer.

8. Prefer 1-3 sentences.

9. Do not repeat the question.

10. Do not add unnecessary explanations.

11. If a college-related question cannot be answered from the context, reply:
"I couldn't find that information in the available college resources."

Conversation History:
{conversation}

Context:
{context}

Current Question:
{question}

Answer:
"""