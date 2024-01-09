# -*- coding: utf-8 -*-

from email_config import EmailConfig
from sales_report import SalesReport
from to_email import ToEmail
from redshift_conector import RedshiftConnector


class Main:
    def __init__(self):
        self.config_email = EmailConfig()
        self.redshift_connector = RedshiftConnector()
        self.redshift_connector.connect()
        self.relatorio_vendas = SalesReport(self.redshift_connector)
        self.html_resultados = self.relatorio_vendas.gerar_mensagem_html()
        self.redshift_connector.disconnect()
        self.enviador = ToEmail(self.config_email, self.relatorio_vendas)

    def run(self):
        self.enviador.enviar_email()

if __name__ == "__main__":
    main = Main()
    main.run()


