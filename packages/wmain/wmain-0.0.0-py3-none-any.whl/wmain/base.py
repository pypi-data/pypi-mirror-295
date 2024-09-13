import os

def create_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
    
def create_path(file_path):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)