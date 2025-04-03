import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from gerencer_saude.core.utils import center_window

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.settings_file = "data/settings.json"
        self.settings = self.load_settings()
        
        # Criar janela de configurações
        self.window = tk.Toplevel(parent)
        self.window.title("Configurações")
        self.window.geometry("500x450")
        self.window.resizable(False, False)
        center_window(self.window)
        
        # Estilo
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Frame principal
        self.main_frame = ttk.Frame(self.window, padding="20 20 20 20", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(self.main_frame, text="Configurações do Aplicativo", 
                 style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Configurações gerais
        ttk.Label(self.main_frame, text="Configurações Gerais", 
                 font=("Arial", 11, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Notificações
        ttk.Label(self.main_frame, text="Ativar notificações:").grid(row=2, column=0, sticky="w", pady=5)
        self.notifications_var = tk.BooleanVar(value=self.settings.get("notifications", True))
        ttk.Checkbutton(self.main_frame, variable=self.notifications_var).grid(row=2, column=1, sticky="w")
        
        # Tema
        ttk.Label(self.main_frame, text="Tema:").grid(row=3, column=0, sticky="w", pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "Claro"))
        themes = ["Claro", "Escuro", "Sistema"]
        ttk.Combobox(self.main_frame, textvariable=self.theme_var, 
                     values=themes, state="readonly", width=15).grid(row=3, column=1, sticky="w")
        
        # Lembrete de consultas
        ttk.Label(self.main_frame, text="Lembrete de consultas (dias antes):").grid(row=4, column=0, sticky="w", pady=5)
        self.reminder_var = tk.IntVar(value=self.settings.get("reminder_days", 3))
        reminder_spin = ttk.Spinbox(self.main_frame, from_=1, to=30, textvariable=self.reminder_var, width=5)
        reminder_spin.grid(row=4, column=1, sticky="w")
        
        # Unidades de medida
        ttk.Label(self.main_frame, text="Unidades de Medida", 
                 font=("Arial", 11, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        # Peso
        ttk.Label(self.main_frame, text="Unidade de peso:").grid(row=6, column=0, sticky="w", pady=5)
        self.weight_unit_var = tk.StringVar(value=self.settings.get("weight_unit", "kg"))
        weight_units = ["kg", "lb"]
        ttk.Combobox(self.main_frame, textvariable=self.weight_unit_var, 
                    values=weight_units, state="readonly", width=15).grid(row=6, column=1, sticky="w")
        
        # Altura
        ttk.Label(self.main_frame, text="Unidade de altura:").grid(row=7, column=0, sticky="w", pady=5)
        self.height_unit_var = tk.StringVar(value=self.settings.get("height_unit", "cm"))
        height_units = ["cm", "m", "pés/polegadas"]
        ttk.Combobox(self.main_frame, textvariable=self.height_unit_var, 
                    values=height_units, state="readonly", width=15).grid(row=7, column=1, sticky="w")
        
        # Temperatura
        ttk.Label(self.main_frame, text="Unidade de temperatura:").grid(row=8, column=0, sticky="w", pady=5)
        self.temp_unit_var = tk.StringVar(value=self.settings.get("temp_unit", "°C"))
        temp_units = ["°C", "°F"]
        ttk.Combobox(self.main_frame, textvariable=self.temp_unit_var, 
                    values=temp_units, state="readonly", width=15).grid(row=8, column=1, sticky="w")
        
        # Privacidade
        ttk.Label(self.main_frame, text="Privacidade", 
                 font=("Arial", 11, "bold")).grid(row=9, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        # Senha
        ttk.Label(self.main_frame, text="Proteger com senha:").grid(row=10, column=0, sticky="w", pady=5)
        self.password_var = tk.BooleanVar(value=self.settings.get("password_protected", False))
        ttk.Checkbutton(self.main_frame, variable=self.password_var, 
                       command=self.toggle_password).grid(row=10, column=1, sticky="w")
        
        # Campo de senha
        ttk.Label(self.main_frame, text="Definir senha:").grid(row=11, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*", width=20)
        self.password_entry.grid(row=11, column=1, sticky="w")
        self.password_entry.insert(0, self.settings.get("password", ""))
        
        # Botões
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=12, column=0, columnspan=2, pady=(30, 0))
        
        ttk.Button(button_frame, text="Salvar", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Restaurar Padrões", 
                  command=self.restore_defaults).pack(side=tk.LEFT, padx=5)
        
        # Atualizar estado inicial dos widgets
        self.toggle_password()
    
    def toggle_password(self):
        if self.password_var.get():
            self.password_entry.config(state="normal")
        else:
            self.password_entry.config(state="disabled")
    
    def load_settings(self):
        # Criar pasta data se não existir
        os.makedirs("data", exist_ok=True)
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    return json.load(f)
            else:
                # Configurações padrão
                default_settings = {
                    "notifications": True,
                    "theme": "Claro",
                    "reminder_days": 3,
                    "weight_unit": "kg",
                    "height_unit": "cm",
                    "temp_unit": "°C",
                    "password_protected": False,
                    "password": ""
                }
                # Salvar as configurações padrão
                with open(self.settings_file, "w") as f:
                    json.dump(default_settings, f, indent=4)
                return default_settings
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")
            return {}
    
    def save_settings(self):
        try:
            settings = {
                "notifications": self.notifications_var.get(),
                "theme": self.theme_var.get(),
                "reminder_days": self.reminder_var.get(),
                "weight_unit": self.weight_unit_var.get(),
                "height_unit": self.height_unit_var.get(),
                "temp_unit": self.temp_unit_var.get(),
                "password_protected": self.password_var.get(),
                "password": self.password_entry.get() if self.password_var.get() else ""
            }
            
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=4)
                
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def restore_defaults(self):
        if messagebox.askyesno("Restaurar Padrões", 
                              "Tem certeza que deseja restaurar todas as configurações para os valores padrão?"):
            # Configurações padrão
            self.notifications_var.set(True)
            self.theme_var.set("Claro")
            self.reminder_var.set(3)
            self.weight_unit_var.set("kg")
            self.height_unit_var.set("cm")
            self.temp_unit_var.set("°C")
            self.password_var.set(False)
            self.password_entry.delete(0, tk.END)
            
            # Atualizar interface
            self.toggle_password()


def get_settings():
    """Carrega e retorna as configurações do aplicativo"""
    settings_file = "data/settings.json"
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                return json.load(f)
        else:
            # Se o arquivo não existir, retorna as configurações padrão
            return {
                "notifications": True,
                "theme": "Claro",
                "reminder_days": 3,
                "weight_unit": "kg",
                "height_unit": "cm",
                "temp_unit": "°C",
                "password_protected": False,
                "password": ""
            }
    except Exception:
        # Em caso de erro, retorna as configurações padrão
        return {
            "notifications": True,
            "theme": "Claro",
            "reminder_days": 3,
            "weight_unit": "kg",
            "height_unit": "cm",
            "temp_unit": "°C",
            "password_protected": False,
            "password": ""
        }


def apply_theme(root):
    """Aplica o tema selecionado à interface"""
    settings = get_settings()
    theme = settings.get("theme", "Claro")
    
    style = ttk.Style()
    
    if theme == "Escuro":
        # Configurações do tema escuro
        root.configure(bg="#2E2E2E")
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        style.configure("TButton", background="#4A4A4A", foreground="#FFFFFF")
        style.configure("TEntry", fieldbackground="#4A4A4A", foreground="#FFFFFF")
        style.configure("TCombobox", fieldbackground="#4A4A4A", foreground="#FFFFFF")
        style.configure("Header.TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Arial", 12, "bold"))
    else:
        # Configurações do tema claro
        root.configure(bg="#F0F0F0")
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", foreground="#000000")
        style.configure("TButton", background="#E0E0E0", foreground="#000000")
        style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#000000")
        style.configure("TCombobox", fieldbackground="#FFFFFF", foreground="#000000")
        style.configure("Header.TLabel", background="#F0F0F0", foreground="#000000", font=("Arial", 12, "bold"))