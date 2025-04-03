import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MedidasManager:
    def __init__(self, dados):
        self.dados = dados
    
    def criar_frame(self, parent, callback_salvar):
        self.callback_salvar = callback_salvar
        
        frame = ttk.Frame(parent)
        
        # Cria um frame com duas colunas
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Formulário para adicionar medidas
        ttk.Label(left_frame, text="Registrar Medidas", font=('Arial', 14, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        # Campos do formulário
        ttk.Label(form_frame, text="Data:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_entry = ttk.Entry(form_frame, width=20)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(form_frame, text="Peso (kg):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.peso_entry = ttk.Entry(form_frame, width=20)
        self.peso_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Pressão Arterial:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.pressao_entry = ttk.Entry(form_frame, width=20)
        self.pressao_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.pressao_entry.insert(0, "120/80")
        
        ttk.Label(form_frame, text="Glicemia:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.glicemia_entry = ttk.Entry(form_frame, width=20)
        self.glicemia_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Colesterol:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.colesterol_entry = ttk.Entry(form_frame, width=20)
        self.colesterol_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botão para adicionar medidas
        ttk.Button(left_frame, text="Adicionar Medida", command=self.adicionar_medida).pack(pady=10)
        
        # Lista de medidas
        ttk.Label(left_frame, text="Histórico de Medidas", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.medidas_tree = ttk.Treeview(left_frame, columns=("data", "peso", "pressao", "glicemia", "colesterol"),
                                        show="headings", height=8)
        self.medidas_tree.heading("data", text="Data")
        self.medidas_tree.heading("peso", text="Peso (kg)")
        self.medidas_tree.heading("pressao", text="Pressão")
        self.medidas_tree.heading("glicemia", text="Glicemia")
        self.medidas_tree.heading("colesterol", text="Colesterol")
        
        self.medidas_tree.column("data", width=100)
        self.medidas_tree.column("peso", width=80)
        self.medidas_tree.column("pressao", width=80)
        self.medidas_tree.column("glicemia", width=80)
        self.medidas_tree.column("colesterol", width=80)
        
        self.medidas_tree.pack(fill=tk.X, pady=10)
        
        # Botão para remover medida selecionada
        ttk.Button(left_frame, text="Remover Medida Selecionada", 
                  command=self.remover_medida).pack(pady=5)
        
        # Gráfico de evolução do peso
        ttk.Label(right_frame, text="Evolução do Peso", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Carregar medidas e atualizar visualizações
        self.carregar_medidas()
        self.atualizar_grafico()
        
        return frame
    
    def carregar_medidas(self):
        # Limpa a tabela
        for item in self.medidas_tree.get_children():
            self.medidas_tree.delete(item)
        
        # Adiciona as medidas à tabela
        for medida in self.dados["medidas"]:
            self.medidas_tree.insert("", tk.END, values=(
                medida["data"],
                medida["peso"],
                medida["pressao"],
                medida["glicemia"],
                medida["colesterol"]
            ))
    
    def adicionar_medida(self):
        # Valida os campos
        try:
            peso = float(self.peso_entry.get()) if self.peso_entry.get() else None
        except ValueError:
            messagebox.showerror("Erro", "O peso deve ser um número válido")
            return
        
        # Cria a nova medida
        nova_medida = {
            "data": self.data_entry.get(),
            "peso": peso,
            "pressao": self.pressao_entry.get(),
            "glicemia": self.glicemia_entry.get(),
            "colesterol": self.colesterol_entry.get()
        }
        
        # Adiciona a medida aos dados
        self.dados["medidas"].append(nova_medida)
        
        # Atualiza as visualizações
        self.carregar_medidas()
        self.atualizar_grafico()
        
        # Limpa os campos
        self.peso_entry.delete(0, tk.END)
        self.pressao_entry.delete(0, tk.END)
        self.pressao_entry.insert(0, "120/80")
        self.glicemia_entry.delete(0, tk.END)
        self.colesterol_entry.delete(0, tk.END)
        
        # Salva os dados
        self.callback_salvar()
    
    def remover_medida(self):
        # Obtém o item selecionado
        selected_item = self.medidas_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione uma medida para remover")
            return
        
        # Obtém o índice do item selecionado
        item_index = self.medidas_tree.index(selected_item[0])
        
        # Remove a medida
        self.dados["medidas"].pop(item_index)
        
        # Atualiza as visualizações
        self.carregar_medidas()
        self.atualizar_grafico()
        
        # Salva os dados
        self.callback_salvar()
    
    def atualizar_grafico(self):
        # Limpa o gráfico
        self.ax.clear()
        
        # Obtém os dados para o gráfico
        datas = []
        pesos = []
        
        for medida in self.dados["medidas"]:
            if medida["peso"]:
                datas.append(medida["data"])
                pesos.append(float(medida["peso"]))
        
        if len(datas) > 0:
            # Cria o gráfico
            self.ax.plot(datas, pesos, 'o-', color='#3498db')
            self.ax.set_xlabel('Data')
            self.ax.set_ylabel('Peso (kg)')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # Configura o eixo x para rotacionar as datas
            plt.xticks(rotation=45)
            
            # Ajusta o layout
            plt.tight_layout()
        else:
            self.ax.text(0.5, 0.5, "Sem dados para exibir", 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes)
        
        # Atualiza o canvas
        self.canvas.draw()