import ollama 
import subprocess
import os

def welcome() -> None:
    print("=" * 40)
    print("    Welcome to the Llama3.2 Chatbot!    ")
    print("=" * 40)
    print("Type 'exit'   : To quit the chatbot")
    print("Type 'status' : To check the status of models")
    print("Type 'create' : To create new model")
    print("=" * 40)
    print()
    return None

def makeCustom() -> str:

    modelName = input("Enter New Model Name: ")
    temperature = input("Enter New Model temperature: ")
    system = input("Enter New Model System: ")

    with open('./Modelfile', 'w') as file:
        file.write(f"FROM llama3.2\n")
        file.write(f"PARAMETER temperature {temperature}\n")
        file.write(f"SYSTEM \"\"\"{system}\"\"\"\n")

    subprocess.run(['ollama', 'create', modelName, '-f', './Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    print("Model Created Successfully!")
    print()

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
    return None

def cleanUp(version: str) -> None:
    subprocess.run(['ollama', 'stop', version], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(['ollama', 'rm', version], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    os.remove('./Modelfile')
    return None

if __name__ == "__main__":
    welcome()
        
    version = "phi4"
    customeModel = False
    while True:
        prompt = input(">>> ").strip().lower()
        if prompt == "exit":
            if customeModel == True:
                cleanUp(version)
            break
        elif prompt == "status":
            getStatus()
            continue
        elif prompt == "create":
            customeModel = True
            version = makeCustom()
            continue
        chat(prompt, version)