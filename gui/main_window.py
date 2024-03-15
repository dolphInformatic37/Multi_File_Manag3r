import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Finestra Principale")
        
        # Creazione di un frame principale
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=300, pady=300)
        
        # Aggiunta di un'etichetta
        self.label = tk.Label(self.main_frame, text="Benvenuto nella Finestra Principale")
        self.label.pack(pady=10)
        
        # Aggiunta di un pulsante
        self.button = tk.Button(self.main_frame, text="Premi qui", command=self.on_button_click)
        self.button.pack(pady=10)
    
    def on_button_click(self):
        # Azione da eseguire quando il pulsante viene premuto
        self.label.config(text="Hai premuto il pulsante!")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
