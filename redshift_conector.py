import psycopg2
from dotenv import load_dotenv
import os

class RedshiftConnector:
    def __init__(self):
        load_dotenv()

        self.host = os.getenv("REDSHIFT_HOST")
        self.port = os.getenv("REDSHIFT_PORT")
        self.database = os.getenv("REDSHIFT_DATABASE")
        self.user = os.getenv("REDSHIFT_USER")
        self.password = os.getenv("REDSHIFT_PASSWORD")
        self.connection = None
        self.cursor = None
        self.query_sales_analitics = """
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
                AND venda.cd_periodo_mes >= 202201
            GROUP BY 
                venda.cd_periodo_dia, dp.ds_neogrupo, dp.ds_categoria_master, dp.ds_categoria, dp.ds_sub_categoria, dp.ds_classe_terapeutica_raia
        """
        
    def connect(self):
        try:
            print(f'Tentando conectar ao Redshift com host={self.host}, port={self.port}, ...')
            self.connection  = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                client_encoding='utf-8'
            )
            self.cursor = self.connection.cursor()
            print("Conectado ao Redshift")
        except Exception as e:
            print(f"Erro: Não foi possível conectar ao Redshift - {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do Redshift")
    
    def executar_query(self):
        try:
            if self.cursor:
                self.cursor.execute(self.query_sales_analitics)
                dados = self.cursor.fetchall()
                return dados
            else:
                print("Erro: Cursor não foi inicializado.")
                return None
        except Exception as e:
            print(f"Erro na execução da query - {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()