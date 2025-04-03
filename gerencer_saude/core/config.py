# Configurações do aplicativo de gerenciamento de saúde pessoal

# Cores do tema
CORES = {
    "primaria": "#4CAF50",       # Verde
    "secundaria": "#2196F3",     # Azul
    "acento": "#FF9800",         # Laranja
    "erro": "#f44336",           # Vermelho
    "sucesso": "#4CAF50",        # Verde
    "aviso": "#FFC107",          # Amarelo
    "info": "#2196F3",           # Azul
    "texto": "#212121",          # Cinza escuro
    "fundo": "#F5F5F5",          # Cinza claro
    "fundo_card": "#FFFFFF"      # Branco
}

# Configurações da janela principal
APP_TITULO = "Gerenciador de Saúde Pessoal"
APP_LARGURA = 800
APP_ALTURA = 600
APP_REDIMENSIONAR = True

# Opções do menu principal
MENU_OPCOES = [
    {"nome": "Perfil", "icone": "👤", "cor": CORES["primaria"]},
    {"nome": "Medidas", "icone": "📏", "cor": CORES["secundaria"]},
    {"nome": "Medicamentos", "icone": "💊", "cor": CORES["acento"]},
    {"nome": "Atividades", "icone": "🏃", "cor": CORES["primaria"]},
    {"nome": "Consultas", "icone": "🩺", "cor": CORES["secundaria"]},
    {"nome": "Relatórios", "icone": "📊", "cor": CORES["acento"]}
]

# Tipos de atividades físicas
TIPOS_ATIVIDADES = [
    "Caminhada",
    "Corrida",
    "Ciclismo",
    "Natação",
    "Musculação",
    "Yoga",
    "Pilates",
    "Funcional",
    "Dança",
    "Outro"
]

# Especialidades médicas comuns
ESPECIALIDADES = [
    "Clínico Geral",
    "Cardiologia",
    "Dermatologia",
    "Endocrinologia",
    "Gastroenterologia",
    "Ginecologia",
    "Neurologia",
    "Oftalmologia",
    "Ortopedia",
    "Pediatria",
    "Psiquiatria",
    "Urologia",
    "Outra"
]

# Frequências de medicação
FREQUENCIAS_MEDICACAO = [
    "Diária",
    "2x ao dia",
    "3x ao dia",
    "4x ao dia",
    "Semanal",
    "Quinzenal",
    "Mensal",
    "Conforme necessário"
]