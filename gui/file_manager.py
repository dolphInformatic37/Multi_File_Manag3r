import tkinter as tk
from tkinter import filedialog

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestore di File")

        # Creazione di un frame principale
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Aggiunta di un pulsante per selezionare i file
        self.select_button = tk.Button(self.main_frame, text="Seleziona File", command=self.select_files)
        self.select_button.pack(pady=10)

        # Etichetta per visualizzare i percorsi dei file selezionati
        self.file_paths_label = tk.Label(self.main_frame, text="")
        self.file_paths_label.pack(pady=10)

        # Aggiunta di un'opzione per prefisso, infisso o suffisso
        self.action_var = tk.StringVar()
        self.action_var.set("prefix")  # Imposta il valore iniziale su prefisso
        self.prefix_radio = tk.Radiobutton(self.main_frame, text="Prefisso", variable=self.action_var, value="prefix")
        self.prefix_radio.pack(side=tk.LEFT, padx=5)
        self.infix_radio = tk.Radiobutton(self.main_frame, text="Infisso", variable=self.action_var, value="infix")
        self.infix_radio.pack(side=tk.LEFT, padx=5)
        self.suffix_radio = tk.Radiobutton(self.main_frame, text="Suffisso", variable=self.action_var, value="suffix")
        self.suffix_radio.pack(side=tk.LEFT, padx=5)

    def select_files(self):
        # Apre una finestra di dialogo per selezionare i file
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Visualizza i percorsi dei file selezionati
            self.file_paths_label.config(text="File selezionati:\n" + "\n".join(file_paths))

            # Applica l'azione selezionata ai file
            self.apply_action(file_paths)

    def apply_action(self, file_paths):
        # Ottieni l'azione selezionata
        action = self.action_var.get()

        # Esegui l'azione sui file selezionati
        for file_path in file_paths:
            new_file_path = self.apply_action_to_file(file_path, action)
            print("Nuovo percorso del file:", new_file_path)

    def apply_action_to_file(self, file_path, action):
        # Esegui l'azione sul nome del file
        path_parts = file_path.split("/")
        file_name = path_parts[-1]
        file_name_parts = file_name.split(".")
        file_name = file_name_parts[0]
        file_extension = file_name_parts[-1]

        if action == "prefix":
            new_file_name = "prefix_" + file_name
        elif action == "infix":
            new_file_name = file_name + "_infix"
        elif action == "suffix":
            new_file_name = file_name + "_suffix"

        new_file_name_with_extension = new_file_name + "." + file_extension
        path_parts[-1] = new_file_name_with_extension
        return "/".join(path_parts)

def main():
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
