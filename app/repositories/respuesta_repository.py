from app.core.database import Database
from app.models.Respuesta import Respuesta


class RespuestaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM respuestas
                ORDER BY respuesta_id ASC;
            """)

            respuestas = cursor.fetchall()
            conn.close()

            return respuestas

        except Exception as e:
            print(f"Error al obtener respuestas: {e}")
            return []

    def obtener_por_id(self, respuesta_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM respuestas
                WHERE respuesta_id = %s;
            """, (respuesta_id,))

            respuesta = cursor.fetchone()
            conn.close()

            return respuesta

        except Exception as e:
            print(f"Error al obtener respuesta: {e}")
            return None

    def crear(self, respuesta: Respuesta):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO respuestas
                (
                    pregunta_id,
                    puntaje,
                    comentario,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING respuesta_id;
            """, (
                respuesta.pregunta_id,
                respuesta.puntaje,
                respuesta.comentario,
                respuesta.estado
            ))

            nuevo_id = cursor.fetchone()["respuesta_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear respuesta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, respuesta_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM respuestas
                WHERE respuesta_id = %s
                RETURNING respuesta_id;
            """, (respuesta_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar respuesta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, respuesta_id: int, respuesta: Respuesta):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE respuestas
                SET pregunta_id = %s,
                    puntaje = %s,
                    comentario = %s,
                    estado = %s
                WHERE respuesta_id = %s
                RETURNING respuesta_id;
            """, (
                respuesta.pregunta_id,
                respuesta.puntaje,
                respuesta.comentario,
                respuesta.estado,
                respuesta_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar respuesta: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False