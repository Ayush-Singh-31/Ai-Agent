import ollama, subprocess

def makeCustom() -> str:

    modelName = input("Enter New Model Name: ")
    temperature = input("Enter New Model temperature: ")
    system = input("Enter New Model System: ")

    with open('./Modelfile', 'w') as file:
        file.write(f"FROM llama3.2\n")
        file.write(f"PARAMETER temperature {temperature}\n")
        file.write(f"SYSTEM \"\"\"{system}\"\"\"\n")
        
    subprocess.run(['ollama', 'create', modelName, '-f', './Modelfile'])
    return modelName

def chat(prompt, version) -> None:
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
    print("Welcome to the Llama Chatbot!")
    print("Type 'exit' to quit.")
    print("Type 'status' to check the status of the models.")

    defonew = input("Would you like to create a new model? (y/n): ").strip().lower()
    if defonew == "y":
        version = makeCustom()
    else:
        version = "llama3.2"

    while True:
        prompt = input(">>> ").strip().lower()
        if prompt == "exit":
            break
        elif prompt == "status":
            getStatus()
            continue
        chat(prompt, version)