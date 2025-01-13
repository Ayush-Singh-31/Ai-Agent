# Multi Model Ai Agent

This repository provides an advanced multi model ai agent script for local Large Language Model (LLM) management using [Ollama](https://github.com/jmorganca/ollama). Its primary objective is to demonstrate a sophisticated pipeline for dynamic model instantiation, ephemeral concurrency, and context-specific chat capabilities with minimal user intervention.

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Workflow and Execution](#workflow-and-execution)
5. [Subprocess Management](#subprocess-management)
6. [Model Lifecycle](#model-lifecycle)
7. [Task Decomposition and Classification](#task-decomposition-and-classification)
8. [Usage Instructions](#usage-instructions)
9. [Advanced Topics](#advanced-topics)
10. [License](#license)

---

## Overview
The script automates key operational aspects of multiple LLM models, including:
- **Model creation and deletion** via `ollama create` and `ollama rm`.
- **Run-time orchestration** of different domain-specific models (e.g., `Decider`, `Language`, and `Task-Breaker`).
- **Task classification** and hierarchical prompt decomposition for complex user requests.
- **Contextual session management** for advanced prompt execution.

By utilizing low-level system calls and advanced concurrency strategies, this orchestrator serves as a template for creating highly modular LLM ecosystems in Python.

---

## Architecture
1. **Orchestrator Entry Point (`__main__`)**  
   - Invokes initialization routines and sets up a default model version.
   - Maintains a command-line interface loop for capturing user input and routing requests to appropriate subsystems.

2. **LLM Facade & Subsystems**  
   - **`initDecider()`, `initLanguage()`, `initTaskBreaker()`**  
     - Each function encapsulates a unique model's lifecycle methods using `ollama`'s CLI for specialized tasks (decision-making, language detection, or subtask generation).
   - **`chat(prompt, version)`**  
     - A high-level function that decides whether to invoke sophisticated subtask breakdown or a direct chat pass-through, based on the classification provided by `Decider`.

3. **File and Process Management**  
   - **`Models.txt`**  
     - A local registry to track and maintain the latest instantiated model references.
   - **`cleanUp(version)`**  
     - Terminates the active model session (`ollama stop`) and purges ephemeral files.

The architecture promotes decoupled modules, simplifying testability and ensuring that scaling or substituting models (e.g., from local Dockerized containers to HPC clusters) remains straightforward.

---

## Core Components

### `welcome()`
- Prints an ASCII-based greeting interface and enumerates available commands.
- Provides a visual demarcation for the user to easily discern valid input directives.

### `init()`
- Sequentially calls `initDecider()`, `initLanguage()`, and `initTaskBreaker()`.
- Creates (or overwrites) the `Models.txt` file to store a local reference of available models.

### `makeCustom(version)`
- Generates a new model file by extending a base parent model specified by `version`.
- Adjusts parameters (e.g., temperature) and system prompts for fine-tuned generation tasks.
- Automatically persists this new model in `Models.txt`.

### `chat(prompt, version)`
- Employs a hybrid approach:
  1. If `taskClassifier(prompt)` returns `"complex"`, the system delegates to `complexTask(prompt)`, then loops through each subtask, providing individualized solutions.
  2. Otherwise, it directly communicates with the selected model.

---

## Workflow and Execution

1. **Initialization**
   - On script execution, `init()` is called to systematically remove or rebuild the pre-defined LLMs (`Decider`, `Language`, `Task-Breaker`).
   - This ensures a clean environment before proceeding with user interactions.

2. **User Interaction Loop**
   - Users input one of the following keywords or a free-text prompt:
     - `exit` : Exits and triggers clean-up sequence.
     - `status` : Invokes `getStatus()` to list active LLM processes.
     - `create` : Calls `makeCustom()` to instantiate a new model from the base version.
     - `change` : Switches the active model in use.
     - Any other string triggers a chain of (1) language verification (`langcheck(prompt)`), (2) classification (`taskClassifier(prompt)`), and (3) subtask decomposition if deemed “complex”.

3. **Model Invocation**
   - The script offloads user-provided prompts to the designated model using `ollama.chat`.
   - All responses are seamlessly printed back, ensuring minimal overhead while showcasing advanced concurrency primitives behind the scenes.

---

## Subprocess Management
Python’s `subprocess.run()` is extensively utilized for:
- Robust process invocation of `ollama` CLI commands without polluting stdout/stderr for the end user.
- Automated removal and recreation of ephemeral models.
- Error handling with defensive patterns (e.g., capturing return codes, silent error logs).

This design pattern not only improves clarity but also mitigates side effects caused by concurrent operations or model misconfigurations.

---

## Model Lifecycle
1. **Create**  
   - Dynamically define new parameter settings (e.g., temperature) and system-level prompts.
2. **Load**  
   - For every user session, the script references an external register (`Models.txt`) to load existing models and determine the default target.
3. **Stop & Remove**  
   - When a session terminates, `cleanUp()` systematically stops active LLM processes and deletes ephemeral artifacts.

---

## Task Decomposition and Classification
- **`langcheck(prompt)`**  
  - Routes the prompt to the `Language` model, ensuring advanced polyglot detection before classification.
- **`taskClassifier(prompt)`**  
  - Evaluates the complexity of the request via the `Decider` model. If designated “complex,” the prompt transitions into a multi-stage breakdown.
- **`complexTask(prompt)`**  
  - Employs the `Task-Breaker` model to sequentially generate subtask structures, facilitating micro-level orchestration.

These abstractions not only modularize the prompt flow but also enhance the system’s extensibility for future expansions (e.g., adding separate code-linter steps or domain-specific validations).

---

## Usage Instructions
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Ayush-Singh-31/Ai-Agent
   cd Ai-Agent
2. **Install Dependencies**
   - Python 3.x with pip recommended
   - [Ollama](https://ollama.com/) installed locally
   - Recommended install flow:
   ```bash
     # If you don't have pip, install it (Linux / macOS):
    python3 -m ensurepip --upgrade
    
    # Install the Python dependencies:
    pip install ollama
3. **Run the Script**
   ```bash
   python main.py
4.**Interact**
  - Type any valid command (status, create, etc.) or a free-form prompt to observe the orchestrator in action.

---

## Advanced Topics

### Ephemeral Concurrency and Scalability

By decoupling the creation and teardown of LLM models, the script can be extended to run numerous parallel sessions. Utilizing ephemeral concurrency patterns (e.g., scaling specific model creation tasks in containerized environments or HPC clusters) allows the platform to handle large user loads or specialized contexts with minimal overhead.

### Custom Parameterization

Users can easily integrate advanced LLM configuration flags. If your model requires specialized hyperparameters or context windows, simply extend the `makeCustom()` logic to persist them in the model definitions.

### Extended Models

To integrate specialized domain models (e.g., sentiment analysis, contextual summarizers, or generative code transformers), replicate the existing pattern in `init()`, create a new method (e.g., `initSentiment()`) with a unique `-f` argument, and reference it in `Models.txt`.

## License

This repository is licensed under the MIT License. Feel free to modify, distribute, or incorporate these scripts in your projects.
