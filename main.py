import requests
import json


def read_file(filename_path):
    with open(filename_path, "r") as f:
        return f.read()

def run_model(prompt):
    # URL of the Ollama model server (adjust as needed)
    url = "http://localhost:11434/api/generate"

    full_response = ""
    data = {"model": "gemma3", "prompt": prompt, "stream": True}
    with requests.post(url, json=data) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break
    print(full_response)

if __name__ == "__main__":
    run_model(read_file("code_files/code1.txt"))
