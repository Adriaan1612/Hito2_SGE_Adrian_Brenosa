import pymysql

class ConexionBD:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db)
        self.cursor = self.connection.cursor()

    def ejecutar_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def obtener_datos(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def cerrar(self):
        self.cursor.close()
        self.connection.close()