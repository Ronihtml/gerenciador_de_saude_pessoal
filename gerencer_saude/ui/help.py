import tkinter as tk
from tkinter import ttk
from gerencer_saude.core.utils import center_window

class HelpWindow:
    def __init__(self, parent):
        self.parent = parent
        
        # Criar janela de ajuda
        self.window = tk.Toplevel(parent)
        self.window.title("Ajuda - Gerenciador de Saúde Pessoal")
        self.window.geometry("700x500")
        self.window.resizable(True, True)
        center_window(self.window)
        
        # Criar notebook para separar os tópicos de ajuda
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Páginas de ajuda
        self.create_introduction_tab()
        self.create_profile_tab()
        self.create_measures_tab()
        self.create_medications_tab()
        self.create_activities_tab()
        self.create_appointments_tab()
        self.create_reports_tab()
        self.create_faq_tab()
        
        # Botão de fechar
        ttk.Button(self.window, text="Fechar", command=self.window.destroy).pack(pady=10)
    
    def create_introduction_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Introdução")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Bem-vindo ao Gerenciador de Saúde Pessoal

Este aplicativo foi desenvolvido para ajudá-lo a monitorar e gerenciar sua saúde de forma simples e organizada.

## Funcionalidades Principais

- **Perfil de Saúde**: Armazene suas informações pessoais e médicas básicas
- **Medidas Corporais**: Registre e acompanhe suas medidas ao longo do tempo
- **Medicamentos**: Gerencie seus medicamentos e horários
- **Atividades Físicas**: Registre seus exercícios e acompanhe seu progresso
- **Consultas Médicas**: Organize seu histórico e agendamento de consultas
- **Relatórios**: Gere relatórios com estatísticas sobre sua saúde

## Como Começar

1. Primeiro, configure seu perfil em "Perfil de Saúde"
2. Explore as diferentes seções do menu principal
3. Adicione suas informações em cada seção
4. Visualize seu progresso nos relatórios

Para mais informações, consulte as outras abas desta ajuda ou entre em contato pelo email: suporte@saudeapp.com
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_profile_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Perfil")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Perfil de Saúde

Nesta seção, você pode gerenciar suas informações pessoais e médicas básicas.

## Informações Disponíveis

- **Dados Pessoais**: Nome, data de nascimento, gênero, etc.
- **Informações de Contato**: Telefone, e-mail e contato de emergência
- **Histórico Médico**: Doenças crônicas, alergias, cirurgias prévias
- **Contatos Médicos**: Médicos, especialistas e seus contatos

## Como Utilizar

1. Acesse a seção "Perfil" no menu principal
2. Preencha seus dados pessoais
3. Adicione seu histórico médico relevante
4. Salve as informações

É importante manter seu perfil atualizado para que seus relatórios e dados sejam precisos.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_measures_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Medidas")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Gerenciamento de Medidas Corporais

Nesta seção, você pode registrar e acompanhar suas medidas corporais ao longo do tempo.

## Medidas Disponíveis

- **Peso**: Acompanhe seu peso e as variações
- **Altura**: Registre sua altura
- **IMC**: Índice de Massa Corporal (calculado automaticamente)
- **Circunferências**: Cintura, quadril, braços, pernas
- **Sinais Vitais**: Pressão arterial, frequência cardíaca, temperatura

## Como Utilizar

1. Acesse a seção "Medidas" no menu principal
2. Clique em "Nova Medida" e selecione o tipo
3. Informe o valor e a data da medição
4. Visualize o histórico e gráficos de evolução

Você pode definir metas para suas medidas e acompanhar seu progresso ao longo do tempo.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_medications_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Medicamentos")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Gerenciamento de Medicamentos

Nesta seção, você pode gerenciar seus medicamentos e horários de administração.

## Funcionalidades

- **Cadastro de Medicamentos**: Nome, dosagem, instruções, etc.
- **Horários**: Configure horários de administração
- **Lembretes**: Receba notificações para tomar seus medicamentos
- **Histórico**: Acompanhe o histórico de administração de cada medicamento

## Como Utilizar

1. Acesse a seção "Medicamentos" no menu principal
2. Clique em "Novo Medicamento" para adicionar um medicamento
3. Informe o nome, dosagem, forma de administração e horários
4. Marque cada dose como "Tomada" quando for administrada

Você pode visualizar um calendário com todos os horários programados e receber lembretes.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_activities_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Atividades")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Gerenciamento de Atividades Físicas

Nesta seção, você pode registrar e acompanhar suas atividades físicas.

## Funcionalidades

- **Registro de Atividades**: Tipo, duração, intensidade, calorias
- **Tipos de Exercícios**: Cardio, musculação, flexibilidade, etc.
- **Metas**: Defina e acompanhe metas de exercícios
- **Progresso**: Visualize seu progresso em gráficos

## Como Utilizar

1. Acesse a seção "Atividades Físicas" no menu principal
2. Clique em "Nova Atividade" para registrar um exercício
3. Selecione o tipo e informe os detalhes da atividade
4. Acompanhe seu histórico e estatísticas

Você pode definir uma rotina de exercícios e verificar sua aderência ao longo do tempo.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_appointments_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Consultas")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Gerenciamento de Consultas Médicas

Nesta seção, você pode organizar suas consultas médicas passadas e futuras.

## Funcionalidades

- **Agendamento**: Registre data, hora, médico e local
- **Especialidades**: Organize consultas por especialidade médica
- **Lembretes**: Receba notificações antes das consultas
- **Histórico**: Mantenha um registro de consultas passadas e diagnósticos

## Como Utilizar

1. Acesse a seção "Consultas" no menu principal
2. Clique em "Nova Consulta" para agendar uma consulta
3. Informe o médico, especialidade, data, hora e local
4. Após a consulta, registre o diagnóstico e recomendações

Você pode anexar documentos como receitas, exames e recomendações médicas.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Relatórios")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Relatórios de Saúde

Nesta seção, você pode gerar relatórios e visualizar estatísticas sobre sua saúde.

## Tipos de Relatórios

- **Evolução de Medidas**: Gráficos de peso, IMC, circunferências, etc.
- **Adesão a Medicamentos**: Taxas de adesão e histórico
- **Atividades Físicas**: Frequência, duração e calorias por período
- **Consultas Médicas**: Histórico e próximas consultas
- **Resumo Geral**: Visão geral de todos os aspectos da sua saúde

## Como Utilizar

1. Acesse a seção "Relatórios" no menu principal
2. Selecione o tipo de relatório desejado
3. Defina o período de análise (semana, mês, ano)
4. Visualize ou exporte o relatório gerado

Você pode exportar os relatórios em formato PDF para compartilhar com seus médicos.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura
    
    def create_faq_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="FAQ")
        
        # Scroll
        scroll = ttk.Scrollbar(tab)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto
        text = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10, yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        scroll.config(command=text.yview)
        
        # Conteúdo
        content = """# Perguntas Frequentes

## Como meus dados são armazenados?
Seus dados são armazenados localmente no seu computador, em arquivos JSON na pasta "data" do aplicativo. Não compartilhamos seus dados com terceiros.

## Posso perder meus dados?
Recomendamos realizar backups regularmente utilizando a função "Exportar Dados" no menu "Arquivo". Assim, você pode restaurar seus dados caso necessário.

## É possível sincronizar entre dispositivos?
Atualmente, o aplicativo não oferece sincronização nativa. No entanto, você pode exportar seus dados e importá-los em outro dispositivo.

## Posso compartilhar relatórios com meu médico?
Sim! Todos os relatórios podem ser exportados em formato PDF para serem compartilhados com seus profissionais de saúde.

## Como configurar lembretes?
Acesse "Configurações" no menu principal e verifique a seção de notificações. Você pode definir lembretes para medicamentos e consultas.

## O aplicativo substitui orientações médicas?
Não. Este aplicativo é apenas uma ferramenta de organização e acompanhamento. Sempre siga as orientações dos seus profissionais de saúde.

## Preciso de internet para usar o aplicativo?
Não, o aplicativo funciona completamente offline.

## Como posso proteger meus dados pessoais?
Acesse "Configurações" e ative a proteção por senha para garantir que apenas você tenha acesso aos seus dados de saúde.
"""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)  # Tornar somente leitura


def show_help(parent):
    """Abre a janela de ajuda"""
    HelpWindow(parent)