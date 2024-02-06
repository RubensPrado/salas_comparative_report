import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ToEmail:
    def __init__(self, config, relatorio):
        self.config = config
        self.relatorio = relatorio

    def enviar_email(self):
        servidor = None

        servidor_smtp = "smtp.gmail.com"
        porta = 587

        corpo_email = MIMEMultipart()
        corpo_email['From'] = self.config.remetente_email 
        corpo_email['To'] = ", ".join(self.config.destinatario_email)
        corpo_email['Cc'] = ", ".join(self.config.destinatario_email_cc)
        corpo_email['Subject'] = self.config.assunto
        corpo_email.attach(MIMEText(self.relatorio.gerar_mensagem_html(), 'html'))

        try:
            print('preparando email')
            servidor = smtplib.SMTP(servidor_smtp, porta)
            servidor.starttls()
            servidor.login(self.config.remetente_email, self.config.senha)

            servidor.sendmail(self.config.remetente_email, self.config.destinatario_email, corpo_email.as_string())
            print('E-mail enviado com sucesso!')

        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")

        finally:
            if servidor is not None:
                servidor.quit()
