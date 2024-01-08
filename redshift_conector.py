import psycopg2

class RedshiftConnector:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
    def executar_query(self, query):
        try:
            conexao = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conexao.cursor()
            cursor.execute(query)
            dados = cursor.fetchall()
            return dados

        except Exception as e:
            print(f"Erro na execução da query: {e}")

        finally:
            if conexao:
                conexao.close()
