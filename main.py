from email_config import EmailConfig
from sales_report import SalesReport
from to_email import ToEmail

class Main:
    def __init__(self):
        self.config_email = EmailConfig()
        self.relatorio_vendas = SalesReport()
        self.enviador = ToEmail(self.config_email, self.relatorio_vendas)

    def run(self):
        self.enviador.enviar_email()

if __name__ == "__main__":
    main = Main()
    main.run()


