from traceback import print_exc

import requests

import json

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
    print(full_response)


# Todo
def output_response_dock(ai_response):
    pass

# Todo
def get_function_headers(file_path):
    function_headers = []

    with open(file_path, "r") as file:
        for line in file:
            if line.strip().startswith("def"):

                function_headers.append(line.strip(" :\n "))
    return function_headers

# Todo
def extract_function_info(file_content):
    pass

# Todo
def create_documentation_prompt(file_content):
    pass

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
"""

response = get_function_headers("test-1.txt")

print(response)
