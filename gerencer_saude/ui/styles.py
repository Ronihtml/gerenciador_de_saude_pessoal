import tkinter as tk
from tkinter import ttk

class AppStyles:
    """Classe para configurar estilos consistentes em toda a aplicação"""
    
    @staticmethod
    def configure_styles():
        """Configura os estilos padrão para toda a aplicação"""
        style = ttk.Style()
        
        # Cores
        bg_color = "#f0f0f0"
        accent_color = "#4a7abc"
        button_color = "#5a8aca"
        
        # Configurações gerais
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11), padding=5)
        style.configure("TEntry", font=("Arial", 11))
        style.configure("TCombobox", font=("Arial", 11))
        
        # Cabeçalhos
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#333333")
        style.configure("Subheader.TLabel", font=("Arial", 14, "bold"), foreground="#444444")
        
        # Botões
        style.configure("Primary.TButton", background="#F8F8FF", foreground="black")
        style.map("Primary.TButton",
                 background=[("active", accent_color), ("pressed", "#3a6aac")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Botões de ação
        style.configure("Add.TButton", background="#4caf50", foreground="white")
        style.map("Add.TButton",
                 background=[("active", "#45a049"), ("pressed", "#3d8b40")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        style.configure("Delete.TButton", background="#f44336", foreground="white")
        style.map("Delete.TButton",
                 background=[("active", "#e53935"), ("pressed", "#d32f2f")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Treeview (para tabelas)
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        return style
    
    @staticmethod
    def create_form_field(parent, label_text, row, column=0, entry_width=30, input_type="entry"):
        """Cria um campo de formulário com label e entrada"""
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=column, sticky="w", padx=5, pady=5)
        
        if input_type == "entry":
            field = ttk.Entry(parent, width=entry_width)
            field.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
        elif input_type == "combobox":
            field = ttk.Combobox(parent, width=entry_width-3)
            field.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
        elif input_type == "date":
            frame = ttk.Frame(parent)
            frame.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
            
            day = ttk.Combobox(frame, width=3, values=[str(i).zfill(2) for i in range(1, 32)])
            day.pack(side=tk.LEFT, padx=2)
            day.set("01")
            
            month = ttk.Combobox(frame, width=3, values=[str(i).zfill(2) for i in range(1, 13)])
            month.pack(side=tk.LEFT, padx=2)
            month.set("01")
            
            year = ttk.Combobox(frame, width=5, values=[str(i) for i in range(2020, 2031)])
            year.pack(side=tk.LEFT, padx=2)
            year.set("2024")
            
            field = (day, month, year)
        elif input_type == "text":
            field = tk.Text(parent, width=entry_width, height=5)
            field.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
        
        return label, field
    
    @staticmethod
    def setup_treeview(parent, columns, column_widths=None):
        """Configura um Treeview com cabeçalhos e scrollbar"""
        frame = ttk.Frame(parent)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configurar colunas
        for i, col in enumerate(columns):
            width = column_widths[i] if column_widths and i < len(column_widths) else 100
            tree.column(col, width=width, anchor="w")
            tree.heading(col, text=col.title())
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
        return frame, tree