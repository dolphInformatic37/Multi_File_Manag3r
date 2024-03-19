import os

def add_suffix_prefix_to_files(file_paths, prefix="", suffix=""):
    try:
        for file_path in file_paths:
            file_dir, file_name = os.path.split(file_path)
            new_file_name = f"{prefix}{file_name}{suffix}"
            new_file_path = os.path.join(file_dir, new_file_name)
            os.rename(file_path, new_file_path)
        return True, "Suffix/Prefix added successfully."
    except Exception as e:
        return False, str(e)
