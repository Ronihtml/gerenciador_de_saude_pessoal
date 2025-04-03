import os
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Garantir que o diretório de dados existe
def verificar_diretorio():
    if not os.path.exists("dados"):
        os.makedirs("dados")

# Carregar dados de um arquivo JSON
def carregar_dados(arquivo):
    verificar_diretorio()
    caminho = f"dados/{arquivo}.json"
    
    if os.path.exists(caminho):
        try:
            with open(caminho, "r") as file:
                return json.load(file)
        except:
            messagebox.showerror("Erro", f"Erro ao carregar dados de {arquivo}.")
            return []
    else:
        return []

# Salvar dados em um arquivo JSON
def salvar_dados(arquivo, dados):
    verificar_diretorio()
    caminho = f"dados/{arquivo}.json"
    
    try:
        with open(caminho, "w") as file:
            json.dump(dados, file, indent=4)
        return True
    except:
        messagebox.showerror("Erro", f"Erro ao salvar dados em {arquivo}.")
        return False

# Validar uma data no formato DD/MM/AAAA
def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Criar um campo de entrada com rótulo
def criar_campo(frame, texto, row, column, width=20):
    tk.Label(frame, text=texto).grid(row=row, column=column, padx=5, pady=5, sticky="e")
    entry = tk.Entry(frame, width=width)
    entry.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
    return entry

# Calcular o IMC
def calcular_imc(peso, altura):
    try:
        peso_float = float(peso)
        altura_float = float(altura)
        imc = peso_float / (altura_float ** 2)
        return round(imc, 2)
    except:
        return 0

# Obter a classificação do IMC
def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidade"

# Criar um estilo consistente para os botões
def configurar_botao(botao, cor="#4CAF50", cor_texto="white"):
    botao.configure(bg=cor, fg=cor_texto, pady=5)
    return botao