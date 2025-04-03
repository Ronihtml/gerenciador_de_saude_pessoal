import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ConsultasApp:
    def __init__(self, root):
        self.root = root
        self.consultas = []
        self.carregar_consultas()
        self.setup_ui()
    
    def criar_frame(self, notebook, salvar_dados):
        # Defina a lógica do que o frame precisa fazer aqui
        frame = ttk.Frame(notebook)
        # Exemplo de configuração de frame
        ttk.Label(frame, text="Consultas Agendadas").pack()
        # Retorne o frame que será adicionado ao notebook
        return frame

    def setup_ui(self):
        # Limpar a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar a tela
        self.root.title("Gerenciador de Saúde - Consultas Médicas")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Gerenciamento de Consultas Médicas", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # Formulário de entrada
        form_frame = ttk.LabelFrame(main_frame, text="Nova Consulta", padding=10)
        form_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        # Campos do formulário
        ttk.Label(form_frame, text="Especialidade:").grid(row=0, column=0, sticky="w", pady=5)
        self.especialidade_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.especialidade_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Médico:").grid(row=1, column=0, sticky="w", pady=5)
        self.medico_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.medico_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Data:").grid(row=2, column=0, sticky="w", pady=5)
        self.data_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.data_var, width=30).grid(row=2, column=1, pady=5)
        ttk.Label(form_frame, text="(DD/MM/AAAA)").grid(row=2, column=2, sticky="w", pady=5)
        
        ttk.Label(form_frame, text="Hora:").grid(row=3, column=0, sticky="w", pady=5)
        self.hora_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hora_var, width=30).grid(row=3, column=1, pady=5)
        ttk.Label(form_frame, text="(HH:MM)").grid(row=3, column=2, sticky="w", pady=5)
        
        ttk.Label(form_frame, text="Local:").grid(row=4, column=0, sticky="w", pady=5)
        self.local_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.local_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(form_frame, text="Observações:").grid(row=5, column=0, sticky="w", pady=5)
        self.obs_text = tk.Text(form_frame, width=30, height=5)
        self.obs_text.grid(row=5, column=1, pady=5)
        
        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Adicionar", command=self.adicionar_consulta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        # Lista de consultas
        list_frame = ttk.LabelFrame(main_frame, text="Consultas Agendadas", padding=10)
        list_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        
        # Treeview para exibir as consultas
        self.consultas_tree = ttk.Treeview(list_frame, columns=("especialidade", "medico", "data", "hora", "local"), 
                                          show="headings", height=10)
        
        self.consultas_tree.heading("especialidade", text="Especialidade")
        self.consultas_tree.heading("medico", text="Médico")
        self.consultas_tree.heading("data", text="Data")
        self.consultas_tree.heading("hora", text="Hora")
        self.consultas_tree.heading("local", text="Local")
        
        self.consultas_tree.column("especialidade", width=120)
        self.consultas_tree.column("medico", width=120)
        self.consultas_tree.column("data", width=80)
        self.consultas_tree.column("hora", width=60)
        self.consultas_tree.column("local", width=120)
        
        self.consultas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.consultas_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.consultas_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botões para gerenciar consultas
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Ver Detalhes", command=self.ver_detalhes).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Excluir", command=self.excluir_consulta).pack(side=tk.LEFT, padx=5)
        
        # Botão Voltar
        
        
        # Preencher a lista de consultas
        self.atualizar_lista()

    def carregar_consultas(self):
        # Verificar se o arquivo existe
        if os.path.exists("consultas.json"):
            try:
                with open("consultas.json", "r") as file:
                    self.consultas = json.load(file)
            except:
                self.consultas = []
        else:
            self.consultas = []

    def salvar_consultas(self):
        with open("consultas.json", "w") as file:
            json.dump(self.consultas, file, indent=4)

    def adicionar_consulta(self):
        # Obter os valores dos campos
        especialidade = self.especialidade_var.get().strip()
        medico = self.medico_var.get().strip()
        data = self.data_var.get().strip()
        hora = self.hora_var.get().strip()
        local = self.local_var.get().strip()
        obs = self.obs_text.get("1.0", tk.END).strip()
        
        # Validar os campos obrigatórios
        if not especialidade or not data or not hora:
            messagebox.showerror("Erro", "Especialidade, data e hora são campos obrigatórios!")
            return
        
        # Validar o formato da data
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return
            
        # Validar o formato da hora
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM")
            return
        
        # Criar um dicionário com os dados da consulta
        consulta = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "especialidade": especialidade,
            "medico": medico,
            "data": data,
            "hora": hora,
            "local": local,
            "observacoes": obs,
            "data_registro": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # Adicionar à lista
        self.consultas.append(consulta)
        
        # Salvar no arquivo
        self.salvar_consultas()
        
        # Atualizar a lista
        self.atualizar_lista()
        
        # Limpar os campos
        self.limpar_campos()
        
        messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")

    def limpar_campos(self):
        self.especialidade_var.set("")
        self.medico_var.set("")
        self.data_var.set("")
        self.hora_var.set("")
        self.local_var.set("")
        self.obs_text.delete("1.0", tk.END)

    def atualizar_lista(self):
        # Limpar a lista
        for i in self.consultas_tree.get_children():
            self.consultas_tree.delete(i)
        
        # Organizar as consultas por data
        consultas_ordenadas = sorted(self.consultas, key=lambda x: (
            datetime.strptime(x["data"], "%d/%m/%Y"),
            datetime.strptime(x["hora"], "%H:%M")
        ))
        
        # Adicionar as consultas à lista
        for consulta in consultas_ordenadas:
            self.consultas_tree.insert("", tk.END, values=(
                consulta["especialidade"],
                consulta["medico"],
                consulta["data"],
                consulta["hora"],
                consulta["local"]
            ), tags=(consulta["id"],))

    def ver_detalhes(self):
        # Verificar se um item está selecionado
        selecionado = self.consultas_tree.selection()
        if not selecionado:
            messagebox.showinfo("Informação", "Selecione uma consulta para ver os detalhes.")
            return
        
        # Obter o ID do item selecionado
        item_id = self.consultas_tree.item(selecionado[0], "tags")[0]
        
        # Encontrar a consulta correspondente
        consulta = next((c for c in self.consultas if c["id"] == item_id), None)
        
        if consulta:
            # Exibir os detalhes em uma nova janela
            detalhes_window = tk.Toplevel(self.root)
            detalhes_window.title("Detalhes da Consulta")
            detalhes_window.geometry("400x400")
            detalhes_window.resizable(False, False)
            
            frame = ttk.Frame(detalhes_window, padding=20)
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="Detalhes da Consulta", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
            
            ttk.Label(frame, text="Especialidade:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["especialidade"]).grid(row=1, column=1, sticky="w", pady=5)
            
            ttk.Label(frame, text="Médico:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["medico"]).grid(row=2, column=1, sticky="w", pady=5)
            
            ttk.Label(frame, text="Data:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["data"]).grid(row=3, column=1, sticky="w", pady=5)
            
            ttk.Label(frame, text="Hora:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["hora"]).grid(row=4, column=1, sticky="w", pady=5)
            
            ttk.Label(frame, text="Local:", font=("Helvetica", 10, "bold")).grid(row=5, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["local"]).grid(row=5, column=1, sticky="w", pady=5)
            
            ttk.Label(frame, text="Observações:", font=("Helvetica", 10, "bold")).grid(row=6, column=0, sticky="nw", pady=5)
            
            obs_text = tk.Text(frame, wrap=tk.WORD, width=30, height=5, borderwidth=1, relief="solid")
            obs_text.grid(row=6, column=1, sticky="w", pady=5)
            obs_text.insert("1.0", consulta["observacoes"])
            obs_text.config(state="disabled")
            
            ttk.Label(frame, text="Data de registro:", font=("Helvetica", 10, "bold")).grid(row=7, column=0, sticky="w", pady=5)
            ttk.Label(frame, text=consulta["data_registro"]).grid(row=7, column=1, sticky="w", pady=5)
            
            ttk.Button(frame, text="Fechar", command=detalhes_window.destroy).grid(row=8, column=0, columnspan=2, pady=20)

    def excluir_consulta(self):
        # Verificar se um item está selecionado
        selecionado = self.consultas_tree.selection()
        if not selecionado:
            messagebox.showinfo("Informação", "Selecione uma consulta para excluir.")
            return
        
        # Confirmar a exclusão
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta consulta?"):
            return
        
        # Obter o ID do item selecionado
        item_id = self.consultas_tree.item(selecionado[0], "tags")[0]
        
        # Remover a consulta da lista
        self.consultas = [c for c in self.consultas if c["id"] != item_id]
        
        # Salvar no arquivo
        self.salvar_consultas()
        
        # Atualizar a lista
        self.atualizar_lista()
        
        
        messagebox.showinfo("Sucesso", "Consulta excluída com sucesso!")