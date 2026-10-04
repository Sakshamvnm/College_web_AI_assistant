import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rag.pipeline import RAGPipeline

# Load the RAG pipeline only once when Django starts
pipeline = RAGPipeline()


def home(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"
        }, status=405)

    try:
        data = json.loads(request.body)

        question = data.get("prompt", "").strip()
        history = data.get("history", [])

        if not question:
            return JsonResponse({
                "answer": "Please enter a question."
            })

        print(f"Question: {question}")
        print(f"History: {history}")

        # Get answer from the RAG pipeline
        answer = pipeline.ask(
            question,
            history=history
        )

        print(f"Answer: {answer}")

        return JsonResponse({
            "answer": answer
        })

    except Exception as e:
        print("Error:", e)

        return JsonResponse({
            "answer": str(e)
        }, status=500)