import os
import tkinter as tk
from tkinter import ttk, filedialog
from Multi_File_Manag3r.file_operations import add_suffix_prefix_to_files
from Multi_File_Manag3r.data_processing import sort_files_by_name

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestore di File")
        self.root.geometry('1200x600')  # Dimensioni della finestra

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Dizionario per mappare i nomi dei file ai loro percorsi
        self.file_path_map = {}

        # Treeview per mostrare i file selezionati
        self.file_tree = ttk.Treeview(self.main_frame, columns=('colonna 1', 'colonna 2'), show='headings')
        self.file_tree.heading('colonna 1', text='Nome attuale del file')
        self.file_tree.heading('colonna 2', text='Nuovo Nome')
        # Imposta la larghezza delle colonne
        self.file_tree.column('colonna 1', width=375)  # Imposta la larghezza della colonna 'colonna 1'
        self.file_tree.column('colonna 2', width=375)  # Imposta la larghezza della colonna 'colonna 2'
        # Imposta l'altezza iniziale del Treeview
        self.file_tree['height'] = 10  # Mostra massimo 10 elementi
        # Scrollbar verticale
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack_forget()  # Nascondi lo scrollbar all'inizio
        self.file_tree.pack(pady=10)

        # Frame per la parte superiore (entry e pulsante Applica Modifiche)
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=20)

        # Entry per modifiche ai nomi dei file e per inserire il suffisso/prefisso
        self.suffix_prefix_entry = tk.Entry(top_frame)
        self.suffix_prefix_entry.pack(padx=10)

        # Etichetta per la scelta prefisso/suffisso
        self.suffix_prefix_label = tk.Label(top_frame, text="Scegli tra prefisso e suffisso:")
        self.suffix_prefix_label.pack(padx=10, pady=(10, 0))

        # Variabile per tenere traccia della scelta prefisso/suffisso
        self.selected_option = tk.StringVar(value="prefisso")

        # Pulsanti di opzione per prefisso/suffisso
        self.prefix_radio = tk.Radiobutton(top_frame, text="Prefisso", variable=self.selected_option, value="prefisso")
        self.prefix_radio.pack(padx=10)
        self.suffix_radio = tk.Radiobutton(top_frame, text="Suffisso", variable=self.selected_option, value="suffisso")
        self.suffix_radio.pack(padx=10)

        # Bottone per applicare le modifiche
        self.apply_change_button = tk.Button(top_frame, text="Applica Modifiche", command=self.apply_changes)
        self.apply_change_button.pack(padx=10, pady=(10, 0))

        # Frame per la parte inferiore (seleziona file e rimuovi selezionato)
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(side=tk.TOP, pady=10)

        # Bottone per selezionare i file
        self.select_button = tk.Button(bottom_frame, text="Seleziona File", command=self.select_files)
        self.select_button.pack(side=tk.LEFT, padx=10)

        # Bottone per rimuovere il file selezionato
        self.remove_button = tk.Button(bottom_frame, text="Rimuovi File Selezionato", command=self.remove_selected)
        self.remove_button.pack(side=tk.RIGHT, padx=10)

        # Bottone per tornare alla schermata principale
        self.back_button = tk.Button(self.main_frame, text="Torna alla schermata principale", command=self.root.destroy)
        self.back_button.pack(side=tk.BOTTOM, pady=20)

    def select_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Ordina i file selezionati in ordine alfabetico
            file_paths_sorted = sort_files_by_name(file_paths)
            for file_path in file_paths_sorted:
                file_name = os.path.basename(file_path)
                if file_name in self.file_path_map:
                    base_name, ext = os.path.splitext(file_name)
                    i = 1
                    new_file_name = f"{base_name}_{i}{ext}"
                    while new_file_name in self.file_path_map:
                        i += 1
                        new_file_name = f"{base_name}_{i}{ext}"
                    file_name = new_file_name
                self.file_path_map[file_name] = file_path
                self.file_tree.insert('', tk.END, values=(file_name, ''))

            # Imposta l'altezza del Treeview in base al numero di file selezionati
            num_files = len(self.file_tree.get_children())
            if num_files > 10:
                self.file_tree['height'] = 10  # Limita il numero di righe visualizzate a 10
                self.scrollbar.pack(side='right', fill='y') # Mostra lo scrollbar
            else:
                self.file_tree['height'] = num_files + 1 # Seleziona il numero di righe nella Treeview
                self.scrollbar.pack_forget() # Nascondi lo scrollbar quando non è necessario

    def apply_changes(self):
        for selected_item in self.file_tree.selection():
            file_path = self.file_tree.item(selected_item)['values'][0]
            new_name = self.suffix_prefix_entry.get()
            option = self.selected_option.get()  # Ottieni l'opzione selezionata
            if option == "prefisso":
                new_name = f"{new_name}{file_path}"
            else:  # Se l'opzione è suffisso
                base_name, extension = os.path.splitext(file_path)
                new_name = f"{base_name}{new_name}{extension}"
            self.file_tree.item(selected_item, values=(file_path, new_name))

    def remove_selected(self):
        for selected_item in self.file_tree.selection():
            self.file_tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    FileManagerApp(root)
    root.mainloop()