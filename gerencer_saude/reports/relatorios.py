import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import datetime

class Relatorios:
    def __init__(self, root, voltar_callback):
        self.root = root
        self.voltar_callback = voltar_callback
        self.frame = tk.Frame(root)
        
        # Cabeçalho
        tk.Label(self.frame, text="Relatórios de Saúde", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Opções de relatórios
        opcoes_frame = tk.Frame(self.frame)
        opcoes_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Button(opcoes_frame, text="Relatório de Medidas", command=self.relatorio_medidas, 
                 width=20, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(opcoes_frame, text="Relatório de Medicamentos", command=self.relatorio_medicamentos,
                 width=20, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(opcoes_frame, text="Relatório de Atividades", command=self.relatorio_atividades,
                 width=20, bg="#FF9800", fg="white").grid(row=1, column=0, padx=5, pady=5)
        
        tk.Button(opcoes_frame, text="Relatório de Consultas", command=self.relatorio_consultas,
                 width=20, bg="#9C27B0", fg="white").grid(row=1, column=1, padx=5, pady=5)
        
        # Área para exibir gráficos
        self.grafico_frame = tk.Frame(self.frame)
        self.grafico_frame.pack(pady=10, fill="both", expand=True)
        
        # Botão para voltar
        tk.Button(self.frame, text="Voltar ao Menu Principal", command=self.voltar,
                 bg="#f44336", fg="white").pack(pady=10)
    
    def exibir(self):
        self.frame.pack(fill="both", expand=True)
    
    def esconder(self):
        self.frame.pack_forget()
    
    def voltar(self):
        self.esconder()
        self.voltar_callback()
    
    def limpar_grafico_frame(self):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
    
    def relatorio_medidas(self):
        self.limpar_grafico_frame()
        try:
            if os.path.exists("dados/medidas.json"):
                with open("dados/medidas.json", "r") as file:
                    dados = json.load(file)
                
                if not dados:
                    messagebox.showinfo("Informação", "Não há dados de medidas para gerar relatório.")
                    return
                
                # Preparar dados para o gráfico
                datas = []
                pesos = []
                alturas = []
                imcs = []
                
                for registro in dados:
                    data = datetime.strptime(registro["data"], "%d/%m/%Y")
                    datas.append(data)
                    pesos.append(float(registro["peso"]))
                    alturas.append(float(registro["altura"]))
                    imcs.append(float(registro["imc"]))
                
                # Criar gráfico
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                
                # Gráfico de peso
                ax1.plot(datas, pesos, 'o-', color='blue', label='Peso (kg)')
                ax1.set_title('Evolução do Peso')
                ax1.set_ylabel('Peso (kg)')
                ax1.grid(True)
                
                # Gráfico de IMC
                ax2.plot(datas, imcs, 'o-', color='red', label='IMC')
                ax2.set_title('Evolução do IMC')
                ax2.set_xlabel('Data')
                ax2.set_ylabel('IMC')
                ax2.grid(True)
                
                # Adicionar linhas de referência para classificação do IMC
                ax2.axhline(y=18.5, color='g', linestyle='--', alpha=0.7)
                ax2.axhline(y=25, color='y', linestyle='--', alpha=0.7)
                ax2.axhline(y=30, color='r', linestyle='--', alpha=0.7)
                
                plt.tight_layout()
                
                # Exibir gráfico no frame
                canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
                
                # Adicionar legenda de IMC
                legenda_frame = tk.Frame(self.grafico_frame)
                legenda_frame.pack(pady=5)
                
                tk.Label(legenda_frame, text="IMC < 18.5: Abaixo do peso", fg="green").pack(side=tk.LEFT, padx=5)
                tk.Label(legenda_frame, text="IMC 18.5-24.9: Peso normal", fg="black").pack(side=tk.LEFT, padx=5)
                tk.Label(legenda_frame, text="IMC 25-29.9: Sobrepeso", fg="orange").pack(side=tk.LEFT, padx=5)
                tk.Label(legenda_frame, text="IMC ≥ 30: Obesidade", fg="red").pack(side=tk.LEFT, padx=5)
            else:
                messagebox.showinfo("Informação", "Não há dados de medidas para gerar relatório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def relatorio_medicamentos(self):
        self.limpar_grafico_frame()
        try:
            if os.path.exists("dados/medicamentos.json"):
                with open("dados/medicamentos.json", "r") as file:
                    dados = json.load(file)
                
                if not dados:
                    messagebox.showinfo("Informação", "Não há dados de medicamentos para gerar relatório.")
                    return
                
                # Criar tabela de medicamentos
                tabela_frame = tk.Frame(self.grafico_frame)
                tabela_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                tk.Label(tabela_frame, text="Relatório de Medicamentos", font=("Helvetica", 14, "bold")).pack(pady=5)
                
                # Criar a tabela
                colunas = ("Nome", "Dosagem", "Frequência", "Horário", "Início", "Fim")
                tabela = ttk.Treeview(tabela_frame, columns=colunas, show='headings')
                
                # Configurar cabeçalhos
                for col in colunas:
                    tabela.heading(col, text=col)
                    tabela.column(col, width=100, anchor="center")
                
                # Inserir dados
                for med in dados:
                    tabela.insert("", "end", values=(
                        med["nome"],
                        med["dosagem"],
                        med["frequencia"],
                        med["horario"],
                        med["inicio"],
                        med["fim"]
                    ))
                
                # Adicionar scrollbar
                scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
                tabela.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side="right", fill="y")
                tabela.pack(fill="both", expand=True)
                
                # Adicionar resumo
                tk.Label(self.grafico_frame, text=f"Total de medicamentos: {len(dados)}", 
                        font=("Helvetica", 12)).pack(pady=5)
            else:
                messagebox.showinfo("Informação", "Não há dados de medicamentos para gerar relatório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def relatorio_atividades(self):
        self.limpar_grafico_frame()
        try:
            if os.path.exists("dados/atividades.json"):
                with open("dados/atividades.json", "r") as file:
                    dados = json.load(file)
                
                if not dados:
                    messagebox.showinfo("Informação", "Não há dados de atividades para gerar relatório.")
                    return
                
                # Preparar dados para o gráfico
                tipos = {}
                calorias_por_semana = {}
                
                for atividade in dados:
                    # Contagem por tipo
                    tipo = atividade["tipo"]
                    if tipo in tipos:
                        tipos[tipo] += 1
                    else:
                        tipos[tipo] = 1
                    
                    # Calorias por semana
                    data = datetime.strptime(atividade["data"], "%d/%m/%Y")
                    semana = data.strftime("%U/%Y")  # Número da semana/ano
                    calorias = float(atividade["calorias"])
                    
                    if semana in calorias_por_semana:
                        calorias_por_semana[semana] += calorias
                    else:
                        calorias_por_semana[semana] = calorias
                
                # Criar figura com dois gráficos
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
                
                # Gráfico de pizza dos tipos de atividades
                labels = list(tipos.keys())
                sizes = list(tipos.values())
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')
                ax1.set_title('Distribuição de Tipos de Atividades')
                
                # Gráfico de barras de calorias por semana
                semanas = list(calorias_por_semana.keys())
                calorias = list(calorias_por_semana.values())
                
                # Ordenar por semana
                semanas_ordenadas = sorted(semanas)
                calorias_ordenadas = [calorias_por_semana[s] for s in semanas_ordenadas]
                
                # Simplificar rótulos de semana para exibição
                rotulos_simplificados = [f"Sem {s.split('/')[0]}" for s in semanas_ordenadas]
                
                ax2.bar(rotulos_simplificados, calorias_ordenadas, color='orange')
                ax2.set_title('Calorias Queimadas por Semana')
                ax2.set_xlabel('Semana')
                ax2.set_ylabel('Calorias')
                ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                
                # Exibir gráfico no frame
                canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
                
                # Adicionar estatísticas
                stats_frame = tk.Frame(self.grafico_frame)
                stats_frame.pack(pady=10)
                
                tk.Label(stats_frame, text=f"Total de atividades: {len(dados)}", 
                        font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
                
                # Calcular total de calorias
                total_calorias = sum(float(a["calorias"]) for a in dados)
                tk.Label(stats_frame, text=f"Total de calorias queimadas: {total_calorias:.2f}", 
                        font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
            else:
                messagebox.showinfo("Informação", "Não há dados de atividades para gerar relatório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def relatorio_consultas(self):
        self.limpar_grafico_frame()
        try:
            if os.path.exists("dados/consultas.json"):
                with open("dados/consultas.json", "r") as file:
                    dados = json.load(file)
                
                if not dados:
                    messagebox.showinfo("Informação", "Não há dados de consultas para gerar relatório.")
                    return
                
                # Criar tabela de consultas
                tabela_frame = tk.Frame(self.grafico_frame)
                tabela_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                tk.Label(tabela_frame, text="Histórico de Consultas Médicas", font=("Helvetica", 14, "bold")).pack(pady=5)
                
                # Criar a tabela
                colunas = ("Data", "Especialidade", "Médico", "Resultado", "Próxima")
                tabela = ttk.Treeview(tabela_frame, columns=colunas, show='headings')
                
                # Configurar cabeçalhos
                for col in colunas:
                    tabela.heading(col, text=col)
                    tabela.column(col, width=100, anchor="center")
                
                # Inserir dados
                for consulta in dados:
                    tabela.insert("", "end", values=(
                        consulta["data"],
                        consulta["especialidade"],
                        consulta["medico"],
                        consulta["resultado"],
                        consulta.get("proxima_consulta", "N/A")
                    ))
                
                # Adicionar scrollbar
                scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
                tabela.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side="right", fill="y")
                tabela.pack(fill="both", expand=True)
                
                # Adicionar resumo e estatísticas
                resumo_frame = tk.Frame(self.grafico_frame)
                resumo_frame.pack(pady=10)
                
                # Especialidades mais consultadas
                especialidades = {}
                for consulta in dados:
                    esp = consulta["especialidade"]
                    if esp in especialidades:
                        especialidades[esp] += 1
                    else:
                        especialidades[esp] = 1
                
                # Encontrar a especialidade mais consultada
                if especialidades:
                    mais_consultada = max(especialidades, key=especialidades.get)
                    tk.Label(resumo_frame, text=f"Especialidade mais consultada: {mais_consultada} ({especialidades[mais_consultada]} consultas)", 
                            font=("Helvetica", 12)).pack(pady=2)
                
                # Verificar consultas futuras
                consultas_futuras = []
                hoje = datetime.now()
                for consulta in dados:
                    if "proxima_consulta" in consulta and consulta["proxima_consulta"]:
                        try:
                            data_prox = datetime.strptime(consulta["proxima_consulta"], "%d/%m/%Y")
                            if data_prox > hoje:
                                consultas_futuras.append(consulta)
                        except:
                            pass
                
                if consultas_futuras:
                    tk.Label(resumo_frame, text=f"Consultas futuras agendadas: {len(consultas_futuras)}", 
                            font=("Helvetica", 12)).pack(pady=2)
                else:
                    tk.Label(resumo_frame, text="Não há consultas futuras agendadas", 
                            font=("Helvetica", 12)).pack(pady=2)
            else:
                messagebox.showinfo("Informação", "Não há dados de consultas para gerar relatório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")