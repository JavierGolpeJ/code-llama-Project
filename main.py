import requests


def read_file(filename_path):
    with open(filename_path, "r") as f:
        return f.read()


# if __name__ == "__main__":
#     read_file("code_files/code1.txt")

def chat_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "gemma3", "prompt": prompt, "stream": True}
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                print(line)


#
#
if __name__ == "__main__":
    chat_with_ollama(read_file("code_files/code1.txt"))
