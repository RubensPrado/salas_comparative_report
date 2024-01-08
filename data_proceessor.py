class DadosProcessor:
    def __init__(self, dados):
        self.dados = dados

    def processar_dados(self):

        dados_formatados = []
        for registro in self.dados:
            dados_formatados.append(f"<p>{registro[0]}: {registro[1]}</p>")
        return "".join(dados_formatados)