import os

def get_input_file_from_script_file(script_file: str):
    path = os.path.join(os.path.dirname(script_file), "../input.txt")
    
    return open(path, "r")