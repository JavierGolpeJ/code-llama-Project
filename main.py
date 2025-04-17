import json
import os
import requests


#writes the LLM output to the text document
def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)

#runs the desired model with the given prompt we've engineered and gives the full code file as context
def run_model(prompt, model, in_file):
# def run_model(prompt, model, function):
    # URL of the Ollama model server (adjust as needed)
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
        output_response_dock(full_response)

# takes the file in and only counts lines of actual code excluding developer commentary
#if size of code is < 150 lines use smaller model
#if > 150 lines use larger model
def File_classifier(in_file):
    count = 0

    with open(in_file, "r") as in_file:

        for line in in_file:
            if "//" in line  or "/*" in line or "*/" in line:
                count = count
            else:
                count = count + 1

    if count >= 150:
        return "Gemma3:12b"
    else:
        return "Gemma3:4b"

# this is not function
# this section of code that uses a forloop to iterate over the elements in the methods array and
# direct them to the proper processing chain via if statement

if __name__ == "__main__":
    directory = "Code-text"
    our_prompt = "For each method in the given code write a general description of what the individual methods do as well as descriptions of the input and output parameters using the following structure \n{file name}\n{function name 1}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\n{function name 2}\n@param {variable name}; {description}\n@return {variable name}; {description}\nOverview: {general function description}\nComments: {previous user comments}\n\nInclude the original developer comments. We are not asking for suggestions or improvements, we are only asking for commentary explaining what the given code does. Must follow the given structure exactly. If you find yourself repeating the same thing over and over, move on to the next function."

    # iterate over files in the code directory
    for dir_path, _, files in os.walk(directory):
        for file in files:
            #if the file is a java file
            if file.endswith(".java"):
                #append the path
                path = os.path.join(dir_path, file)
                #run the model
                run_model(our_prompt, File_classifier(path), path)


# def get_all_functions(file_path):
#     function_blocks = []
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#
#     inside_function = False
#     current_function = []
#     brace_count = 0
#
#     # Loop through every line in the file.
#     for line in lines:
#         stripped = line.strip()
#
#         # If not in a function, look for a potential function signature.
#         # We check for common Java access modifiers and the presence of a parenthesis.
#         if not inside_function and (
#                 stripped.startswith("public") or stripped.startswith("private") or stripped.startswith(
#                 "protected")) and "(" in stripped:
#             # This is a potential start of a function.
#             inside_function = True
#             current_function.append(line)
#             brace_count += line.count("{") - line.count("}")
#             # If the opening brace is on the next line, we continue without any additional action.
#             continue
#
#         # If already inside a function, add the line to the current function block.
#         if inside_function:
#             current_function.append(line)
#             brace_count += line.count("{") - line.count("}")
#
#             # When brace_count returns to 0, we've found the end of the current function.
#             if brace_count == 0:
#                 function_blocks.append(''.join(current_function))
#                 current_function = []
#                 inside_function = False
#
#     return function_blocks


# testing new main
# if __name__ == "__main__":
#     directory = "Code-text"
#     # iterate over files in a directory that end with ".java"
#     for dir_path, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".java"):
#                 path = os.path.join(dir_path, file)
#                 functions = get_all_functions(path)
#                 print(f"\nFunctions in {file}:")
#                 for i, function in enumerate(functions, 1):
#                     print(f"\nFunction {i}:\n{function}")
#                     description(function, model, None)
#                     # parameters(function, model, None)
#                     # output(function, model, None)


# Original main
# if __name__ == "__main__":
#     model = "codellama:7b"
#     prompt_text = "Generate documentation for this code: "
#     # function_array = None
#     Context = None
#     directory = 'Code-text'
#
#     function_array = extract_code_from_directory(directory)
#     # print(function_array)
#
#     for filename, functions in function_array.items():
#         print(f"\nFile: {filename}")
#         for code in functions:
#             print(f"  Header: {code}")
#             output(code, model, None)
#             run_model(prompt_text, model, code,Context)

    # run_model(prompt_text, model, Context)
    # print("model is done running...")