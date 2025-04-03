import tkinter as tk
from tkinter import ttk
import os
from gerencer_saude.core.config import APP_TITULO, APP_LARGURA, APP_ALTURA, APP_REDIMENSIONAR, CORES
from gerencer_saude.core.utils import verificar_diretorio
from gerencer_saude.ui.menu import MenuPrincipal

class App:
    def __init__(self, root):
        self.root = root
        self.configurar_janela()
        self.inicializar_app()
    
    def configurar_janela(self):
        # Configurar a janela principal
        self.root.title(APP_TITULO)
        self.root.geometry(f"{APP_LARGURA}x{APP_ALTURA}")
        self.root.resizable(APP_REDIMENSIONAR, APP_REDIMENSIONAR)
        
        # Centralizar na tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela - APP_LARGURA) // 2
        y = (altura_tela - APP_ALTURA) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Configurar cores
        self.root.configure(bg=CORES["fundo"])
        
        # Configurar estilo para widgets ttk
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar estilos para Treeview (tabelas)
        style.configure("Treeview", 
                        background=CORES["fundo_card"],
                        foreground=CORES["texto"],
                        rowheight=25,
                        fieldbackground=CORES["fundo_card"])
        style.configure("Treeview.Heading", 
                       font=('Helvetica', 10, 'bold'),
                       background=CORES["primaria"],
                       foreground="white")
        style.map('Treeview', background=[('selected', CORES["secundaria"])])
    
    def inicializar_app(self):
        # Garantir que o diretório de dados existe
        verificar_diretorio()
        
        # Exibir o menu principal
        self.menu_principal = MenuPrincipal(self.root)
        self.menu_principal.exibir()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()