import requests
import json

def run_model(prompt):
    # URL of the Ollama model server (adjust as needed)
    url = "http://localhost:11434/api/generate"

    full_response = ""
    data = {"model": "qwen2.5-coder:0.5b", "prompt": prompt, "stream": True}
    with requests.post(url, json=data) as response:
            for line in response.iter_lines():
                    if line:
                        json_line = json.loads(line.decode("utf-8"))
                        full_response += json_line.get("response", "")
                        if json_line.get("done", False):
                            break
    print(full_response)

def get_code(file_name):
    with open(file_name, "r") as file:
        content = file.read()
        print(content)
    return content



# Example usage:
if __name__ == "__main__":
    prompt_text = "i want you to make comments for this code:" + get_code("test-1.txt")
    run_model(prompt_text)