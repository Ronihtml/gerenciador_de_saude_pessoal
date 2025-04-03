import os
import json
import datetime

class DataManager:
    def __init__(self):
        # Diretório para armazenar os dados
        self.data_dir = "dados"
        self.ensure_data_directory()
        
        # Arquivos de dados
        self.perfil_file = os.path.join(self.data_dir, "perfil.json")
        self.medidas_file = os.path.join(self.data_dir, "medidas.json")
        self.medicamentos_file = os.path.join(self.data_dir, "medicamentos.json")
        self.atividades_file = os.path.join(self.data_dir, "atividades.json")
        self.consultas_file = os.path.join(self.data_dir, "consultas.json")
        
        # Inicializar arquivos
        self.initialize_files()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados exista"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def initialize_files(self):
        """Inicializa os arquivos de dados se não existirem"""
        files = {
            self.perfil_file: {},
            self.medidas_file: [],
            self.medicamentos_file: [],
            self.atividades_file: [],
            self.consultas_file: []
        }
        
        for file_path, default_data in files.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=4)
    
    def load_data(self, file_path):
        """Carrega dados de um arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, cria um novo
            default_data = [] if file_path != self.perfil_file else {}
            self.save_data(file_path, default_data)
            return default_data
    
    def save_data(self, file_path, data):
        """Salva dados em um arquivo JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Métodos específicos para cada tipo de dado
    def get_perfil(self):
        return self.load_data(self.perfil_file)
    
    def save_perfil(self, perfil_data):
        self.save_data(self.perfil_file, perfil_data)
    
    def get_medidas(self):
        return self.load_data(self.medidas_file)
    
    def add_medida(self, medida):
        medidas = self.get_medidas()
        medida['id'] = self.generate_id(medidas)
        medidas.append(medida)
        self.save_data(self.medidas_file, medidas)
    
    def update_medida(self, medida_id, updated_medida):
        medidas = self.get_medidas()
        for i, medida in enumerate(medidas):
            if medida.get('id') == medida_id:
                updated_medida['id'] = medida_id
                medidas[i] = updated_medida
                break
        self.save_data(self.medidas_file, medidas)
    
    def delete_medida(self, medida_id):
        medidas = self.get_medidas()
        medidas = [m for m in medidas if m.get('id') != medida_id]
        self.save_data(self.medidas_file, medidas)
    
    def get_medicamentos(self):
        return self.load_data(self.medicamentos_file)
    
    def add_medicamento(self, medicamento):
        medicamentos = self.get_medicamentos()
        medicamento['id'] = self.generate_id(medicamentos)
        medicamentos.append(medicamento)
        self.save_data(self.medicamentos_file, medicamentos)
    
    def update_medicamento(self, medicamento_id, updated_medicamento):
        medicamentos = self.get_medicamentos()
        for i, medicamento in enumerate(medicamentos):
            if medicamento.get('id') == medicamento_id:
                updated_medicamento['id'] = medicamento_id
                medicamentos[i] = updated_medicamento
                break
        self.save_data(self.medicamentos_file, medicamentos)
    
    def delete_medicamento(self, medicamento_id):
        medicamentos = self.get_medicamentos()
        medicamentos = [m for m in medicamentos if m.get('id') != medicamento_id]
        self.save_data(self.medicamentos_file, medicamentos)
    
    def get_atividades(self):
        return self.load_data(self.atividades_file)
    
    def add_atividade(self, atividade):
        atividades = self.get_atividades()
        atividade['id'] = self.generate_id(atividades)
        atividades.append(atividade)
        self.save_data(self.atividades_file, atividades)
    
    def update_atividade(self, atividade_id, updated_atividade):
        atividades = self.get_atividades()
        for i, atividade in enumerate(atividades):
            if atividade.get('id') == atividade_id:
                updated_atividade['id'] = atividade_id
                atividades[i] = updated_atividade
                break
        self.save_data(self.atividades_file, atividades)
    
    def delete_atividade(self, atividade_id):
        atividades = self.get_atividades()
        atividades = [a for a in atividades if a.get('id') != atividade_id]
        self.save_data(self.atividades_file, atividades)
    
    def get_consultas(self):
        return self.load_data(self.consultas_file)
    
    def add_consulta(self, consulta):
        consultas = self.get_consultas()
        consulta['id'] = self.generate_id(consultas)
        consultas.append(consulta)
        self.save_data(self.consultas_file, consultas)
    
    def update_consulta(self, consulta_id, updated_consulta):
        consultas = self.get_consultas()
        for i, consulta in enumerate(consultas):
            if consulta.get('id') == consulta_id:
                updated_consulta['id'] = consulta_id
                consultas[i] = updated_consulta
                break
        self.save_data(self.consultas_file, consultas)
    
    def delete_consulta(self, consulta_id):
        consultas = self.get_consultas()
        consultas = [c for c in consultas if c.get('id') != consulta_id]
        self.save_data(self.consultas_file, consultas)
    
    def generate_id(self, items):
        """Gera um ID único para um novo item"""
        if not items:
            return 1
        
        max_id = max(item.get('id', 0) for item in items)
        return max_id + 1