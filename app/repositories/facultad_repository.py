
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Facultad import Facultad


class FacultadRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_facultades,
                        nombre_facultades,
                        estado,
                        created_at,
                        updated_at
                    FROM facultades
                    ORDER BY id_facultades ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar facultades: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_facultades: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_facultades,
                        nombre_facultades,
                        estado,
                        created_at,
                        updated_at
                    FROM facultades
                    WHERE id_facultades = %s;
                """, (id_facultades,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar facultad: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, facultad: Facultad):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO facultades (
                        nombre_facultades,
                        estado
                    )
                    VALUES (%s, %s)
                    RETURNING id_facultades;
                """, (
                    facultad.nombre_facultades,
                    facultad.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_facultades"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear facultad: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_facultades: int, facultad: Facultad):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE facultades
                    SET
                        nombre_facultades = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_facultades = %s
                    RETURNING id_facultades;
                """, (
                    facultad.nombre_facultades,
                    facultad.estado,
                    id_facultades
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar facultad: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_facultades: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM facultades
                    WHERE id_facultades = %s
                    RETURNING id_facultades;
                """, (id_facultades,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar facultad: {e}")
            raise

        finally:
            if conn:
                conn.close()
