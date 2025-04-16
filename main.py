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
    prompt = ("For the following function, if there is already a comment then retype it but do not"
              "change the comment in any way. So basically just show me the unaltered comment\n")
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
        "For the following function, give me what the function outputs / returns. If there is no return value then simply say 'There is not return value"
        "for this function'. If there is then you must follow this Strict Format: '@return {variable name} {variable description}'\n"
    )
    run_model(prompt, model, function, context)


def output_response_dock(ai_response):
    with open("test-output.txt", "a") as file:
        file.write(ai_response)


def run_model(prompt, model, function, context):
    # URL of the Ollama model server (adjust as needed)
    url = "http://localhost:11434/api/generate"

    Full_prompt = prompt + function + context
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


def get_Functions(file_name, function_array, directory_name):
    with open(file_name, "r") as file:
        content = file.read()
        print("gets to the file")
        # print(content)
    return content


# gets all functions header that starts with public from java file
def get_function_headers(file_path, directory_name):
    path = os.path.join(directory_name, file_path)
    function_headers = []

    with open(path, "r") as file:
        for line in file:
            if line.strip().startswith("public"):
                function_headers.append(line.strip(" :\n "))
    return function_headers


# gets all files the .java extention
def extract_headers_from_directory(directory_name):
    all_headers = {}

    for dir_path, dir_names, files in os.walk(directory_name):
        for file in files:
            if file.endswith(".java"):
                relative_path = os.path.relpath(os.path.join(dir_path, file), directory_name)
                headers = get_function_headers(relative_path, directory_name)
                if headers:
                    all_headers[relative_path] = headers

    return all_headers


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
if __name__ == "__main__":
    prompt_text = None
    function_array = None
    Context = None

    get_Functions()

    for functions in function_array:
        pass

    run_model(prompt_text)
    print("model is done running...")
