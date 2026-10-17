
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.CargaDocente import CargaDocente


class CargaDocenteRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_carga,
                        id_usuario,
                        id_periodo,
                        id_grupo,
                        estado,
                        created_at,
                        updated_at
                    FROM carga_docente
                    ORDER BY id_carga ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar cargas docentes: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_carga: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_carga,
                        id_usuario,
                        id_periodo,
                        id_grupo,
                        estado,
                        created_at,
                        updated_at
                    FROM carga_docente
                    WHERE id_carga = %s;
                """, (id_carga,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar carga docente: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, carga: CargaDocente):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO carga_docente (
                        id_usuario,
                        id_periodo,
                        id_grupo,
                        estado
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_carga;
                """, (
                    carga.id_usuario,
                    carga.id_periodo,
                    carga.id_grupo,
                    carga.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_carga"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear carga docente: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_carga: int, carga: CargaDocente):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE carga_docente
                    SET
                        id_usuario = %s,
                        id_periodo = %s,
                        id_grupo = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_carga = %s
                    RETURNING id_carga;
                """, (
                    carga.id_usuario,
                    carga.id_periodo,
                    carga.id_grupo,
                    carga.estado,
                    id_carga
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar carga docente: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_carga: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM carga_docente
                    WHERE id_carga = %s
                    RETURNING id_carga;
                """, (id_carga,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar carga docente: {e}")
            raise

        finally:
            if conn:
                conn.close()
