import ollama

def chat(prompt, version = "llama3.2") -> None:
    messages = [
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ]
    response = ollama.chat(version, messages = messages)
    print(response['message']['content'])

def getStatus() -> None:
    response: ollama.ProcessResponse = ollama.ps()
    for model in response.models:
        print('Model: ', model.model)
        print('  Digest: ', model.digest)
        print('  Expires at: ', model.expires_at)
        print('  Size: ', model.size)
        print('  Size vram: ', model.size_vram)
        print('  Details: ', model.details)
        print('\n')
    return None

if __name__ == "__main__":
    version = input("Enter Model Name: ")
    print("Welcome to the Llama Chatbot!")
    print("Type 'exit' to quit.")
    while True:
        prompt = input(">>> ").strip().lower()
        if prompt == "exit":
            break
        elif prompt == "status":
            getStatus()
            continue
        chat(prompt)