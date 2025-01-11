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
    print("Type 'change' : To change to another model")
    print("=" * 40)
    print()
    return None

def initDecider() -> None:
    subprocess.run(['ollama', 'rm', 'Decider'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Decider', '-f', './Decider-Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return None

def initLanguage() -> None:
    subprocess.run(['ollama', 'rm', 'Language'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Language', '-f', './Language-Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return None

def initTaskBreaker() -> None:
    subprocess.run(['ollama', 'rm', 'Task-Breaker'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Task-Breaker', '-f', './TaskBreaker-Modelfile'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return None

def init() -> None:
    initDecider()
    initLanguage()
    initTaskBreaker()
    os.system('touch Models.txt')
    models = subprocess.run(["ollama","list"], stdout = subprocess.PIPE, text = True)
    models = models.stdout.split("\n")
    with open('Models.txt', 'w') as file:
        for i in range(1,len(models)):
            if len(models[i]) > 0:
                file.write(models[i].split()[0].split(":")[0] + "\n")
    return None

def addModel(version: str) -> None:
    with open('Models.txt', 'w') as file:
        file.write(version + "\n")
    return None

def makeCustom(version: str) -> str:

    modelName = input("Enter New Model Name: ")
    temperature = input("Enter New Model temperature: ")
    system = input("Enter New Model System: ")
    if len(modelName) == 0 or len(temperature) == 0 or len(system) == 0:
        print("Invalid Input!")
        return "Error(1)"
    with open(f'./{modelName}', 'w') as file:
        file.write(f"# {modelName}\n")
        file.write(f"FROM {version}\n")
        file.write(f"PARAMETER temperature {temperature}\n")
        file.write(f"SYSTEM \"\"\"{system}\"\"\"\n")

    subprocess.run(['ollama', 'create', modelName, '-f', f'./{modelName}'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    addModel(version)

    print("Model Created Successfully!")
    print()

    return modelName

def langcheck(prompt: str) -> str:
    messages = [
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ]
    response = ollama.chat("Language", messages = messages)
    return response['message']['content']

def taskClassifier(prompt: str) -> str:
    # Use Lighter Model for Task Classification
    messages = [
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ]
    response = ollama.chat("Decider", messages = messages)
    return response['message']['content']

def complexTask(prompt: str) -> list:
    messages = [
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ]
    response = ollama.chat("Task-Breaker", messages = messages)
    taskList = response['message']['content']
    taskList = taskList.split("\n")
    subtasks = []
    for task in taskList:
        if taskClassifier(task) == "complex":
            complexTask(task)
        else:
            subtasks.append(task)
    return subtasks

def chat(prompt, version) -> None:
    if taskClassifier(prompt) == "complex":
        print("Going Complex")
        subtasks = complexTask(prompt)
        print(subtasks)
        return None
    else:
        messages = [
        {
            'role': 'user',
            'content': f"{prompt}",
        },
        ]
        response = ollama.chat(version, messages = messages)
        print(response['message']['content'])
        return None

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
    os.remove('Models.txt')
    return None

if __name__ == "__main__":
    welcome()
    init()
    
    version = "phi4"
    while True:
        prompt = input(">>> ").strip().lower()
        if prompt == "exit":
            cleanUp(version)
            break
        elif prompt == "status":
            getStatus()
            continue
        elif prompt == "create":
            version = makeCustom(version)
            if version == "Error(1)":
                print("Error in creating model!")
                continue
            continue
        elif prompt == "change":
            version = input("Enter Model Name: ")
            continue
        prompt = langcheck(prompt)
        chat(prompt, version)