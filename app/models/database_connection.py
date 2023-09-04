import psycopg2

class DatabaseConnection:
    conn = None

    def __init__(self, donde:str ="-"):
        print("iniciando?",donde)
        try:
            self.conn = psycopg2.connect(
                "dbname=fdpkijde user=fdpkijde password=BSaXT5TQ8uOvLYRRTQnCCqrH8c8-bDzQ host=rosie.db.elephantsql.com"
            )
        except psycopg2.OperationalError as err:
            print(err)
            self.conn.close()

    def get_connection(self):
        return self.conn

    def close_connection(self,donde:str ="*"):
        print("cerrando: ",donde)
        self.conn.close()