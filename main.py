import tkinter as tk

from file_manager import FileManagerApp
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Finestra Principale")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=200, pady=100)
        
        self.label = tk.Label(self.main_frame, text="Benvenuto nella Finestra Principale")
        self.label.pack(pady=10)
        
        self.button = tk.Button(self.main_frame, text="Apri Gestore di File", command=self.open_file_manager)
        self.button.pack(pady=10)

    def open_file_manager(self):
        # Nasconde temporaneamente la finestra principale
        self.root.withdraw()
        # Crea una nuova finestra per il FileManagerApp
        file_manager_window = tk.Toplevel()
        file_manager_window.title("Gestore di File")
        FileManagerApp(file_manager_window)
        
        # Attende che la nuova finestra venga chiusa per riaprire la finestra principale
        file_manager_window.wait_window()
        self.root.deiconify()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()