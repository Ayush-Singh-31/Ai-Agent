def getApiKey() -> str:
    try:
        with open("openai.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("API key not found!")

if __name__ == "__main__":
    apiKey = getApiKey()
    