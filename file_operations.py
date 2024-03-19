import os

def add_suffix_prefix_to_files(file_paths, text, option):
    """
    Aggiunge un prefisso o un suffisso ai file selezionati.
    
    Args:
        file_paths (list): Lista dei percorsi dei file selezionati.
        text (str): Testo del prefisso o del suffisso da aggiungere.
        option (str): Opzione per prefisso o suffisso.
        
    Returns:
        list: Lista dei percorsi dei file con il prefisso o il suffisso aggiunto.
    """
    modified_file_paths = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        base_name, extension = os.path.splitext(file_name)
        if option == "prefisso":
            new_name = f"{text}{base_name}{extension}"
        else:  # option == "suffisso"
            new_name = f"{base_name}{text}{extension}"
        modified_file_paths.append(new_name)
    return modified_file_paths