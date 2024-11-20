class Encuesta:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def crear_encuesta(self, encuesta_data):
        query = """
        INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana,
                             BebidasDestiladasSemana, VinosSemana, PerdidasControl,
                             DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.db_connection.ejecutar_query(query, encuesta_data)

    def obtener_encuestas(self, query=None, params=None):
        if query is None:
            query = "SELECT * FROM ENCUESTA"
        if params is None:
            params = []

        self.db_connection.cursor.execute(query, params)
        encuestas = self.db_connection.cursor.fetchall()
        return encuestas

    def obtener_encuesta_por_id(self, encuesta_id):
        query = "SELECT * FROM ENCUESTA WHERE idEncuesta = %s;"
        return self.db_connection.obtener_datos(query, (encuesta_id,))

    def actualizar_encuesta(self, encuesta_id, encuesta_data):
        query = """
        UPDATE ENCUESTA SET
            edad = %s, Sexo = %s, BebidasSemana = %s, CervezasSemana = %s,
            BebidasFinSemana = %s, BebidasDestiladasSemana = %s, VinosSemana = %s,
            PerdidasControl = %s, DiversionDependenciaAlcohol = %s, ProblemasDigestivos = %s,
            TensionAlta = %s, DolorCabeza = %s
        WHERE idEncuesta = %s;
        """
        self.db_connection.ejecutar_query(query, encuesta_data + (encuesta_id,))

    def eliminar_encuesta(self, encuesta_id):
        query = "DELETE FROM ENCUESTA WHERE idEncuesta = %s;"
        self.db_connection.ejecutar_query(query, (encuesta_id,))