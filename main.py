import json
import os
import requests


# writes the LLM output to the text document
def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)


# runs the desired model with the given prompt we've engineered and gives the full code file as context
def run_model(prompt, model, in_file_contents):
    url = "http://localhost:11434/api/generate"
    full_prompt = prompt + in_file_contents
    full_response = ""

    data = {"model": model, "prompt": full_prompt, "stream": True}
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break

        output_response_dock(full_response)


# decides which model to use based on number of actual code lines
def File_classifier(file_path):
    count = 0
    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("//") or "/*" in stripped or "*/" in stripped:
                continue
            if stripped:  # ignore empty lines
                count += 1

    return "gemma3:12b" if count >= 150 else "gemma3"


# main process
if __name__ == "__main__":
    directory = "Code-text"
    prompt = (
        "For each method in the given code write a general description of what the individual methods do as well as descriptions of the input and output parameters using the following structure \n"
        "{file name}\n"
        "{function name 1}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "{function name 2}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "Include the original developer comments. We are not asking for suggestions or improvements, we are only asking for commentary explaining what the given code does. Must follow the given structure exactly. If you find yourself repeating the same thing over and over, move on to the next function."
    )

    for dir_path, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                full_path = os.path.join(dir_path, file)

                # Read file contents
                with open(full_path, "r", encoding="utf-8") as java_file:
                    contents = java_file.read()

                # Determine model size
                model = File_classifier(full_path)

                # Run model with content
                run_model(prompt, model, contents)