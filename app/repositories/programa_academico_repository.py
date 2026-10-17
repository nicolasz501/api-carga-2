
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.ProgramaAcademico import ProgramaAcademico


class ProgramaAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_programas_academicos,
                        id_facultades,
                        nombre_programas,
                        estado,
                        created_at,
                        updated_at
                    FROM programas_academicos
                    ORDER BY id_programas_academicos ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar programas académicos: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_programas_academicos: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_programas_academicos,
                        id_facultades,
                        nombre_programas,
                        estado,
                        created_at,
                        updated_at
                    FROM programas_academicos
                    WHERE id_programas_academicos = %s;
                """, (id_programas_academicos,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar programa académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, programa: ProgramaAcademico):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO programas_academicos (
                        id_facultades,
                        nombre_programas,
                        estado
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id_programas_academicos;
                """, (
                    programa.id_facultades,
                    programa.nombre_programas,
                    programa.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_programas_academicos"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear programa académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(
        self,
        id_programas_academicos: int,
        programa: ProgramaAcademico
    ):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE programas_academicos
                    SET
                        id_facultades = %s,
                        nombre_programas = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_programas_academicos = %s
                    RETURNING id_programas_academicos;
                """, (
                    programa.id_facultades,
                    programa.nombre_programas,
                    programa.estado,
                    id_programas_academicos
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar programa académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_programas_academicos: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM programas_academicos
                    WHERE id_programas_academicos = %s
                    RETURNING id_programas_academicos;
                """, (id_programas_academicos,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar programa académico: {e}")
            raise

        finally:
            if conn:
                conn.close()
