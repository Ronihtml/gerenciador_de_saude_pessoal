import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AtividadesManager:
    def __init__(self, dados):
        self.dados = dados
    
    def criar_frame(self, parent, callback_salvar):
        self.callback_salvar = callback_salvar
        
        frame = ttk.Frame(parent)
        
        # Dividimos o frame em duas colunas
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título da seção
        ttk.Label(left_frame, text="Registrar Atividade Física", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame do formulário
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Campos do formulário
        ttk.Label(form_frame, text="Data:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_entry = ttk.Entry(form_frame, width=20)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(form_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.tipo_entry = ttk.Combobox(form_frame, width=20, values=[
            "Caminhada", "Corrida", "Ciclismo", "Natação", "Musculação", "Yoga", "Outro"
        ])
        self.tipo_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Duração (min):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.duracao_entry = ttk.Entry(form_frame, width=20)
        self.duracao_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Calorias:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.calorias_entry = ttk.Entry(form_frame, width=20)
        self.calorias_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Distância (km):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.distancia_entry = ttk.Entry(form_frame, width=20)
        self.distancia_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Observações:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.NW)
        self.obs_text = tk.Text(form_frame, width=20, height=4)
        self.obs_text.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botão para adicionar atividade
        ttk.Button(left_frame, text="Registrar Atividade", 
                  command=self.adicionar_atividade).pack(pady=10)
        
        # Lista de atividades
        ttk.Label(left_frame, text="Atividades Recentes", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Criação do Treeview
        columns = ("data", "tipo", "duracao", "calorias", "distancia")
        self.atividades_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=8)
        
        # Configuração das colunas
        self.atividades_tree.heading("data", text="Data")
        self.atividades_tree.heading("tipo", text="Tipo")
        self.atividades_tree.heading("duracao", text="Duração (min)")
        self.atividades_tree.heading("calorias", text="Calorias")
        self.atividades_tree.heading("distancia", text="Distância (km)")
        
        self.atividades_tree.column("data", width=80)
        self.atividades_tree.column("tipo", width=100)
        self.atividades_tree.column("duracao", width=80)
        self.atividades_tree.column("calorias", width=80)
        self.atividades_tree.column("distancia", width=80)
        
        # Configuração da barra de rolagem
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.atividades_tree.yview)
        self.atividades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacotamento do Treeview e barra de rolagem
        self.atividades_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para remover atividade
        ttk.Button(left_frame, text="Remover Atividade Selecionada", 
                  command=self.remover_atividade).pack(pady=10)
        
        # Gráfico de atividades por tipo
        ttk.Label(right_frame, text="Resumo de Atividades", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Carrega as atividades
        self.carregar_atividades()
        self.atualizar_grafico()
        
        return frame
    
    def carregar_atividades(self):
        # Limpa a tabela
        for item in self.atividades_tree.get_children():
            self.atividades_tree.delete(item)
        
        # Adiciona as atividades à tabela
        for atividade in self.dados["atividades"]:
            self.atividades_tree.insert("", tk.END, values=(
                atividade["data"],
                atividade["tipo"],
                atividade["duracao"],
                atividade["calorias"],
                atividade["distancia"]
            ))
    
    def adicionar_atividade(self):
        # Valida os campos
        tipo = self.tipo_entry.get().strip()
        
        if not tipo:
            messagebox.showerror("Erro", "O tipo de atividade é obrigatório")
            return
        
        try:
            duracao = int(self.duracao_entry.get()) if self.duracao_entry.get() else 0
        except ValueError:
            messagebox.showerror("Erro", "A duração deve ser um número inteiro")
            return
        
        try:
            calorias = int(self.calorias_entry.get()) if self.calorias_entry.get() else 0
        except ValueError:
            messagebox.showerror("Erro", "As calorias devem ser um número inteiro")
            return
        
        try:
            distancia = float(self.distancia_entry.get()) if self.distancia_entry.get() else 0
        except ValueError:
            messagebox.showerror("Erro", "A distância deve ser um número válido")
            return
        
        # Cria a nova atividade
        nova_atividade = {
            "data": self.data_entry.get(),
            "tipo": tipo,
            "duracao": duracao,
            "calorias": calorias,
            "distancia": distancia,
            "observacoes": self.obs_text.get("1.0", tk.END).strip()
        }
        
        # Adiciona a atividade aos dados
        self.dados["atividades"].append(nova_atividade)
        
        # Atualiza as visualizações
        self.carregar_atividades()
        self.atualizar_grafico()
        
        # Limpa os campos
        self.tipo_entry.set("")
        self.duracao_entry.delete(0, tk.END)
        self.calorias_entry.delete(0, tk.END)
        self.distancia_entry.delete(0, tk.END)
        self.obs_text.delete("1.0", tk.END)
        
        # Salva os dados
        self.callback_salvar()
        
        messagebox.showinfo("Sucesso", "Atividade registrada com sucesso!")
    
    def remover_atividade(self):
        # Obtém o item selecionado
        selected_item = self.atividades_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione uma atividade para remover")
            return
        
        # Obtém o índice do item selecionado
        item_index = self.atividades_tree.index(selected_item[0])
        
        # Confirmação
        confirma = messagebox.askyesno("Confirmar", 
                                      "Tem certeza que deseja remover esta atividade?")
        
        if confirma:
            # Remove a atividade
            self.dados["atividades"].pop(item_index)
            
            # Atualiza as visualizações
            self.carregar_atividades()
            self.atualizar_grafico()
            
            # Salva os dados
            self.callback_salvar()
    
    def atualizar_grafico(self):
        # Limpa o gráfico
        self.ax.clear()
        
        # Contagem de atividades por tipo
        tipos = {}
        for atividade in self.dados["atividades"]:
            tipo = atividade["tipo"]
            if tipo in tipos:
                tipos[tipo] += 1
            else:
                tipos[tipo] = 1
        
        if tipos:
            # Extrai os dados para o gráfico
            labels = list(tipos.keys())
            values = list(tipos.values())
            
            # Cria o gráfico de barras
            bars = self.ax.bar(labels, values, color='#3498db')
            
            # Adiciona rótulos
            self.ax.set_xlabel('Tipo de Atividade')
            self.ax.set_ylabel('Quantidade')
            self.ax.set_title('Atividades por Tipo')
            
            # Rotaciona os rótulos do eixo x
            plt.xticks(rotation=45, ha='right')
            
            # Adiciona valores sobre as barras
            for bar in bars:
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.0f}',
                            ha='center', va='bottom')
            
            # Ajusta o layout
            plt.tight_layout()
        else:
            self.ax.text(0.5, 0.5, "Sem dados para exibir", 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes)
        
        # Atualiza o canvas
        self.canvas.draw()