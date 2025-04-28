import json
import os
import re
import requests
import time

# regex patterns for Java
class_pattern  = re.compile(r'^\s*(?:public\s+)?class\s+(\w+)')
method_pattern = re.compile(
    r'^\s*(?:public|protected|private)?\s*'          # visibility
    r'(?:static\s+)?'                                 # optional static
    r'[A-Za-z_<>\[\]]+\s+'                            # return type
    r'(\w+)\s*\(.*\)\s*[{;]'                          # method name + params
)

def extract_methods_and_docs(java_text):
    """
    Given the full text of a Java file, return a list of tuples
    (method_name, documentation_string, method_code_block).
    """
    entries = []
    i = 0
    lines = java_text.splitlines()
    n = len(lines)

    while i < n:
        line = lines[i]
        m = method_pattern.match(line)
        if m:
            method_name = m.group(1)
            # look backwards for a Javadoc immediately above
            doc = ""
            j = i - 1
            if j >= 0 and lines[j].strip().endswith("*/"):
                # scan upward until start of /**
                doc_lines = []
                while j >= 0:
                    doc_lines.append(lines[j])
                    if '/**' in lines[j]:
                        break
                    j -= 1
                doc = "\n".join(reversed(doc_lines))
                # strip the /* */ markers
                doc = re.sub(r'^/\*\*|\*/$', '', doc, flags=re.MULTILINE).strip()

            # now capture the full method block by counting braces
            brace_count = 0
            block_lines = []
            # if the opening brace is on the signature line, start count at 1
            if '{' in line:
                brace_count = line.count('{') - line.count('}')
                block_lines.append(line)
            i += 1
            # read until we've closed all braces
            while i < n and brace_count > 0:
                block_lines.append(lines[i])
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1

            entries.append((method_name, doc, "\n".join(block_lines)))
            continue  # skip the i += 1 below, since we've advanced in the inner loop

        i += 1

    return entries



def scrape_java_file(path):
    """
    Reads a .java file and returns a list of dicts:
      [ { "class_name": ..., "methods": [ ... ] }, … ]
    """
    classes = []
    current = None

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            cls = class_pattern.match(line)
            if cls:
                # start a new class entry
                if current:
                    classes.append(current)
                current = {"class_name": cls.group(1), "methods": []}
                continue

            if current:
                m = method_pattern.match(line)
                if m:
                    current["methods"].append(m.group(1))

    # append last class if present
    if current:
        classes.append(current)
    return classes

#writes the LLM output to the text document
def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)

#runs the desired model with the given prompt we've engineered and gives the full code file as context
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
#if size of code is < 150 lines use smaller model
#if > 150 lines use larger model
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


def process_java_file(path):
    """
    Reads a .java file, extracts its class name and all methods,
    then returns a list of dicts in the format you specified.
    """
    text = open(path, encoding='utf-8').read()
    # find the first class declaration
    cls_match = class_pattern.search(text)
    class_name = cls_match.group(1) if cls_match else os.path.splitext(os.path.basename(path))[0]

    results = []
    for method_name, doc, block in extract_methods_and_docs(text):
        results.append({
            "class name":    class_name,
            "function":      method_name,
            "func_documentation": doc,
            "func_block":    block
        })
    return results

def process_all_java(src_dir):
    """
    Walks src_dir for .java files, processes each,
    and returns a single list of all method-entries.
    """
    all_entries = []
    for dirpath, _, files in os.walk(src_dir):
        for fname in files:
            if fname.endswith(".java"):
                path = os.path.join(dirpath, fname)
                all_entries.extend(process_java_file(path))
    return all_entries

# def process_all_java(src_dir, dst_root="output"):
#     # make a root output directory
#     os.makedirs(dst_root, exist_ok=True)
#
#     for dirpath, _, files in os.walk(src_dir):
#         for fname in files:
#             if not fname.endswith(".java"):
#                 continue
#
#             java_path = os.path.join(dirpath, fname)
#             structure = scrape_java_file(java_path)
#
#             # derive a per-file directory name, e.g. "Test1.java" → "Test1"
#             base = os.path.splitext(fname)[0]
#             # per_dir = os.path.join(dst_root, base)
#             # os.makedirs(per_dir, exist_ok=True)
#
#             # write out structure.json inside that directory
#             out_path = os.path.join(dst_root, f"{base}.json")
#             with open(out_path, "w", encoding="utf-8") as outfile:
#                 json.dump(structure, outfile, indent=4)
#
#             print(f"Wrote {len(structure)} classes to {out_path}")

if __name__ == "__main__":
    directory = "Code-text"
    our_prompt = (
        "For each method in the given code write a general description of what the individual methods do as well as descriptions of the input and output parameters using the following structure \n"
        "{file name}\n"
        "{function name 1}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "{function name 2}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n"
        "Include the original developer comments. We are not asking for suggestions or improvements, we are only asking for commentary explaining what the given code does. Must follow the given structure exactly. If you find yourself repeating the same thing over and over, move on to the next function."
    )
    structure = {}
    # iterate over files in the code directory
    for dir_path, _, files in os.walk(directory):
        for file in files:
            #if the file is a java file
            if file.endswith(".java"):
                #append the path
                path = os.path.join(dir_path, file)

                classes = scrape_java_file(path)
                if classes:
                    structure[path] = classes

                with open(path, "r", encoding="utf-8") as java_file:
                    content = java_file.read()

                model = File_classifier(path)

                #run the model
                run_model(our_prompt, model, content)

    # process_all_java(src_dir='Code-text', dst_root='output')

    output = process_all_java("Code-text")
    with open("methods.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print(f"Wrote {len(output)} method entries to methods.json")

    # with open("structure.json", "w") as outfile:
    #     json.dump(structure, outfile, indent=4)
    print("Wrote class/method structure to structure.json")