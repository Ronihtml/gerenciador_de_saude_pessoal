import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import os
from gerencer_saude.ui.styles import apply_style
from gerencer_saude.core.utils import load_data, validate_date
from gerencer_saude.core.config import DASHBOARD_CONFIG

class Dashboard:
    def __init__(self, parent, user_data, callback_func):
        self.parent = parent
        self.user_data = user_data
        self.callback_func = callback_func
        
        self.frame = ttk.Frame(parent)
        apply_style(self.frame, "dashboard")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título do Dashboard
        title_label = ttk.Label(self.frame, text="Dashboard de Saúde", 
                               font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20)
        
        # Data atual
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        date_label = ttk.Label(self.frame, text=f"Data: {current_date}", 
                              font=("Helvetica", 10))
        date_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w", padx=20)
        
        # Resumo rápido
        quick_stats_frame = ttk.LabelFrame(self.frame, text="Resumo Rápido")
        quick_stats_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        
        self.create_quick_stats(quick_stats_frame)
        
        # Gráfico de progresso
        chart_frame = ttk.LabelFrame(self.frame, text="Progresso")
        chart_frame.grid(row=2, column=1, pady=10, padx=20, sticky="nsew")
        
        self.create_chart(chart_frame)
        
        # Próximos eventos
        events_frame = ttk.LabelFrame(self.frame, text="Próximos Eventos")
        events_frame.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")
        
        self.create_events_list(events_frame)
        
        # Dicas de saúde
        tips_frame = ttk.LabelFrame(self.frame, text="Dicas de Saúde")
        tips_frame.grid(row=3, column=1, pady=10, padx=20, sticky="nsew")
        
        self.create_health_tips(tips_frame)
        
        # Botões de ação
        action_frame = ttk.Frame(self.frame)
        action_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=20)
        
        ttk.Button(action_frame, text="Atualizar Dashboard", 
                  command=self.refresh_dashboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Exportar Resumo", 
                  command=self.export_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Voltar ao Menu", 
                  command=lambda: self.callback_func("menu")).pack(side=tk.LEFT, padx=5)

    def create_quick_stats(self, parent_frame):
        # Se tiver dados de perfil
        if 'peso' in self.user_data.get('medidas', {}).get('historico', [{}])[-1]:
            ultimo_peso = self.user_data['medidas']['historico'][-1]['peso']
            peso_label = ttk.Label(parent_frame, text=f"Peso atual: {ultimo_peso} kg")
            peso_label.pack(anchor="w", pady=2)
        
        # Número de medicamentos ativos
        med_count = len([m for m in self.user_data.get('medicamentos', {}).get('lista', []) 
                         if m.get('ativo', True)])
        med_label = ttk.Label(parent_frame, text=f"Medicamentos ativos: {med_count}")
        med_label.pack(anchor="w", pady=2)
        
        # Próxima consulta
        proximas_consultas = sorted([c for c in self.user_data.get('consultas', {}).get('lista', []) 
                                    if validate_date(c.get('data', '')) >= datetime.datetime.now()],
                                   key=lambda x: validate_date(x.get('data', '')))
        
        if proximas_consultas:
            proxima = proximas_consultas[0]
            consulta_label = ttk.Label(parent_frame, 
                                     text=f"Próxima consulta: {proxima.get('data', '')} - {proxima.get('especialidade', '')}")
            consulta_label.pack(anchor="w", pady=2)
        else:
            consulta_label = ttk.Label(parent_frame, text="Não há consultas agendadas")
            consulta_label.pack(anchor="w", pady=2)
            
        # Atividades na semana
        atividades_semana = len([a for a in self.user_data.get('atividades', {}).get('historico', []) 
                               if (datetime.datetime.now() - validate_date(a.get('data', ''))).days <= 7])
        atividade_label = ttk.Label(parent_frame, text=f"Atividades na última semana: {atividades_semana}")
        atividade_label.pack(anchor="w", pady=2)

    def create_chart(self, parent_frame):
        figure = plt.Figure(figsize=(4, 3), dpi=100)
        ax = figure.add_subplot(111)
        
        # Dados para o gráfico (exemplo com peso)
        if 'medidas' in self.user_data and 'historico' in self.user_data['medidas']:
            historico = self.user_data['medidas']['historico']
            if historico and 'data' in historico[0] and 'peso' in historico[0]:
                datas = [validate_date(item.get('data', '')) for item in historico]
                pesos = [float(item.get('peso', 0)) for item in historico]
                
                ax.plot(datas, pesos, marker='o')
                ax.set_title('Evolução do Peso')
                ax.set_xlabel('Data')
                ax.set_ylabel('Peso (kg)')
                figure.tight_layout()
        else:
            ax.text(0.5, 0.5, "Sem dados suficientes para gerar gráfico", 
                   horizontalalignment='center', verticalalignment='center')
        
        canvas = FigureCanvasTkAgg(figure, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_events_list(self, parent_frame):
        # Lista das próximas consultas e lembretes de medicamentos
        eventos = []
        
        # Consultas
        for consulta in self.user_data.get('consultas', {}).get('lista', []):
            data_consulta = validate_date(consulta.get('data', ''))
            if data_consulta >= datetime.datetime.now():
                eventos.append({
                    'data': data_consulta,
                    'descricao': f"Consulta: {consulta.get('especialidade', '')}",
                    'tipo': 'consulta'
                })
        
        # Medicamentos (próximas doses)
        for med in self.user_data.get('medicamentos', {}).get('lista', []):
            if med.get('ativo', True) and med.get('horarios'):
                for horario in med.get('horarios', []):
                    eventos.append({
                        'data': datetime.datetime.combine(
                            datetime.datetime.now().date(), 
                            datetime.datetime.strptime(horario, "%H:%M").time()
                        ),
                        'descricao': f"Medicamento: {med.get('nome', '')}",
                        'tipo': 'medicamento'
                    })
        
        # Ordenar eventos por data
        eventos = sorted(eventos, key=lambda x: x['data'])[:5]  # Mostrar apenas os 5 próximos
        
        if eventos:
            for evento in eventos:
                data_str = evento['data'].strftime("%d/%m/%Y %H:%M")
                item_frame = ttk.Frame(parent_frame)
                item_frame.pack(fill=tk.X, pady=2)
                
                if evento['tipo'] == 'consulta':
                    icon_label = ttk.Label(item_frame, text="🏥")
                else:
                    icon_label = ttk.Label(item_frame, text="💊")
                
                icon_label.pack(side=tk.LEFT, padx=5)
                
                ttk.Label(item_frame, text=f"{data_str} - {evento['descricao']}").pack(
                    side=tk.LEFT, padx=5)
        else:
            ttk.Label(parent_frame, text="Não há eventos próximos agendados").pack(
                pady=10, padx=10)

    def create_health_tips(self, parent_frame):
        # Lista de dicas de saúde
        dicas = [
            "Beba pelo menos 2 litros de água por dia.",
            "Pratique pelo menos 30 minutos de atividade física diariamente.",
            "Mantenha uma alimentação balanceada, rica em frutas e vegetais.",
            "Durma de 7 a 8 horas por noite para um bom descanso.",
            "Faça check-ups médicos regularmente."
        ]
        
        for dica in dicas:
            tip_frame = ttk.Frame(parent_frame)
            tip_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(tip_frame, text="✓").pack(side=tk.LEFT, padx=5)
            ttk.Label(tip_frame, text=dica, wraplength=200).pack(side=tk.LEFT, padx=5)

    def refresh_dashboard(self):
        # Recarrega os dados e atualiza o dashboard
        self.user_data = load_data()
        
        # Destroi o frame atual
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Recria os widgets
        self.create_widgets()
        messagebox.showinfo("Atualização", "Dashboard atualizado com sucesso!")

    def export_summary(self):
        # Exporta um resumo em formato de texto
        try:
            with open("resumo_saude.txt", "w") as file:
                file.write("RESUMO DE SAÚDE\n")
                file.write("=" * 50 + "\n\n")
                
                file.write(f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}\n\n")
                
                # Dados do perfil
                if 'perfil' in self.user_data:
                    file.write("PERFIL:\n")
                    for key, value in self.user_data['perfil'].items():
                        file.write(f"{key.capitalize()}: {value}\n")
                    file.write("\n")
                
                # Últimas medidas
                if 'medidas' in self.user_data and 'historico' in self.user_data['medidas']:
                    if self.user_data['medidas']['historico']:
                        ultima_medida = self.user_data['medidas']['historico'][-1]
                        file.write("ÚLTIMAS MEDIDAS:\n")
                        for key, value in ultima_medida.items():
                            if key != 'data':
                                file.write(f"{key.capitalize()}: {value}\n")
                        file.write("\n")
                
                # Medicamentos ativos
                if 'medicamentos' in self.user_data and 'lista' in self.user_data['medicamentos']:
                    file.write("MEDICAMENTOS ATIVOS:\n")
                    med_ativos = [m for m in self.user_data['medicamentos']['lista'] 
                                 if m.get('ativo', True)]
                    for med in med_ativos:
                        file.write(f"- {med.get('nome', '')}: {', '.join(med.get('horarios', []))}\n")
                    file.write("\n")
                
                # Próximas consultas
                if 'consultas' in self.user_data and 'lista' in self.user_data['consultas']:
                    file.write("PRÓXIMAS CONSULTAS:\n")
                    proximas = [c for c in self.user_data['consultas']['lista'] 
                               if validate_date(c.get('data', '')) >= datetime.datetime.now()]
                    proximas = sorted(proximas, key=lambda x: validate_date(x.get('data', '')))
                    
                    for consulta in proximas:
                        file.write(f"- {consulta.get('data', '')}: {consulta.get('especialidade', '')} "
                                  f"com Dr(a). {consulta.get('medico', '')}\n")
            
            messagebox.showinfo("Exportação", 
                             f"Resumo exportado com sucesso para {os.path.abspath('resumo_saude.txt')}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def show(self):
        self.frame.tkraise()