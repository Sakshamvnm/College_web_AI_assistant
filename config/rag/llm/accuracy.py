import time
import psutil
import pandas as pd

from chatbot import ask

# Questions to evaluate
test_questions = [
    "What is Artificial Intelligence?",
    "Who invented Python?",
    "What is Machine Learning?",
    "Explain cloud computing.",
    "What is an operating system?"
]

results = []

for question in test_questions:

    print(f"Testing: {question}")

    # Measure response time
    start = time.time()

    response, inputs, outputs = ask(question)

    end = time.time()

    response_time = end - start

    # Token statistics
    input_tokens = inputs["input_ids"].shape[1]
    output_tokens = len(outputs[0]) - input_tokens

    # Speed
    tokens_per_sec = output_tokens / response_time

    # CPU & RAM
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.Process().memory_info().rss / (1024**2)

    # Store results
    results.append({
        "Question": question,
        "Response Time": response_time,
        "Input Tokens": input_tokens,
        "Output Tokens": output_tokens,
        "Tokens/sec": tokens_per_sec,
        "CPU (%)": cpu,
        "RAM (MB)": ram
    })

    print("Done.\n")

# Create dataframe
df = pd.DataFrame(results)

# Print results
print(df)

# Save results
df.to_csv("metrics.csv", index=False)

print("\nmetrics.csv created successfully!")