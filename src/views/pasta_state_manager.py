class PastaStateManager:
    _instance = None
    _estados = {}  # Dicionário para armazenar o estado de cada pasta

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PastaStateManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_estado(self, pasta_id):
        """Retorna o estado atual de uma pasta"""
        return self._estados.get(pasta_id, False)  # False = fechada por padrão

    def set_estado(self, pasta_id, estado):
        """Define o estado de uma pasta"""
        self._estados[pasta_id] = estado

    def fechar_pasta(self, pasta_id):
        """Fecha uma pasta (usado pelo Repositor)"""
        self._estados[pasta_id] = False
        return False

    def abrir_pasta(self, pasta_id):
        """Abre uma pasta (usado pelo Vendedor)"""
        self._estados[pasta_id] = True
        return True