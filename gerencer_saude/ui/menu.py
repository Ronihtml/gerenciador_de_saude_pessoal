import tkinter as tk
from tkinter import ttk, messagebox
import gerencer_saude.features.perfil as perfil
import gerencer_saude.features.medidas as medidas
import gerencer_saude.features.medicamentos as medicamentos
import gerencer_saude.features.atividades as atividades
import gerencer_saude.features.consultas as consultas
import gerencer_saude.reports.relatorios as relatorios

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Saúde Pessoal")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#f0f0f0")
        self.style.configure("Menu.TButton", font=("Arial", 12), width=20, padding=10)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Cabeçalho
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        header_label = ttk.Label(header_frame, text="Gerenciamento de Saúde Pessoal", 
                                style="Header.TLabel")
        header_label.pack()
        
        # Menu principal
        menu_frame = ttk.Frame(self.root, style="TFrame")
        menu_frame.pack(expand=True, fill=tk.BOTH, padx=100, pady=20)
        
        # Botões do menu
        btn_perfil = ttk.Button(menu_frame, text="Perfil do Usuário", 
                              style="Menu.TButton", command=self.abrir_perfil)
        btn_perfil.pack(pady=10)
        
        btn_medidas = ttk.Button(menu_frame, text="Medidas Corporais", 
                               style="Menu.TButton", command=self.abrir_medidas)
        btn_medidas.pack(pady=10)
        
        btn_medicamentos = ttk.Button(menu_frame, text="Medicamentos", 
                                    style="Menu.TButton", command=self.abrir_medicamentos)
        btn_medicamentos.pack(pady=10)
        
        btn_atividades = ttk.Button(menu_frame, text="Atividades Físicas", 
                                  style="Menu.TButton", command=self.abrir_atividades)
        btn_atividades.pack(pady=10)
        
        btn_consultas = ttk.Button(menu_frame, text="Consultas Médicas", 
                                 style="Menu.TButton", command=self.abrir_consultas)
        btn_consultas.pack(pady=10)
        
        btn_relatorios = ttk.Button(menu_frame, text="Relatórios", 
                                  style="Menu.TButton", command=self.abrir_relatorios)
        btn_relatorios.pack(pady=10)
        
        # Rodapé
        footer_frame = ttk.Frame(self.root, style="TFrame")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=10)
        
        btn_sair = ttk.Button(footer_frame, text="Sair", command=self.root.destroy)
        btn_sair.pack(side=tk.RIGHT)
    
    def abrir_perfil(self):
        perfil_window = tk.Toplevel(self.root)
        perfil_app = perfil.PerfilApp(perfil_window)
    
    def abrir_medidas(self):
        medidas_window = tk.Toplevel(self.root)
        medidas_app = medidas.MedidasApp(medidas_window)
    
    def abrir_medicamentos(self):
        medicamentos_window = tk.Toplevel(self.root)
        medicamentos_app = medicamentos.MedicamentosApp(medicamentos_window)
    
    def abrir_atividades(self):
        atividades_window = tk.Toplevel(self.root)
        atividades_app = atividades.AtividadesApp(atividades_window)
    
    def abrir_consultas(self):
        consultas_window = tk.Toplevel(self.root)
        consultas_app = consultas.ConsultasApp(consultas_window)
    
    def abrir_relatorios(self):
        relatorios_window = tk.Toplevel(self.root)
        relatorios_app = relatorios.RelatoriosApp(relatorios_window)