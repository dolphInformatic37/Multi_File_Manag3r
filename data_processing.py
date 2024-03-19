import os

def sort_files_by_name(file_paths):
    
    return sorted(file_paths, key=lambda x: os.path.basename(x))

