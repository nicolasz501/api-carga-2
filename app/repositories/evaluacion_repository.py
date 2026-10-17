
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Evaluacion import Evaluacion


class EvaluacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_evaluaciones,
                        id_carga,
                        tipo_evaluacion,
                        titulo,
                        fecha_envio,
                        estado,
                        created_at,
                        updated_at
                    FROM evaluaciones
                    ORDER BY id_evaluaciones ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar evaluaciones: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_evaluaciones: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_evaluaciones,
                        id_carga,
                        tipo_evaluacion,
                        titulo,
                        fecha_envio,
                        estado,
                        created_at,
                        updated_at
                    FROM evaluaciones
                    WHERE id_evaluaciones = %s;
                """, (id_evaluaciones,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar evaluación: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, evaluacion: Evaluacion):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO evaluaciones (
                        id_carga,
                        tipo_evaluacion,
                        titulo,
                        fecha_envio,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_evaluaciones;
                """, (
                    evaluacion.id_carga,
                    evaluacion.tipo_evaluacion,
                    evaluacion.titulo,
                    evaluacion.fecha_envio,
                    evaluacion.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_evaluaciones"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear evaluación: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(
        self,
        id_evaluaciones: int,
        evaluacion: Evaluacion
    ):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE evaluaciones
                    SET
                        id_carga = %s,
                        tipo_evaluacion = %s,
                        titulo = %s,
                        fecha_envio = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_evaluaciones = %s
                    RETURNING id_evaluaciones;
                """, (
                    evaluacion.id_carga,
                    evaluacion.tipo_evaluacion,
                    evaluacion.titulo,
                    evaluacion.fecha_envio,
                    evaluacion.estado,
                    id_evaluaciones
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar evaluación: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_evaluaciones: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM evaluaciones
                    WHERE id_evaluaciones = %s
                    RETURNING id_evaluaciones;
                """, (id_evaluaciones,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar evaluación: {e}")
            raise

        finally:
            if conn:
                conn.close()
