# Funzione per ottenere l'estensione di un file
def get_file_extension(file_path):
    """
    Restituisce l'estensione di un file dato il percorso del file.
    
    Args:
        file_path (str): Il percorso del file.
        
    Returns:
        str: Estensione del file.
    """
    return os.path.splitext(file_path)[1]

# Costanti
MAX_SELECTED_FILES = 10
