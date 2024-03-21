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
    existing_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in file_paths]
    for file_path, existing_name in zip(file_paths, existing_names):
        directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        base_name, extension = os.path.splitext(file_name)
        new_name = base_name
        # Controlla se il nuovo nome esiste già nella directory
        if os.path.exists(os.path.join(directory, f"{new_name}{extension}")):
            # Se esiste, aggiungi un suffisso univoco
            i = 1
            while os.path.exists(os.path.join(directory, f"{new_name}_{i}{extension}")):
                i += 1
            new_name = f"{new_name}_{i}"
        if option == "prefisso":
            new_name = f"{text}{new_name}"
        else:  # option == "suffisso"
            new_name = f"{new_name}{text}"
        new_file_path = os.path.join(directory, f"{new_name}{extension}")
        modified_file_paths.append(new_file_path)
    return modified_file_paths
