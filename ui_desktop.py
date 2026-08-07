import tkinter as tk
from tkinter import ttk
from src.desktop.ui import AgenciaApp

if __name__ == "__main__":
    root = tk.Tk()
    
    # Aplica um tema mais moderno do Tkinter
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
        
    app = AgenciaApp(root)
    root.mainloop()