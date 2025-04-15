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
    pass

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description to an output doc that meets are requirements
# as described in the proposal doc
def description(function, model, context):
    pass

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description of the parameters to an output doc that meets are requirements
# as described in the proposal doc
def parameters(function, model, context):
    pass

# Inputs = the full function, the model decided based off of the class, any context necessary(can be null)
# Output = NONE
# steps:
# 1. define the prompt
# 2. run model with prompt
# this take in the whole function and outs a description of the return values to an output doc that meets are requirements
# as described in the proposal doc
def output(function, model, context):
    pass

def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)

def run_model(prompt):
    # URL of the Ollama model server (adjust as needed)
    url = "http://localhost:11434/api/generate"

    full_response = ""
    data = {"model": "codellama:7b", "prompt": prompt, "stream": True}
    with requests.post(url, json=data) as response:
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                full_response += json_line.get("response", "")
                if json_line.get("done", False):
                    break
    # outputs to doc
    output_response_dock(full_response)


# this function takes in java/ python code file and collects all of the methods and classes within the code file
# and stores them within an array


# Todo
def output_response_dock(ai_response):
    pass

# Todo
def get_function_headers(file_path, directory_name):
    path = os.path.join(directory_name, file_path)
    function_headers = []

    with open(path, "r") as file:
        for line in file:
            if line.strip().startswith("public"):
                function_headers.append(line.strip(" :\n "))
    return function_headers


def extract_headers_from_directory(directory_name):
    all_headers = {}

    for dir_path, dir_names ,files in os.walk(directory_name):
        for file in files:
            if file.endswith(".java"):
                relative_path = os.path.relpath(os.path.join(dir_path, file), directory_name)
                headers = get_function_headers(relative_path, directory_name)
                if headers:
                    all_headers[relative_path] = headers

    return all_headers
  
# need a global array of functions:
# function_array =
# conext_array = any class/ interfaces

def get_Functions(file_name, function_array):
    with open(file_name, "r") as file:
        content = file.read()
        print("gets to the file")
        # print(content)
    return content

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

# Example usage:
# if __name__ == "__main__":
#     prompt_text = """ give me code comments for this code in this format at the top of each function:
#     @param
#     @feature
#     @return
#
#     code starts here:
#     def fibonacci_sequence(n):
#     a, b = 0, 1
#     if n <= 0:
#         return []
#     elif n == 1:
#         return [0]
#     else:
#         result = [0, 1]
#         while len(result) < n:
#             next_num = a + b
#             if next_num < n:
#                 result.append(next_num)
#                 a, b = b, next_num
#             else:
#                 break
#         return result
#     """
#     # prompt_text = "i want you to make comments for this code: \n" + get_code("test-1.txt")
#     # print(prompt_text)
#     run_model(prompt_text)
#     print("model is done running...")

prompt_text = """
    def fibonacci_sequence(n):
    a, b = 0, 1
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    else:
        result = [0, 1]
        while len(result) < n:
            next_num = a + b
            if next_num < n:
                result.append(next_num)
                a, b = b, next_num
            else:
                break
        return result

# response = get_function_headers()
# print(response)

directory = 'Code-text'
headers_by_file = extract_headers_from_directory(directory)
print(headers_by_file)
    """
    # prompt_text = "i want you to make comments for this code: \n" + get_code("test-1.txt")
    # print(prompt_text)

    run_model(prompt_text)
    print("model is done running...")

