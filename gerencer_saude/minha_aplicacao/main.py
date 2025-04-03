import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Importando os módulos do aplicativo
from gerencer_saude.features.perfil import PerfilManager
from gerencer_saude.features.medidas import MedidasManager
from gerencer_saude.features.medicamentos import MedicamentosManager
from gerencer_saude.features.atividades import AtividadesManager
from gerencer_saude.features.consultas import ConsultasApp

class HealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Saúde Pessoal")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")
        
        # Configuração de estilo
        self.configure_style()
        
        # Criação dos gerenciadores
        self.data_file = "dados_saude.json"
        self.carregar_dados()
        
        self.perfil_manager = PerfilManager(self.dados)
        self.medidas_manager = MedidasManager(self.dados)
        self.medicamentos_manager = MedicamentosManager(self.dados)
        self.atividades_manager = AtividadesManager(self.dados)
        self.consultas_manager = ConsultasApp(self.root)
        
        # Criação da interface
        self.criar_interface()
     
    
    def configure_style(self):
        # Configura o estilo dos widgets
        style = ttk.Style()
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TNotebook", background="#f0f4f8", borderwidth=0)
        style.configure("TNotebook.Tab", background="#dde6f0", padding=[12, 6], font=('Arial', 10))
        style.map("TNotebook.Tab", background=[("selected", "#3498db")],
                  foreground=[("selected", "#ffffff")])
        style.configure("TButton", background="#3498db", foreground="#ffffff", 
                       padding=10, font=('Arial', 10, 'bold'))
        style.configure("TLabel", background="#f0f4f8", font=('Arial', 10))
        style.configure("Title.TLabel", background="#f0f4f8", font=('Arial', 16, 'bold'))
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(main_frame, text="Gerenciador de Saúde Pessoal", style="Title.TLabel")
        titulo.pack(pady=10)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Aba de Perfil
        perfil_frame = self.perfil_manager.criar_frame(self.notebook)
        self.notebook.add(perfil_frame, text="Perfil")
        
        # Aba de Medidas
        medidas_frame = self.medidas_manager.criar_frame(self.notebook, self.salvar_dados)
        self.notebook.add(medidas_frame, text="Medidas")
        
        # Aba de Medicamentos
        medicamentos_frame = self.medicamentos_manager.criar_frame(self.notebook, self.salvar_dados)
        self.notebook.add(medicamentos_frame, text="Medicamentos")
        
        # Aba de Atividades Físicas
        atividades_frame = self.atividades_manager.criar_frame(self.notebook, self.salvar_dados)
        self.notebook.add(atividades_frame, text="Atividades Físicas")
        
        # Aba de Consultas Médicas
        consultas_frame = self.consultas_manager.criar_frame(self.notebook, self.salvar_dados)
        self.notebook.add(consultas_frame, text="Consultas Médicas")
        
        # Botão para salvar os dados
        btn_salvar = ttk.Button(main_frame, text="Salvar Todas as Alterações", 
                               command=self.salvar_dados)
        btn_salvar.pack(pady=10)
    
    def carregar_dados(self):
        # Carrega os dados do arquivo JSON ou cria uma estrutura de dados vazia
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.dados = json.load(f)
            except:
                self.criar_estrutura_dados()
        else:
            self.criar_estrutura_dados()
    
    def criar_estrutura_dados(self):
        # Cria uma estrutura de dados vazia
        self.dados = {
            "perfil": {
                "nome": "",
                "idade": "",
                "altura": "",
                "genero": "",
                "condicoes_medicas": ""
            },
            "medidas": [],
            "medicamentos": [],
            "atividades": [],
            "consultas": []
        }
    
    def salvar_dados(self):
        # Salva os dados no arquivo JSON
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthApp(root)
    root.mainloop()