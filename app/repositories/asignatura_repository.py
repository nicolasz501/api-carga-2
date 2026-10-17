
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Asignatura import Asignatura


class AsignaturaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_asignatura,
                        id_programa,
                        codigo_asignatura,
                        nombre_asignatura,
                        creditos,
                        estado,
                        created_at,
                        updated_at
                    FROM asignatura
                    ORDER BY id_asignatura ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar asignaturas: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_asignatura: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_asignatura,
                        id_programa,
                        codigo_asignatura,
                        nombre_asignatura,
                        creditos,
                        estado,
                        created_at,
                        updated_at
                    FROM asignatura
                    WHERE id_asignatura = %s;
                """, (id_asignatura,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar asignatura: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, asignatura: Asignatura):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO asignatura (
                        id_programa,
                        codigo_asignatura,
                        nombre_asignatura,
                        creditos,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_asignatura;
                """, (
                    asignatura.id_programa,
                    asignatura.codigo_asignatura,
                    asignatura.nombre_asignatura,
                    asignatura.creditos,
                    asignatura.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_asignatura"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear asignatura: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_asignatura: int, asignatura: Asignatura):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE asignatura
                    SET
                        id_programa = %s,
                        codigo_asignatura = %s,
                        nombre_asignatura = %s,
                        creditos = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_asignatura = %s
                    RETURNING id_asignatura;
                """, (
                    asignatura.id_programa,
                    asignatura.codigo_asignatura,
                    asignatura.nombre_asignatura,
                    asignatura.creditos,
                    asignatura.estado,
                    id_asignatura
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar asignatura: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_asignatura: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM asignatura
                    WHERE id_asignatura = %s
                    RETURNING id_asignatura;
                """, (id_asignatura,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar asignatura: {e}")
            raise

        finally:
            if conn:
                conn.close()
