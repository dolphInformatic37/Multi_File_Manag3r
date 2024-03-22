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
        directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        base_name, extension = os.path.splitext(file_name)
        new_name = base_name
        if option == "prefisso":
            new_name = f"{text}{new_name}"
        else:  # option == "suffisso"
            new_name = f"{new_name}{text}"
        new_file_path = os.path.join(directory, f"{new_name}{extension}")
        # Verifica se il nuovo nome esiste già nella directory
        if os.path.exists(new_file_path):
            i = 1
            while True:
                new_name_with_suffix = f"{new_name}_{i}"
                new_file_path_with_suffix = os.path.join(directory, f"{new_name_with_suffix}{extension}")
                if not os.path.exists(new_file_path_with_suffix):
                    new_name = new_name_with_suffix
                    new_file_path = new_file_path_with_suffix
                    break
                i += 1
        # Rinomina effettivamente il file sul disco
        os.rename(file_path, new_file_path)
        modified_file_paths.append(new_file_path)
    return modified_file_paths