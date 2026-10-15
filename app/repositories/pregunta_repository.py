from app.core.database import Database
from app.models.Pregunta import Pregunta


class PreguntaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM preguntas
                ORDER BY pregunta_id ASC;
            """)

            preguntas = cursor.fetchall()
            conn.close()

            return preguntas

        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
            return []

    def obtener_por_id(self, pregunta_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM preguntas
                WHERE pregunta_id = %s;
            """, (pregunta_id,))

            pregunta = cursor.fetchone()
            conn.close()

            return pregunta

        except Exception as e:
            print(f"Error al obtener pregunta: {e}")
            return None

    def crear(self, pregunta: Pregunta):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO preguntas
                (
                    evaluacion_id,
                    texto_pregunta,
                    numero_orden,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING pregunta_id;
            """, (
                pregunta.evaluacion_id,
                pregunta.texto_pregunta,
                pregunta.numero_orden,
                pregunta.estado
            ))

            nuevo_id = cursor.fetchone()["pregunta_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear pregunta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, pregunta_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM preguntas
                WHERE pregunta_id = %s
                RETURNING pregunta_id;
            """, (pregunta_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar pregunta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, pregunta_id: int, pregunta: Pregunta):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE preguntas
                SET evaluacion_id = %s,
                    texto_pregunta = %s,
                    numero_orden = %s,
                    estado = %s
                WHERE pregunta_id = %s
                RETURNING pregunta_id;
            """, (
                pregunta.evaluacion_id,
                pregunta.texto_pregunta,
                pregunta.numero_orden,
                pregunta.estado,
                pregunta_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar pregunta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False