from datetime import datetime, timedelta
from redshift_conector import RedshiftConnector

class SalesReport:
    def __init__(self, redshift_connector=None):
        self.data_atual = datetime.now()
        self.data_anterior = self.data_atual - timedelta(days=1)
        self.data_formatada = self.data_anterior.strftime("%d/%m")
        self.link = "https://docs.google.com/spreadsheets/d/1D1zaCjjf9XfdO321x3JDAFT-PoL51mquMg8PW_R5xt8/edit#gid=0"
    
    def obter_dados_redshift(self):
        redshift_connector = RedshiftConnector()
        redshift_connector.connect()
        
        try:
            dados = redshift_connector.executar_query()
            return dados
        finally:
            redshift_connector.disconnect()


    def gerar_mensagem_html(self):

        dados_redshift = self.obter_dados_redshift()

        if dados_redshift:
            # Construa a tabela HTML com base nos dados da consulta
            tabela_html = "<table border='1'><tr><th>cd_periodo_dia</th><th>ds_neogrupo</th><th>ds_categoria_master</th><th>ds_categoria</th><th>ds_sub_categoria</th><th>ds_classe_terapeutica_raia</th><th>vendas</th></tr>"

            for linha in dados_redshift:
                tabela_html += "<tr>"
                for coluna in linha:
                    tabela_html += f"<td>{coluna}</td>"
                tabela_html += "</tr>"

            tabela_html += "</table>" 

        mensagem_html = f"""
        <body>

            <p><strong>Bom dia, tudo bem?</strong></p>

            <h1>Relatório Comparativo de Vendas</h1>
            <p><strong>Segue Relatório Comparativo de Vendas</strong> atualizado com dados até <strong>{self.data_formatada}</strong>.</p>
            <p>Ele pode ser acessado através do seguinte <strong><a href={self.link} target="_blank">link</a></strong>.</p>

            <h2>Destaques do Comparativo</h2>
            <p>Abaixo seguem os principais destaques do comparativo com o mês de Dezembro (para isso utilizamos como período de comparação os dias <strong>04/12 ao 07/12</strong> para o mês de Dezembro e os dias <strong>01/01 ao 04/01</strong> para o mês de Janeiro):</p>

            <h2>Diferença Total</h2>
            <p>A <font color="red"><strong>diferença total</strong></font> entre os períodos analisados é de <font color="red"><strong>-86,6 MM</strong></font>. O principal destaque do período de comparação é o neogrupo Medicamento Marca (<font color="red"><strong>-52,6 MM</strong></font>), OTC Marca (<font color="red"><strong>-12,4 MM</strong></font>) e Perfumaria (<font color="red"><strong>-10,7 MM</strong></font>).</p>

            <h2>Medicamento Marca</h2>
            <p><strong>Medicamento Marca</strong> segue com sua queda considerável na Classe Terapêutica Diabetes (<font color="red"><strong>-11,9 MM; -26,4%</strong></font>), além disso, Antidepressivos & Estabilizadores de Humor (<font color="red"><strong>-6,2 MM; -35,4%</strong></font>) e Psicoanalepticos, Álcool, Tabaco & Outros (<font color="red"><strong>-2,9 MM; -39,7%</strong></font>), também apresentam valores negativos nas vendas. Elas estão presentes nas Masters Medicamentos – RX (<font color="red"><strong>-37,5 MM; -24,6%</strong></font>) e Psicotrópicos (<font color="red"><strong>-15,0 MM; -35,4%</strong></font>).</p>

            <h2>OTC Marca</h2>
            <p>Já em <strong>OTC Marca</strong>, vemos que sua queda está entre as Classes Terapêuticas Vitaminas, Sais Minerais & Nutrientes (<font color="red"><strong>-3,3 MM; -26,4%</strong></font>) e Oftalmológicos & Otológicos (<font color="red"><strong>-1,1 MM; -22,2%</strong></font>). Que encontramos nas Masters Vitaminas (<font color="red"><strong>-3,9 MM; -27,0%</strong></font>) e Medicamentos OTC (<font color="red"><strong>-1,6 MM; -5,6%</strong></font>).</p>

            <h2>Perfumaria</h2>
            <p><strong>Perfumaria</strong>, por sua vez, segue com as quedas das Categorias Masters Pele (<font color="red"><strong>-5,6 MM; -13,7%</strong></font>) e Banho (<font color="red"><strong>-1,7 MM; -19,2%</strong></font>). Por conta das Categorias Tratamento da Pele Medicinais (<font color="red"><strong>-3,8 MM; -22,0%</strong></font>), Desodorantes (<font color="red"><strong>-1,3 MM; -21,1%</strong></font>) e Tratamento da Pele (<font color="red"><strong>-1,0 MM; -17,5%</strong></font>). Contudo, tivemos um <font color="blue"><strong>crescimento considerável</strong></font> nas vendas de Fraldas Infantis (<font color="blue"><strong>+1,7 MM; +24,7%</strong></font>).</p>

        </body>
        """.format(self.data_formatada, self.link)
        return mensagem_html

