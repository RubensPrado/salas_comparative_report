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
        self.query_sales_analitics ="""
          select 
            venda.cd_periodo_dia 
            ,dp.ds_neogrupo 
            ,dp.ds_categoria_master 
            ,dp.ds_categoria 
            --,dp.ds_produto 
            ,dp.ds_sub_categoria 
            ,dp.ds_classe_terapeutica_raia  
            ,sum(venda.vl_rbv_apos_dev) as vendas
        from rd_corp.fat_venda_produto_dia venda		
            left join rd_corp.dim_produto dp on (dp.cd_produto = venda.cd_produto and dp.fl_ultima_versao = 1)
        where venda.cd_cliente not in ('-1','-2')
            and venda.cd_periodo_mes >= 202201
            --and venda.cd_periodo_dia = 20230705
        group by venda.cd_periodo_dia, dp.ds_neogrupo, dp.ds_categoria_master, dp.ds_categoria ,dp.ds_sub_categoria, dp.ds_classe_terapeutica_raia
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
            print('executando a query')
            if self.cursor:
                self.cursor.execute(self.query_sales_analitics)
                dados = self.cursor.fetchall()
                print(dados)
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