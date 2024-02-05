import pandas as pd
import pymysql

class DadosVendas:
    def __init__(self, conexao):
        self.conexao = conexao

    def obter_dados_vendas(self):
        query = """
            SELECT 
                venda.cd_periodo_dia,
                dp.ds_neogrupo,
                dp.ds_categoria_master,
                dp.ds_categoria,
                dp.ds_sub_categoria,
                dp.ds_classe_terapeutica_raia,
                SUM(venda.vl_rbv_apos_dev) AS vendas
            FROM 
                rd_corp.fat_venda_produto_dia venda
                LEFT JOIN rd_corp.dim_produto dp ON (dp.cd_produto = venda.cd_produto AND dp.fl_ultima_versao = 1)
            WHERE 
                venda.cd_cliente NOT IN ('-1', '-2')
                AND (venda.cd_periodo_mes = DATE_FORMAT(CURDATE(), '%Y%m') OR venda.cd_periodo_mes = DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y%m'))
            GROUP BY 
                venda.cd_periodo_dia, dp.ds_neogrupo, dp.ds_categoria_master, dp.ds_categoria, dp.ds_sub_categoria, dp.ds_classe_terapeutica_raia
        """

        # Conectar ao banco de dados
        with self.conexao.cursor() as cursor:
            cursor.execute(query)
            resultado_query = cursor.fetchall()

        # Criar um DataFrame com os resultados
        colunas = ["cd_periodo_dia", "ds_neogrupo", "ds_categoria_master", "ds_categoria", "ds_sub_categoria", "ds_classe_terapeutica_raia", "vendas"]
        df = pd.DataFrame(resultado_query, columns=colunas)

        return df

    def calcular_diferenca_por_neogrupo(self):
        dados_vendas = self.obter_dados_vendas()

        # Calcular a diferença por ds_neogrupo
        diferenca_por_neogrupo = dados_vendas.groupby("ds_neogrupo")["vendas"].diff().fillna(0)

        # Adicionar a coluna de diferença ao DataFrame original
        dados_vendas["diferenca_por_neogrupo"] = diferenca_por_neogrupo

        return dados_vendas

# Exemplo de uso
conexao = pymysql.connect(host='bi-cloud.dados.rd.com.br', user='rudpsilva', password='itLwluGcZdH1', database='poc-rd')
dados_vendas_obj = DadosVendas(conexao)
resultado_final = dados_vendas_obj.calcular_diferenca_por_neogrupo()
print(resultado_final)
