import subprocess, ollama

subprocess.run(['ollama', 'create', 'Language', '-f', './Language-Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

version = "Language"
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