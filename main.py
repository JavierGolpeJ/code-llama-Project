import requests
def chat_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "gemma3", "prompt": prompt, "stream": True}
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                print(line)

if __name__ == "__main__":
    chat_with_ollama("Tell me a joke.")