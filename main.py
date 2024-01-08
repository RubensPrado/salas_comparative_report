from email_config import EmailConfig
from sales_report import SalesReport
from to_email import ToEmail
from redshift_conector import RedshiftConnector


class Main:
    def __init__(self):
        self.config_email = EmailConfig()
        self.relatorio_vendas = SalesReport()
        self.enviador = ToEmail(self.config_email, self.relatorio_vendas)
        
    def extrair_dados_redshift(self):
        query = 'SELECT * FROM sua_tabela;'
        dados_redshift = self.extractor.extrair_dados(query)
        return dados_redshift

    def run(self):
        dados_redshift = self.extrair_dados_redshift()
        self.relatorio_vendas.dados_redshift = dados_redshift
        
        self.enviador.enviar_email()

if __name__ == "__main__":
    main = Main()
    main.run()


