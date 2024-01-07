import os
from dotenv import load_dotenv

class EmailConfig:
    def __init__(self):
        load_dotenv()
        self.remetente_email = os.environ.get('EMAIL_USUARIO')
        self.senha = os.environ.get('EMAIL_SENHA')
        self.destinatario_email = ["rubenseprado@gmail.com","rubenspradosilva@gmail.com"]
        self.assunto = "Relatório Comparativo de Vendas"

