import tkinter as tk
from tkinter import messagebox
import threading
import time
import datetime
import json
import os
from plyer import notification

class NotificacoesManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.notificacoes_file = os.path.join(self.data_manager.data_dir, "notificacoes.json")
        self.initialize_notificacoes_file()
        self.notificacoes_thread = None
        self.running = False
        
    def initialize_notificacoes_file(self):
        """Inicializa o arquivo de notificações se não existir"""
        if not os.path.exists(self.notificacoes_file):
            with open(self.notificacoes_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    def get_notificacoes(self):
        """Carrega notificações do arquivo JSON"""
        try:
            with open(self.notificacoes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, cria um novo
            self.save_notificacoes([])
            return []
    
    def save_notificacoes(self, notificacoes):
        """Salva notificações no arquivo JSON"""
        with open(self.notificacoes_file, 'w', encoding='utf-8') as f:
            json.dump(notificacoes, f, ensure_ascii=False, indent=4)
    
    def adicionar_notificacao(self, titulo, mensagem, data_hora, tipo="medicamento"):
        """Adiciona uma nova notificação"""
        notificacoes = self.get_notificacoes()
        nova_notificacao = {
            "id": self.generate_id(notificacoes),
            "titulo": titulo,
            "mensagem": mensagem,
            "data_hora": data_hora,
            "tipo": tipo,
            "ativa": True
        }
        notificacoes.append(nova_notificacao)
        self.save_notificacoes(notificacoes)
    
    def remover_notificacao(self, notificacao_id):
        """Remove uma notificação específica"""
        notificacoes = self.get_notificacoes()
        notificacoes = [n for n in notificacoes if n.get('id') != notificacao_id]
        self.save_notificacoes(notificacoes)
    
    def atualizar_notificacao(self, notificacao_id, notificacao_atualizada):
        """Atualiza uma notificação específica"""
        notificacoes = self.get_notificacoes()
        for i, notificacao in enumerate(notificacoes):
            if notificacao.get('id') == notificacao_id:
                notificacao_atualizada['id'] = notificacao_id
                notificacoes[i] = notificacao_atualizada
                break
        self.save_notificacoes(notificacoes)
    
    def generate_id(self, items):
        """Gera um ID único para uma nova notificação"""
        if not items:
            return 1
        
        max_id = max(item.get('id', 0) for item in items)
        return max_id + 1
    
    def iniciar_verificacao_notificacoes(self):
        """Inicia a thread de verificação de notificações"""
        if self.notificacoes_thread is None or not self.running:
            self.running = True
            self.notificacoes_thread = threading.Thread(target=self.verificar_notificacoes)
            self.notificacoes_thread.daemon = True
            self.notificacoes_thread.start()
    
    def parar_verificacao_notificacoes(self):
        """Para a thread de verificação de notificações"""
        self.running = False
        if self.notificacoes_thread:
            self.notificacoes_thread.join(timeout=1)
    
    def verificar_notificacoes(self):
        """Verifica continuamente se há notificações para exibir"""
        while self.running:
            notificacoes = self.get_notificacoes()
            data_atual = datetime.datetime.now()
            
            for notificacao in notificacoes:
                if not notificacao.get('ativa', True):
                    continue
                
                try:
                    data_notificacao = datetime.datetime.strptime(
                        notificacao['data_hora'], 
                        "%Y-%m-%d %H:%M:%S"
                    )
                    
                    # Se está no momento de notificar (com margem de 1 minuto)
                    diferenca = (data_notificacao - data_atual).total_seconds()
                    if 0 <= diferenca <= 60:
                        self.exibir_notificacao(notificacao)
                        # Desativa a notificação após exibir (para não mostrar novamente)
                        notificacao['ativa'] = False
                        self.atualizar_notificacao(notificacao['id'], notificacao)
                except (ValueError, KeyError):
                    # Ignora notificações com formato de data inválido
                    pass
            
            # Verifica a cada 30 segundos
            time.sleep(30)
    
    def exibir_notificacao(self, notificacao):
        """Exibe uma notificação na área de trabalho"""
        try:
            notification.notify(
                title=notificacao['titulo'],
                message=notificacao['mensagem'],
                app_name="Gerenciamento de Saúde",
                timeout=10
            )
        except Exception:
            # Fallback para messagebox se a notificação do sistema falhar
            # Note que isso só funciona se a aplicação principal estiver em execução
            messagebox.showinfo(notificacao['titulo'], notificacao['mensagem'])
    
    def notificar_medicamentos(self):
        """Cria notificações para medicamentos com base nos horários programados"""
        medicamentos = self.data_manager.get_medicamentos()
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
        
        for medicamento in medicamentos:
            if not medicamento.get('ativo', True):
                continue
                
            horarios = medicamento.get('horarios', [])
            for horario in horarios:
                data_hora = f"{data_atual} {horario}:00"
                self.adicionar_notificacao(
                    f"Hora do medicamento: {medicamento['nome']}",
                    f"Lembre-se de tomar {medicamento['dosagem']} de {medicamento['nome']}",
                    data_hora,
                    "medicamento"
                )
    
    def notificar_consultas(self):
        """Cria notificações para consultas médicas agendadas"""
        consultas = self.data_manager.get_consultas()
        
        for consulta in consultas:
            data = consulta.get('data', '')
            horario = consulta.get('horario', '')
            
            if data and horario:
                # Notificação um dia antes
                try:
                    data_consulta = datetime.datetime.strptime(f"{data} {horario}", "%d/%m/%Y %H:%M")
                    um_dia_antes = data_consulta - datetime.timedelta(days=1)
                    
                    self.adicionar_notificacao(
                        f"Lembrete de Consulta Médica",
                        f"Você tem uma consulta com {consulta.get('medico', 'seu médico')} amanhã às {horario}",
                        um_dia_antes.strftime("%Y-%m-%d %H:%M:%S"),
                        "consulta"
                    )
                    
                    # Notificação uma hora antes
                    uma_hora_antes = data_consulta - datetime.timedelta(hours=1)
                    
                    self.adicionar_notificacao(
                        f"Consulta Médica em Breve",
                        f"Sua consulta com {consulta.get('medico', 'seu médico')} é em 1 hora",
                        uma_hora_antes.strftime("%Y-%m-%d %H:%M:%S"),
                        "consulta"
                    )
                except ValueError:
                    # Ignora data/hora inválida
                    pass