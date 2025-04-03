import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import csv
import os
import datetime

from gerencer_saude.ui.styles import apply_style
from gerencer_saude.core.utils import load_data

class ExportModule:
    def __init__(self, parent, user_data, callback_func):
        self.parent = parent
        self.user_data = user_data
        self.callback_func = callback_func
        
        self.frame = ttk.Frame(parent)
        apply_style(self.frame, "export")
        
        self.export_format = tk.StringVar(value="json")
        self.selected_data = {}
        self.initialize_selected_data()
        
        self.create_widgets()
    
    def initialize_selected_data(self):
        # Inicializa a seleção de dados para exportação
        self.selected_data = {
            "perfil": tk.BooleanVar(value=True),
            "medidas": tk.BooleanVar(value=True),
            "medicamentos": tk.BooleanVar(value=True),
            "consultas": tk.BooleanVar(value=True),
            "atividades": tk.BooleanVar(value=True)
        }
    
    def create_widgets(self):
        # Título
        title_label = ttk.Label(self.frame, text="Exportar Dados", 
                               font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, padx=20)
        
        # Descrição
        description = ttk.Label(self.frame, 
                              text="Selecione os dados que deseja exportar e o formato de arquivo.")
        description.grid(row=1, column=0, columnspan=3, pady=5, padx=20, sticky="w")
        
        # Seleção de dados
        data_frame = ttk.LabelFrame(self.frame, text="Dados para Exportação")
        data_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=20, sticky="nsew")
        
        # Checkboxes para seleção de dados
        for i, (key, var) in enumerate(self.selected_data.items()):
            ttk.Checkbutton(data_frame, text=key.capitalize(), variable=var).grid(
                row=i, column=0, sticky="w", padx=10, pady=5)
        
        # Opções de formato
        format_frame = ttk.LabelFrame(self.frame, text="Formato de Exportação")
        format_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky="nsew")
        
        ttk.Radiobutton(format_frame, text="JSON", value="json", 
                       variable=self.export_format).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Radiobutton(format_frame, text="CSV", value="csv", 
                       variable=self.export_format).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Radiobutton(format_frame, text="Texto simples", value="txt", 
                       variable=self.export_format).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        # Botões de ação
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)
        
        ttk.Button(button_frame, text="Exportar", command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Selecionar Todos", 
                  command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Desmarcar Todos", 
                  command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Voltar", 
                  command=lambda: self.callback_func("menu")).pack(side=tk.LEFT, padx=5)
    
    def select_all(self):
        for var in self.selected_data.values():
            var.set(True)
    
    def deselect_all(self):
        for var in self.selected_data.values():
            var.set(False)
    
    def export_data(self):
        # Verifica se algum dado foi selecionado
        if not any(var.get() for var in self.selected_data.values()):
            messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de dado para exportar.")
            return
        
        # Prepara os dados selecionados para exportação
        export_data = {}
        for key, var in self.selected_data.items():
            if var.get() and key in self.user_data:
                export_data[key] = self.user_data[key]
        
        # Define o formato e nome padrão do arquivo
        formato = self.export_format.get()
        default_filename = f"dados_saude_{datetime.datetime.now().strftime('%Y%m%d')}"
        
        # Abre diálogo para selecionar onde salvar
        filetypes = []
        if formato == "json":
            filetypes = [("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
            default_filename += ".json"
        elif formato == "csv":
            filetypes = [("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
            default_filename += ".csv"
        else:  # txt
            filetypes = [("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
            default_filename += ".txt"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{formato}",
            filetypes=filetypes,
            initialfile=default_filename
        )
        
        if not filepath:
            return  # Operação cancelada pelo usuário
        
        try:
            if formato == "json":
                self.export_as_json(export_data, filepath)
            elif formato == "csv":
                self.export_as_csv(export_data, filepath)
            else:  # txt
                self.export_as_txt(export_data, filepath)
                
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")
    
    def export_as_json(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def export_as_csv(self, data, filepath):
        # Criar um único arquivo CSV com múltiplas seções
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            for section, section_data in data.items():
                # Escreve o cabeçalho da seção
                writer.writerow([section.upper()])
                
                if section == 'perfil':
                    # Perfil é um dicionário simples
                    writer.writerow(['Campo', 'Valor'])
                    for key, value in section_data.items():
                        writer.writerow([key, value])
                elif section in ['medidas', 'atividades'] and 'historico' in section_data:
                    # Histórico de medidas ou atividades
                    if section_data['historico']:
                        # Obter cabeçalhos a partir das chaves do primeiro item
                        headers = list(section_data['historico'][0].keys())
                        writer.writerow(headers)
                        
                        # Escrever cada linha de dados
                        for item in section_data['historico']:
                            writer.writerow([item.get(h, '') for h in headers])
                elif section in ['medicamentos', 'consultas'] and 'lista' in section_data:
                    # Lista de medicamentos ou consultas
                    if section_data['lista']:
                        # Obter cabeçalhos a partir das chaves do primeiro item
                        headers = list(section_data['lista'][0].keys())
                        writer.writerow(headers)
                        
                        # Escrever cada linha de dados
                        for item in section_data['lista']:
                            writer.writerow([item.get(h, '') for h in headers])
                
                # Linha em branco entre seções
                writer.writerow([])
    
    def export_as_txt(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE DADOS DE SAÚDE\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data de exportação: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            for section, section_data in data.items():
                f.write(f"{section.upper()}\n")
                f.write("-" * 50 + "\n")
                
                if section == 'perfil':
                    # Perfil é um dicionário simples
                    for key, value in section_data.items():
                        f.write(f"{key.capitalize()}: {value}\n")
                elif section in ['medidas', 'atividades'] and 'historico' in section_data:
                    # Histórico de medidas ou atividades
                    for i, item in enumerate(section_data['historico']):
                        f.write(f"Item {i+1}:\n")
                        for key, value in item.items():
                            f.write(f"  {key.capitalize()}: {value}\n")
                        f.write("\n")
                elif section in ['medicamentos', 'consultas'] and 'lista' in section_data:
                    # Lista de medicamentos ou consultas
                    for i, item in enumerate(section_data['lista']):
                        f.write(f"Item {i+1}:\n")
                        for key, value in item.items():
                            f.write(f"  {key.capitalize()}: {value}\n")
                        f.write("\n")
                
                f.write("\n")
    
    def show(self):
        self.frame.tkraise()