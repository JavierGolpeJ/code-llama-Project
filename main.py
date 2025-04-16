from lib2to3.fixes.fix_input import context
from traceback import print_exc

import requests
import os
import json

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# pull out preveus comments and sends them to output doc
def prec_comment(function, model, context):
    prompt = "For the following function, Ignor all the comments that are already there \n"
    run_model(prompt, model, function, context)

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description to an output doc that meets are requirements
# as described in the proposal doc
def description(function, model, context):
        prompt = ("For the following function, give me an overall description of what this function does for the code. "
                  " Must follow this Strict Format: '@param: {description of function}' \n")
        run_model(prompt, model, function, context)
# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description of the parameters to an output doc that meets are requirements
# as described in the proposal doc
def parameters(function, model, context):
    prompt = (
        "For the following function, give me a list of the parameters/ inputs used along with a short description of what they represent."
        "and for each parameter it must start with @param. Must follow this Strict Format: '@param: {variable name} {variable description of what it represents/ does}' and nothing else\n"
    )
    run_model(prompt, model, function, context)

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description of the return values to an output doc that meets are requirements
# as described in the proposal doc
def output(function, model, context):
    prompt = (
        "For the following function, give me a what the function funtionn output / rerturn. If there is no return value then simply say 'There is not return value"
        "for this function'. If there is then you must follow this Strict Format: '@return {variable name} {variable description'\n"
    )

    run_model(prompt, model, function, context)

def write_code_to_file(code):
    with open("test-output.txt", "a") as f:
        f.write("\n" + code)

def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)

def run_model(prompt, model, function,  context):
# def run_model(prompt, model, function):
    # URL of the Ollama model server (adjust as needed)
    url = "http://localhost:11434/api/generate"

    Full_prompt = prompt + function
    full_response = ""

    data = {"model": model, "prompt": Full_prompt, "stream": True}
    with requests.post(url, json=data) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break

    # outputs to doc
        output_response_dock(full_response)
        write_code_to_file(function)


# this function takes in java/ python code file and collects all of the methods and classes within the code file
# and stores them within an array

# Todo
# def get_function_headers(file_path, directory_name):
#     path = os.path.join(directory_name, file_path)
#     # function_headers = []
#     function_code = []
#
#     with open(path, "r") as file:
    #     for line in file:
    #         stripped = line.strip()
    #         if stripped.startswith("public class"):
    #             continue
    #         if line.strip().startswith("public") and (line.strip().endswith("}")):
    #             function_headers.append(line.strip(" {\n "))
    # return function_headers


def get_function_code(file_path, directory_name):
    path = os.path.join(directory_name, file_path)
    function_lines = []
    inside_function = False
    brace_count = 0
    with open(path, "r") as file:
        for line in file:
            stripped = line.strip()

            if stripped.startswith("public class"):
                continue
            if not inside_function and (stripped.startswith("public") and stripped.endswith("{")):
                inside_function = True

            if inside_function:
                function_lines.append(line)

                brace_count += line.count("{")
                brace_count -= line.count("}")

                if brace_count == 0:
                    break

    return ''.join(function_lines)

def extract_code_from_directory(directory_name):
    all_headers = {}

    for dir_path, dir_names ,files in os.walk(directory_name):
        for file in files:
            if file.endswith(".java"):
                relative_path = os.path.relpath(os.path.join(dir_path, file), directory_name)
                headers = get_function_code(relative_path, directory_name)
                if headers:
                    all_headers[relative_path] = headers

    return all_headers
  
# need a global array of functions:
# function_array =
# conext_array = any class/ interfaces


# does the something as get function but gathers user defined class and interfaces.
def get_contex(file_name, conext_array):
    pass

# this function take as imput the array of methods and classes. And clasifies base on there level of complexity.
#  *We must determine criteria for complexity levels*
def Method_classifier(function_array):
    for functions in function_array:
        pass

# this is not function
# this section of code that uses a forloop to iterate over the elements in the methods array and
# direct them to the proper processing chain via if statement

# if function is:
# class = 1 then use the smallest model.
    # **EACH OF THESE FUNCTION GET THE WHOLE BODY OF TEXT**
    # run pre comment function
    # run overall description function
    # run impute parameters function
    # run output value function
# class = 2 then use small model and pass in necessary context
    # **EACH OF THESE FUNCTION GET THE WHOLE BODY OF TEXT**
    # run pre comment function
    # run overall description function
    # run impute parameters function
    # run output value function
# class = 3 then use big model
    # **EACH OF THESE FUNCTION GET THE WHOLE BODY OF TEXT**
    # run pre comment function
    # run overall description function
    # run impute parameters function
    # run output value function
# class = 4 then use big and pass in necessary context
    # **EACH OF THESE FUNCTION GET THE WHOLE BODY OF TEXT**
    # run pre comment function
    # run overall description function
    # run impute parameters function
    # run output value function

# print 3 blank lines to output doc for next function

def get_all_functions(file_path):
    function_blocks = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    inside_function = False
    current_function = []
    brace_count = 0

    # Loop through every line in the file.
    for line in lines:
        stripped = line.strip()

        # If not in a function, look for a potential function signature.
        # We check for common Java access modifiers and the presence of a parenthesis.
        if not inside_function and (
                stripped.startswith("public") or stripped.startswith("private") or stripped.startswith(
                "protected")) and "(" in stripped:
            # This is a potential start of a function.
            inside_function = True
            current_function.append(line)
            brace_count += line.count("{") - line.count("}")
            # If the opening brace is on the next line, we continue without any additional action.
            continue

        # If already inside a function, add the line to the current function block.
        if inside_function:
            current_function.append(line)
            brace_count += line.count("{") - line.count("}")

            # When brace_count returns to 0, we've found the end of the current function.
            if brace_count == 0:
                function_blocks.append(''.join(current_function))
                current_function = []
                inside_function = False

    return function_blocks


# testing new main
if __name__ == "__main__":
    model = "codellama:7b"
    directory = "Code-text"
    # iterate over files in a directory that end with ".java"
    for dir_path, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                path = os.path.join(dir_path, file)
                functions = get_all_functions(path)
                print(f"\nFunctions in {file}:")
                for i, function in enumerate(functions, 1):
                    print(f"\nFunction {i}:\n{function}")
                    description(function, model, None)
                    # parameters(function, model, None)
                    # output(function, model, None)


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