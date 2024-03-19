import tkinter as tk
from Multi_File_Manag3r.main_window import MainWindow

def main():
    # Crea un'applicazione Tkinter
    root = tk.Tk()
    root.title("Il tuo titolo dell'applicazione")

    # Crea l'istanza della finestra principale dell'applicazione
    app = MainWindow(root)

    # Avvia il loop principale dell'applicazione Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
