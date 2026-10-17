
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Pregunta import Pregunta


class PreguntaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_preguntas,
                        texto_preguntas,
                        numero_orden,
                        estado,
                        created_at,
                        updated_at
                    FROM preguntas
                    ORDER BY
                        numero_orden ASC NULLS LAST,
                        id_preguntas ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar preguntas: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_preguntas: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_preguntas,
                        texto_preguntas,
                        numero_orden,
                        estado,
                        created_at,
                        updated_at
                    FROM preguntas
                    WHERE id_preguntas = %s;
                """, (id_preguntas,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar pregunta: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, pregunta: Pregunta):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO preguntas (
                        texto_preguntas,
                        numero_orden,
                        estado
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id_preguntas;
                """, (
                    pregunta.texto_preguntas,
                    pregunta.numero_orden,
                    pregunta.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_preguntas"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear pregunta: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_preguntas: int, pregunta: Pregunta):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE preguntas
                    SET
                        texto_preguntas = %s,
                        numero_orden = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_preguntas = %s
                    RETURNING id_preguntas;
                """, (
                    pregunta.texto_preguntas,
                    pregunta.numero_orden,
                    pregunta.estado,
                    id_preguntas
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar pregunta: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_preguntas: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM preguntas
                    WHERE id_preguntas = %s
                    RETURNING id_preguntas;
                """, (id_preguntas,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar pregunta: {e}")
            raise

        finally:
            if conn:
                conn.close()
