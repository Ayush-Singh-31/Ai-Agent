import ollama

def init(version) -> None:
    with open("modelfile", "r") as file:
        build = file.read()
    ollama.create(model = version, modelfile = build, stream = True)
    return None

if __name__ == "__main__":
    version = "Agent"
    init(version)
    print("Welcome to the Llama Chatbot!")
    print("Type 'exit' to quit.")
    while True:
        prompt = input(">>> ").strip().lower()
        if prompt == "exit":
            break
        response = ollama.generate('llama3.2', prompt)
        print(response['response'])