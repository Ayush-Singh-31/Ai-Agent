import subprocess, ollama

subprocess.run(['ollama', 'create', 'Task-Breaker', '-f', './TaskBreaker-Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

version = "Task-Breaker"
while True:
    prompt = input("Enter your prompt: ")
    messages = [
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ]
    response = ollama.chat(version, messages = messages)
    print(response['message']['content'])