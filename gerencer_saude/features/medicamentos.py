import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MedicamentosManager:
    def __init__(self, dados):
        self.dados = dados
    
    def criar_frame(self, parent, callback_salvar):
        self.callback_salvar = callback_salvar
        
        frame = ttk.Frame(parent)
        
        # Título da seção
        ttk.Label(frame, text="Gerenciamento de Medicamentos", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame do formulário
        form_frame = ttk.Frame(frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Campos do formulário
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Dosagem:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dosagem_entry = ttk.Entry(form_frame, width=30)
        self.dosagem_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Frequência:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.frequencia_entry = ttk.Entry(form_frame, width=30)
        self.frequencia_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Horários:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.horarios_entry = ttk.Entry(form_frame, width=30)
        self.horarios_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Data de início:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.inicio_entry = ttk.Entry(form_frame, width=30)
        self.inicio_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.inicio_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(form_frame, text="Data de término:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.termino_entry = ttk.Entry(form_frame, width=30)
        self.termino_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Observações:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.NW)
        self.obs_text = tk.Text(form_frame, width=30, height=4)
        self.obs_text.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botão para adicionar medicamento
        ttk.Button(frame, text="Adicionar Medicamento", 
                  command=self.adicionar_medicamento).pack(pady=10)
        
        # Frame da lista de medicamentos
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Lista de medicamentos
        ttk.Label(list_frame, text="Medicamentos Atuais", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Cria o Treeview para exibir os medicamentos
        columns = ("nome", "dosagem", "frequencia", "horarios", "inicio", "termino")
        self.medicamentos_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # Configura as colunas
        self.medicamentos_tree.heading("nome", text="Nome")
        self.medicamentos_tree.heading("dosagem", text="Dosagem")
        self.medicamentos_tree.heading("frequencia", text="Frequência")
        self.medicamentos_tree.heading("horarios", text="Horários")
        self.medicamentos_tree.heading("inicio", text="Início")
        self.medicamentos_tree.heading("termino", text="Término")
        
        self.medicamentos_tree.column("nome", width=120)
        self.medicamentos_tree.column("dosagem", width=80)
        self.medicamentos_tree.column("frequencia", width=80)
        self.medicamentos_tree.column("horarios", width=100)
        self.medicamentos_tree.column("inicio", width=80)
        self.medicamentos_tree.column("termino", width=80)
        
        # Adiciona barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.medicamentos_tree.yview)
        self.medicamentos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacota o Treeview e a barra de rolagem
        self.medicamentos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adiciona evento de clique duplo para ver detalhes
        self.medicamentos_tree.bind("<Double-1>", self.exibir_detalhes_medicamento)
        
        # Botão para remover medicamento
        ttk.Button(frame, text="Remover Medicamento Selecionado", 
                  command=self.remover_medicamento).pack(pady=10)
        
        # Carrega os medicamentos
        self.carregar_medicamentos()
        
        return frame
    
    def carregar_medicamentos(self):
        # Limpa a lista
        for item in self.medicamentos_tree.get_children():
            self.medicamentos_tree.delete(item)
        
        # Adiciona os medicamentos à lista
        for medicamento in self.dados["medicamentos"]:
            self.medicamentos_tree.insert("", tk.END, values=(
                medicamento["nome"],
                medicamento["dosagem"],
                medicamento["frequencia"],
                medicamento["horarios"],
                medicamento["inicio"],
                medicamento["termino"]
            ))
    
    def adicionar_medicamento(self):
        # Valida os campos obrigatórios
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome do medicamento é obrigatório")
            return
        
        # Cria o novo medicamento
        novo_medicamento = {
            "nome": nome,
            "dosagem": self.dosagem_entry.get().strip(),
            "frequencia": self.frequencia_entry.get().strip(),
            "horarios": self.horarios_entry.get().strip(),
            "inicio": self.inicio_entry.get().strip(),
            "termino": self.termino_entry.get().strip(),
            "observacoes": self.obs_text.get("1.0", tk.END).strip()
        }
        
        # Adiciona o medicamento
        self.dados["medicamentos"].append(novo_medicamento)
        
        # Atualiza a lista
        self.carregar_medicamentos()
        
        # Limpa os campos
        self.nome_entry.delete(0, tk.END)
        self.dosagem_entry.delete(0, tk.END)
        self.frequencia_entry.delete(0, tk.END)
        self.horarios_entry.delete(0, tk.END)
        self.termino_entry.delete(0, tk.END)
        self.obs_text.delete("1.0", tk.END)
        
        # Salva os dados
        self.callback_salvar()
        
        messagebox.showinfo("Sucesso", "Medicamento adicionado com sucesso!")
    
    def remover_medicamento(self):
        # Obtém o item selecionado
        selected_item = self.medicamentos_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um medicamento para remover")
            return
        
        # Obtém o índice do item selecionado
        item_index = self.medicamentos_tree.index(selected_item[0])
        
        # Confirmação
        confirma = messagebox.askyesno("Confirmar", 
                                      "Tem certeza que deseja remover este medicamento?")
        
        if confirma:
            # Remove o medicamento
            self.dados["medicamentos"].pop(item_index)
            
            # Atualiza a lista
            self.carregar_medicamentos()
            
            # Salva os dados
            self.callback_salvar()
    
    def exibir_detalhes_medicamento(self, event):
        # Obtém o item selecionado
        item = self.medicamentos_tree.selection()[0]
        item_index = self.medicamentos_tree.index(item)
        
        # Obtém o medicamento
        medicamento = self.dados["medicamentos"][item_index]
        
        # Cria uma janela para exibir os detalhes
        detalhes_window = tk.Toplevel()
        detalhes_window.title("Detalhes do Medicamento")
        detalhes_window.geometry("400x300")
        
        # Configuração de estilo
        detalhes_window.configure(bg="#f0f4f8")
        
        # Título
        ttk.Label(detalhes_window, text=medicamento["nome"], 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Detalhes
        detalhes = ttk.Frame(detalhes_window)
        detalhes.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Informações
        info = [
            ("Dosagem:", medicamento["dosagem"]),
            ("Frequência:", medicamento["frequencia"]),
            ("Horários:", medicamento["horarios"]),
            ("Data de início:", medicamento["inicio"]),
            ("Data de término:", medicamento["termino"])
        ]
        
        for i, (label_text, value) in enumerate(info):
            ttk.Label(detalhes, text=label_text, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Label(detalhes, text=value).grid(
                row=i, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Observações
        ttk.Label(detalhes, text="Observações:", font=('Arial', 10, 'bold')).grid(
            row=len(info), column=0, padx=5, pady=5, sticky=tk.NW)
        
        obs_text = tk.Text(detalhes, width=30, height=5, wrap=tk.WORD)
        obs_text.grid(row=len(info), column=1, padx=5, pady=5, sticky=tk.W)
        obs_text.insert("1.0", medicamento["observacoes"])
        obs_text.configure(state="disabled")
        
        # Botão para fechar
        ttk.Button(detalhes_window, text="Fechar", 
                  command=detalhes_window.destroy).pack(pady=10)