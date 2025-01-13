import ollama
import subprocess
import os

def welcome() -> None:
    """
    Prints a simple welcome banner and basic usage instructions.
    """
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
    """
    Removes any existing 'Decider' model, then creates a fresh one using 'Decider-Modelfile'.
    """
    subprocess.run(['ollama', 'rm', 'Decider'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Decider', '-f', './Decider-Modelfile'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None

def initLanguage() -> None:
    """
    Removes any existing 'Language' model, then creates a fresh one using 'Language-Modelfile'.
    """
    subprocess.run(['ollama', 'rm', 'Language'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Language', '-f', './Language-Modelfile'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None

def initTaskBreaker() -> None:
    """
    Removes any existing 'Task-Breaker' model, then creates a fresh one using 'TaskBreaker-Modelfile'.
    """
    subprocess.run(['ollama', 'rm', 'Task-Breaker'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ollama', 'create', 'Task-Breaker', '-f', './TaskBreaker-Modelfile'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None

def init() -> None:
    """
    Initializes the three default models (Decider, Language, Task-Breaker) and 
    logs the list of models to 'Models.txt'.
    """
    initDecider()
    initLanguage()
    initTaskBreaker()

    # Create 'Models.txt' file if it doesn't exist
    os.system('touch Models.txt')

    # Get list of models from 'ollama list'
    models = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, text=True)
    models = models.stdout.split("\n")

    # Write model names to 'Models.txt'
    with open('Models.txt', 'w') as file:
        for i in range(1, len(models)):
            if len(models[i]) > 0:
                file.write(models[i].split()[0].split(":")[0] + "\n")

    return None

def addModel(version: str) -> None:
    """
    Writes the given model version to 'Models.txt'.
    """
    with open('Models.txt', 'w') as file:
        file.write(version + "\n")
    return None

def makeCustom(version: str) -> str:
    """
    Prompts user for new model details (name, temperature, system) and creates the model.
    Returns the new model name or 'Error(1)' on invalid input.
    """
    modelName = input("Enter New Model Name: ")
    temperature = input("Enter New Model temperature: ")
    system = input("Enter New Model System: ")

    # Check for empty inputs
    if len(modelName) == 0 or len(temperature) == 0 or len(system) == 0:
        print("Invalid Input!")
        return "Error(1)"

    # Create a new model file locally
    with open(f'./{modelName}', 'w') as file:
        file.write(f"# {modelName}\n")
        file.write(f"FROM {version}\n")
        file.write(f"PARAMETER temperature {temperature}\n")
        file.write(f"SYSTEM \"\"\"{system}\"\"\"\n")

    # Create the model via ollama
    subprocess.run(['ollama', 'create', modelName, '-f', f'./{modelName}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Record the new model version
    addModel(version)

    print("Model Created Successfully!")
    print()
    return modelName

def langcheck(prompt: str) -> str:
    """
    Uses the 'Language' model to possibly transform or process the prompt 
    before passing it along for classification or further chat.
    """
    messages = [
        {
            'role': 'user',
            'content': f"{prompt}",
        },
    ]
    response = ollama.chat("Language", messages=messages)
    return response['message']['content']

def taskClassifier(prompt: str) -> str:
    """
    Uses the 'Decider' model to classify the prompt 
    as 'complex' or not (based on the model's logic).
    """
    messages = [
        {
            'role': 'user',
            'content': f"{prompt}",
        },
    ]
    response = ollama.chat("Decider", messages=messages)
    return response['message']['content']

def complexTask(prompt: str) -> list:
    """
    Breaks down a complex prompt into subtasks using the 'Task-Breaker' model 
    and returns a list of those subtasks.
    """
    messages = [
        {
            'role': 'user',
            'content': f"{prompt}",
        },
    ]
    response = ollama.chat("Task-Breaker", messages=messages)
    taskList = response['message']['content'].split("\n")
    subtasks = []
    for task in taskList:
        subtasks.append(task)
    return subtasks

def chat(prompt, version) -> None:
    """
    Decides if prompt is 'complex' and either:
      1. Breaks it into subtasks and chats through each subtask.
      2. Or chats directly with the model if it's not complex.
    """
    if taskClassifier(prompt) == "complex":
        # If prompt is complex, break into subtasks
        subtasks = complexTask(prompt)
        for task in subtasks:
            messages = [
                {
                    'role': 'user',
                    'content': f"How to: {task}",
                },
            ]
            response = ollama.chat(version, messages=messages)
            print(response['message']['content'])
            print()
        return None
    else:
        # Simple prompt: just respond
        messages = [
            {
                'role': 'user',
                'content': f"{prompt}",
            },
        ]
        response = ollama.chat(version, messages=messages)
        print(response['message']['content'])
        return None

def getStatus() -> None:
    """
    Fetches and displays the status of all models via ollama.ps().
    """
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
    """
    Stops the specified model and removes 'Models.txt'.
    """
    subprocess.run(['ollama', 'stop', version], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove('Models.txt')
    return None

if __name__ == "__main__":
    # Display welcome message and set up default models
    welcome()
    init()

    # Default model version
    version = "phi4"

    while True:
        prompt = input(">>> ").strip().lower()

        # Exit the chatbot
        if prompt == "exit":
            cleanUp(version)
            break

        # Check status of models
        elif prompt == "status":
            getStatus()
            continue

        # Create a new custom model
        elif prompt == "create":
            version = makeCustom(version)
            if version == "Error(1)":
                print("Error in creating model!")
            continue

        # Switch to an existing model
        elif prompt == "change":
            version = input("Enter Model Name: ")
            continue

        # Language-check the prompt and run chat
        prompt = langcheck(prompt)
        chat(prompt, version)