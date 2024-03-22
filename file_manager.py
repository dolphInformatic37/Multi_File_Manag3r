import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from file_operations import add_suffix_prefix_to_files

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

        # Variabile per tenere traccia del valore precedente della Entry
        self.previous_entry_value = tk.StringVar(value="")  # Inizialmente vuoto

        # Aggiungi una funzione di callback per aggiornare l'anteprima in tempo reale
        self.suffix_prefix_entry.bind("<KeyRelease>", self.update_preview)

        # Variabile per tenere traccia delle modifiche proposte
        self.proposed_changes = {}

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
        self.apply_change_button = tk.Button(top_frame, text="Applica Modifiche", command=self.confirm_changes)
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
        """
        Permette all'utente di selezionare i file e li aggiunge alla Treeview.
        """
        # Verifica se la finestra di dialogo è già aperta
        if getattr(self, "_file_dialog_open", False):
            # Mostra un messaggio informativo se la finestra di dialogo è già aperta
            messagebox.showinfo("Finestra di selezione già aperta", "La finestra per la selezione dei file è già aperta.")
            return

        # Imposta la variabile di controllo per indicare che la finestra di dialogo è aperta
        self._file_dialog_open = True

        # Crea la finestra di dialogo per la selezione dei file
        file_paths = filedialog.askopenfilenames()

        # Ripristina la variabile di controllo dopo la chiusura della finestra di dialogo
        self._file_dialog_open = False

        if file_paths:
            # Lista per tenere traccia dei nomi dei file duplicati
            duplicate_files = []

            for file_path in file_paths:
                file_name = os.path.basename(file_path)

                # Controlla se il file è già presente
                if file_name in self.file_path_map:
                    duplicate_files.append(file_name)
                    continue

                # Altrimenti, aggiungi il file alla Treeview
                self.file_path_map[file_name] = file_path
                self.file_tree.insert('', tk.END, values=(file_name, ''))

            # Aggiorna l'anteprima delle modifiche
            self.update_preview(None)

            # Se ci sono nomi duplicati, mostra una finestra pop-up
            if duplicate_files:
                self.show_duplicate_files_popup(duplicate_files)

            # Aggiorna l'altezza della Treeview
            self.update_treeview_height()

    def get_unique_file_name(self, base_name, ext):
        """
        Restituisce un nome di file unico evitando duplicati.

        Args:
            base_name (str): Nome di base del file.
            ext (str): Estensione del file.

        Returns:
            str: Nome di file unico.
        """
        new_file_name = f"{base_name}{ext}"
        i = 1
        while new_file_name in self.file_path_map:
            new_file_name = f"{base_name}_{i}{ext}"
            i += 1
        return new_file_name
    
    def show_duplicate_files_popup(self, duplicate_files):
        """
        Mostra una finestra pop-up per avvertire l'utente dei file duplicati.
        
        Args:
            duplicate_files (list): Lista dei nomi dei file duplicati.
        """
        message = "I seguenti file sono già stati selezionati:\n\n"
        for file_name in duplicate_files:
            message += f"- {file_name}\n"
        messagebox.showwarning("File duplicati", message)
    
    def update_treeview_height(self):
        """
        Aggiorna l'altezza della Treeview in base al numero di file rimanenti.
        """
        num_files = len(self.file_tree.get_children())
        if num_files > 10:
            self.file_tree['height'] = 10  # Limita il numero di righe visualizzate a 10
            self.scrollbar.pack(side='right', fill='y')  # Mostra lo scrollbar
        else:
            self.file_tree['height'] = num_files + 1  # Seleziona il numero di righe nella Treeview
            self.scrollbar.pack_forget()  # Nascondi lo scrollbar quando non è necessario

    def update_preview(self, event):
        # Ottieni il testo inserito nella Entry
        text = self.suffix_prefix_entry.get()

        # Ottieni l'opzione selezionata
        option = self.selected_option.get()

        # Aggiorna l'anteprima delle modifiche
        for item_id in self.file_tree.get_children():
            old_name = self.file_tree.item(item_id, "values")[0]
            new_name = ""

            # Applica le modifiche proposte in base all'opzione selezionata
            if option == "prefisso":
                new_name = f"{text}{old_name}"
            else:  # option == "suffisso"
                base_name, extension = os.path.splitext(old_name)
                new_name = f"{base_name}{text}{extension}"

            # Aggiorna l'anteprima delle modifiche direttamente nella Treeview
            self.file_tree.item(item_id, values=(old_name, new_name))

            # Aggiorna il dizionario delle modifiche proposte
            self.proposed_changes[item_id] = (old_name, new_name)

    def confirm_changes(self):
        # Controlla se ci sono file selezionati nella Treeview
        if not self.file_tree.get_children():
            messagebox.showwarning("Nessun file selezionato", "Non ci sono file da modificare.")
            return

        # Crea una finestra di conferma e memorizzala come attributo dell'istanza
        self.confirmation_window = tk.Toplevel(self.root)
        self.confirmation_window.title("Conferma modifiche")

        # Etichetta di conferma
        confirmation_label = tk.Label(self.confirmation_window, text="Vuoi confermare le modifiche?")
        confirmation_label.pack(padx=80, pady=20)

        # Frame per i pulsanti
        button_frame = tk.Frame(self.confirmation_window)
        button_frame.pack(padx=20, pady=10)

        # Bottone per confermare
        confirm_button = tk.Button(button_frame, text=" Si ", command=self.apply_changes_and_close_confirmation)
        confirm_button.pack(side=tk.LEFT, padx=10)

        # Bottone per annullare
        cancel_button = tk.Button(button_frame, text=" No ", command=self.confirmation_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def apply_changes_and_close_confirmation(self):
        # Chiudi la finestra di conferma delle modifiche
        self.confirmation_window.destroy()

        # Chiamata alla funzione per applicare le modifiche
        self.apply_changes()

    def apply_changes(self):
        # Ottieni il testo inserito nell'Entry per prefisso/suffisso
        text = self.suffix_prefix_entry.get()

        # Verifica se la casella di testo è vuota
        if not text:
            messagebox.showwarning("Nessuna modifica", "Inserisci un prefisso o un suffisso prima di applicare le modifiche.")
            return

        # Ottieni l'opzione selezionata per prefisso/suffisso
        option = self.selected_option.get()

        # Crea una lista di percorsi dei file selezionati
        file_paths = list(self.file_path_map.values())

        # Applica i prefissi o i suffissi ai nomi dei file utilizzando la funzione definita nell'altro script
        modified_file_paths = add_suffix_prefix_to_files(file_paths, text, option)

        # Aggiorna la visualizzazione nella Treeview con i nuovi nomi dei file
        for item_id, new_file_path in zip(self.file_tree.get_children(), modified_file_paths):
            old_name = self.file_tree.item(item_id, "values")[0]
            self.file_tree.item(item_id, values=(old_name, os.path.basename(new_file_path)))
            
        # Mostra un messaggio informativo
        messagebox.showinfo("Modifiche applicate", "Le modifiche sono state applicate con successo.")

        # Resetta il dizionario delle modifiche proposte
        self.proposed_changes = {}

    def remove_selected(self):
        """
        Rimuove i file selezionati dalla Treeview.
        """
        for selected_item in self.file_tree.selection():
            self.file_tree.delete(selected_item)

        # Aggiorna l'altezza della Treeview dopo la rimozione dei file
        self.update_treeview_height()