import json
import os
import re
import requests
import time

# regex patterns for Java
class_pattern = re.compile(r'^\s*(?:public\s+)?class\s+(\w+)')
method_pattern = re.compile(
    r'^\s*(?:public|protected|private)?\s*'  # visibility
    r'(?:static\s+)?'  # optional static
    r'[A-Za-z_<>\[\]]+\s+'  # return type
    r'(\w+)\s*\(.*\)\s*[{;]'  # method name + params
)


def scrape_java_file(path):
    """
   Reads a .java file and returns a list of dictionaries:
   [
       {
           "class_name": ...,
           "function": ...,
           "documentation": ...,
           "block_code": ...
       },
       ...
   ]
   """
    results = []
    current_class_name = None
    current_method = None
    collecting_method = False
    brace_count = 0
    method_code = []
    documentation = []

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            # Check for class
            cls = class_pattern.match(line)
            if cls:
                current_class_name = cls.group(1)
                continue

            if current_class_name:
                # If currently collecting a method
                if collecting_method:
                    method_code.append(line)
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0:
                        # method ends
                        results.append({
                            "class_name": current_class_name,
                            "function": current_method,
                            "documentation": "".join(documentation).strip(),
                            "block_code": "".join(method_code).strip()
                        })
                        collecting_method = False
                        method_code = []
                        documentation = []
                        current_method = None
                    continue

                # Collect documentation
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                    documentation.append(line)
                    continue

                # Check for method
                m = method_pattern.match(line)
                if m:
                    current_method = m.group(1)
                    collecting_method = True
                    method_code.append(line)
                    brace_count = line.count('{') - line.count('}')
    return results


# writes the LLM output to the text document
def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)


# runs the desired model with the given prompt we've engineered and gives the full code file as context
def run_model(prompt, model, in_file):
    # def run_model(prompt, model, function):
    # URL of the Ollama model server (adjust as needed)

    start_time = time.time()
    url = "http://localhost:11434/api/generate"

    full_prompt = prompt + in_file
    full_response = ""

    data = {"model": model, "prompt": full_prompt, "stream": True}
    with requests.post(url, json=data) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break

        # outputs to doc
        #     print(full_response)
        output_response_dock(full_response)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)


# takes the file in and only counts lines of actual code excluding developer commentary
# if size of code is < 150 lines use smaller model
# if > 150 lines use larger model
def File_classifier(in_file):
    count = 0

    with open(in_file, "r") as f:

        for line in f:
            stripped = line.strip()
            if stripped.startswith("//") or "/*" in stripped or "*/" in stripped:
                continue
            if stripped:  # ignore empty lines
                count += 1

    if count >= 150:
        print(f"Lines in file: {count}")
        return "Gemma3:4b"
    else:
        print(f"Lines in file: {count}")
        return "Gemma3:12b"
        # return "qwen2.5-coder:0.5b"
        # return "Gemma3:4b"


# this is not function
# this section of code that uses a forloop to iterate over the elements in the methods array and
# direct them to the proper processing chain via if statement


if __name__ == "__main__":
    directory = "Minesweeper-reop"
    our_prompt = (
        "For each method in the given code write a general description of what the individual methods do as well as descriptions of the input and output parameters using the following structure \n"
        "{file name}\n"
        "{function name 1}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "{function name 2}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "Include the original developer comments. We are not asking for suggestions or improvements, we are only asking for commentary explaining what the given code does. Must follow the given structure exactly. If you find yourself repeating the same thing over and over, move on to the next function."
    )
    structure = []
    # iterate over files in the code directory
    for dir_path, _, files in os.walk(directory):
        for file in files:
            # if the file is a java file
            if file.endswith(".java"):
                # append the path
                path = os.path.join(dir_path, file)

                classes = scrape_java_file(path)
                if classes:
                    # structure[path] = classes
                    structure.extend(classes)

                with open(path, "r", encoding="utf-8") as java_file:
                    content = java_file.read()

                model = File_classifier(path)

                # run the model
                run_model(our_prompt, model, content)

    with open("structure2.json", "w") as outfile:
        json.dump(structure, outfile, indent=4)

    print("Wrote class/method structure to structure.json")
