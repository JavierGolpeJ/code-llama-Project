import json
import os
import re
import requests
import time, random

# regex patterns for Java
class_pattern  = re.compile(r'^\s*(?:public\s+)?class\s+(\w+)')
method_pattern = re.compile(
r'''^
        \s*
        (?:public|protected|private)   # optional visibility
        \s+
        (?:static\s+)?                  # optional static
        (?:[A-Za-z_<>\[\]]+\s+)?        # optional return type (catches constructors too)
        (\w+)                           # method or constructor name
        \s*\([^)]*\)                    # args in parentheses
        \s*(?:\{)?\s*$                  # optional {, then end-of-line
    ''',
    re.VERBOSE
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


# 1) Define your library of prompt templates
PROMPT_TEMPLATES = {
    "zero_shot": (
        "For each method in the given Java code, write a general description "
        "of what it does, listing its @param and @return. "
        "Include any original developer comments, but no suggestions.\n\n"
        "{file_name}\n"   # we’ll .format() this
        "{method_stub}"
    ),

    "few_shot": (
        "Example 1:\n"
        "  foo(int x)\n"
        "  @param x; the input value\n"
        "  @return int; the result doubled\n"
        "  Overview: doubles the input value.\n"
        "\n"
        "Example 2:\n"
        "  bar(String s)\n"
        "  @param s; the input string\n"
        "  @return String; uppercase version\n"
        "  Overview: converts string to uppercase.\n"
        "\n"
        "Now document the methods in:\n"
        "{file_name}\n"
        "{method_stub}"
    ),

    "chain_of_thought": (
        "We want to document Java methods. Let's think step by step:\n"
        "1) Identify the method signature and its parameters.\n"
        "2) Look for the Javadoc comment just above it.\n"
        "3) List @param lines and @return line.\n"
        "4) Write an Overview sentence.\n"
        "\n"
        "{file_name}\n"
        "{method_stub}"
    ),

    "hybrid": (
        # few-shot + CoT in one
        "Example:\n"
        "  Q: foo(int x) /** doubles x */  →\n"
        "  1) param x; the input integer\n"
        "  2) return int; x*2\n"
        "  Overview: returns double the input\n"
        "\n"
        "Now you:\n"
        "{file_name}\n"
        "{method_stub}"
    ),
}

# 2) A helper to build the prompt from one of those templates
def build_prompt(path, methods, style="few_shot"):
    # 2a) method_stub: join all methods into one blob
    stub_lines = []
    for name, doc, block in methods:
        stub_lines.append(f"{name}({', '.join(re.findall(r'\\w+\\s+\\w+', block.splitlines()[0]))})")
        # e.g. “push(int x)”
        if doc:
            stub_lines.append(doc.replace("\n", " "))
        stub_lines.append("")  # blank line between methods
    method_stub = "\n".join(stub_lines)

    # 2b) take the filename only
    file_name = os.path.basename(path)

    # 2c) pick the template and substitute
    template = PROMPT_TEMPLATES.get(style)
    if not template:
        raise ValueError(f"Unknown prompt style: {style}")

    return template.format(file_name=file_name, method_stub=method_stub)

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
            if not file.endswith(".java"):
                continue

            path = os.path.join(dir_path, file)
            content = open(path, encoding="utf-8").read()

            # extract your methods
            methods = extract_methods_and_docs(content)

            if not methods:
                continue

            # classify file size → pick model
            model = File_classifier(path)

            # 3) build the prompt in the style you want:
            #    could be “zero_shot”, “few_shot”, “chain_of_thought” or “hybrid”
            style = random.choice(["few_shot", "chain_of_thought", "zero_shot", "hybrid"])
            print(f"Style used: {style}")
            prompt = build_prompt(path, methods, style=style)

            # 4) call your existing run_model
            run_model(prompt, model, content)

    # process_all_java(src_dir='Code-text', dst_root='output')ai

    output = process_all_java("Code-text")
    with open("methods.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print(f"Wrote {len(output)} method entries to methods.json")

    # with open("structure.json", "w") as outfile:
    #     json.dump(structure, outfile, indent=4)
    # print("Wrote class/method structure to structure.json")