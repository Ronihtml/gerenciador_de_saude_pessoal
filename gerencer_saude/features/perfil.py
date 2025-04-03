import tkinter as tk
from tkinter import ttk

class PerfilManager:
    def __init__(self, dados):
        self.dados = dados
    
    def criar_frame(self, parent):
        frame = ttk.Frame(parent)
        
        # Título da seção
        ttk.Label(frame, text="Seu Perfil de Saúde", font=('Arial', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=20, padx=20, sticky=tk.W)
        
        # Campos do perfil
        campos = [
            ("Nome:", "nome"),
            ("Idade:", "idade"),
            ("Altura (cm):", "altura"),
            ("Gênero:", "genero")
        ]
        
        # Criação dos campos de entrada
        self.entries = {}
        
        for i, (label_text, field) in enumerate(campos):
            ttk.Label(frame, text=label_text).grid(row=i+1, column=0, padx=20, pady=10, sticky=tk.W)
            self.entries[field] = ttk.Entry(frame, width=40)
            self.entries[field].grid(row=i+1, column=1, padx=20, pady=10, sticky=tk.W)
            
            # Preenche os campos com dados existentes
            if self.dados["perfil"][field]:
                self.entries[field].insert(0, self.dados["perfil"][field])
        
        # Campo para condições médicas (texto maior)
        ttk.Label(frame, text="Condições Médicas:").grid(
            row=len(campos)+1, column=0, padx=20, pady=10, sticky=tk.NW)
        
        self.entries["condicoes_medicas"] = tk.Text(frame, width=40, height=8)
        self.entries["condicoes_medicas"].grid(
            row=len(campos)+1, column=1, padx=20, pady=10, sticky=tk.W)
        
        # Preenche o campo de condições médicas
        if self.dados["perfil"]["condicoes_medicas"]:
            self.entries["condicoes_medicas"].insert("1.0", self.dados["perfil"]["condicoes_medicas"])
        
        # Botão para atualizar os dados
        ttk.Button(frame, text="Atualizar Perfil", command=self.atualizar_perfil).grid(
            row=len(campos)+2, column=0, columnspan=2, pady=20)
        
        return frame
    
    def atualizar_perfil(self):
        # Atualiza os dados do perfil
        for field in ["nome", "idade", "altura", "genero"]:
            self.dados["perfil"][field] = self.entries[field].get()
        
        # Atualiza o campo de condições médicas
        self.dados["perfil"]["condicoes_medicas"] = self.entries["condicoes_medicas"].get("1.0", tk.END).strip()