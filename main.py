import json
import os
import re
import time
import requests
import prompts

# Patterns for class and method
class_pattern = re.compile(r'^\s*(?:public\s+)?class\s+(\w+)')
method_pattern = re.compile(
    r'''^
        \s*
        (?:public|protected|private)   # visibility
        \s+
        (?:static\s+)?                # optional static
        (?:[A-Za-z_<>\[\]]+\s+)?      # return type or constructor
        (\w+)                         # method/constructor name
        \s*\([^)]*\)                  # parameters
        \s*(?:\{)?\s*$
    ''',
    re.VERBOSE
)

# Extract methods with optional Javadoc and full block
def extract_methods_and_docs(java_text):
    entries = []
    i = 0
    lines = java_text.splitlines()
    n = len(lines)

    while i < n:
        line = lines[i]
        m = method_pattern.match(line)
        if m:
            method_name = m.group(1)
            doc = ""
            j = i - 1
            if j >= 0 and lines[j].strip().endswith("*/"):
                doc_lines = []
                while j >= 0:
                    doc_lines.append(lines[j])
                    if '/**' in lines[j]:
                        break
                    j -= 1
                doc = "\n".join(reversed(doc_lines))
                doc = re.sub(r'^/\*\*|\*/$', '', doc, flags=re.MULTILINE).strip()

            brace_count = 0
            block_lines = []
            if '{' in line:
                brace_count = line.count('{') - line.count('}')
                block_lines.append(line)
            i += 1
            while i < n and brace_count > 0:
                block_lines.append(lines[i])
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1

            entries.append((method_name, doc, "\n".join(block_lines)))
            continue
        i += 1

    return entries

# Send prompt to local model
def run_model(prompt, model, in_file):
    url = "http://localhost:11434/api/generate"
    full_prompt = prompt + in_file
    data = {"model": model, "prompt": full_prompt, "stream": True}
    full_response = ""
    with requests.post(url, json=data) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break
    return full_response.strip()

# Classify file size to choose model
def File_classifier(in_file):
    count = 0
    with open(in_file, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("//") or "/*" in stripped or "*/" in stripped:
                continue
            if stripped:
                count += 1
    return "Gemma3:4b" if count >= 150 else "Gemma3:12b"

# Build prompt for a single method
def build_prompt(file_name, method_name, doc, block):
    stub = f"{method_name}({', '.join(re.findall(r'\\w+\\s+\\w+', block.splitlines()[0]))})"
    if doc:
        stub += "\n" + doc.replace("\n", " ")
    full_prompt = (
        "Example 1:\n"
        "  foo(int x)\n"
        "  @param x; the input value\n"
        "  @return int; the result doubled\n"
        "  Overview: doubles the input value.\n\n"
        "Example 2:\n"
        "  bar(String s)\n"
        "  @param s; the input string\n"
        "  @return String; uppercase version\n"
        "  Overview: converts string to uppercase.\n\n"
        f"Now document the method in:\n{file_name}\n{stub}"
    )
    return full_prompt

# Main runner
if __name__ == "__main__":
    source_dir = "Code-text"
    results = []

    for dirpath, _, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(".java"):
                continue

            path = os.path.join(dirpath, file)
            with open(path, encoding="utf-8") as f:
                java_text = f.read()

            class_match = class_pattern.search(java_text)
            class_name = class_match.group(1) if class_match else os.path.splitext(file)[0]
            model = File_classifier(path)

            methods = extract_methods_and_docs(java_text)
            for method_name, doc, block in methods:
                prompt = build_prompt(file, method_name, doc, block)
                print(f"Sending method '{method_name}' from class '{class_name}' to model...")
                ai_response = run_model(prompt, model, java_text)
                results.append({
                    "class name": class_name,
                    "function": method_name,
                    # "func_documentation": doc,
                    "func_block": block,
                    "response": ai_response
                })

    with open("ai_responses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"Wrote {len(results)} entries to ai_responses.json")
