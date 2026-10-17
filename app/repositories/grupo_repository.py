
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Grupo import Grupo


class GrupoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_grupo,
                        id_asignatura,
                        nombre_grupos,
                        estado,
                        created_at,
                        updated_at
                    FROM grupo
                    ORDER BY id_grupo ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar grupos: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_grupo: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_grupo,
                        id_asignatura,
                        nombre_grupos,
                        estado,
                        created_at,
                        updated_at
                    FROM grupo
                    WHERE id_grupo = %s;
                """, (id_grupo,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar grupo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, grupo: Grupo):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO grupo (
                        id_asignatura,
                        nombre_grupos,
                        estado
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id_grupo;
                """, (
                    grupo.id_asignatura,
                    grupo.nombre_grupos,
                    grupo.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_grupo"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear grupo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_grupo: int, grupo: Grupo):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE grupo
                    SET
                        id_asignatura = %s,
                        nombre_grupos = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_grupo = %s
                    RETURNING id_grupo;
                """, (
                    grupo.id_asignatura,
                    grupo.nombre_grupos,
                    grupo.estado,
                    id_grupo
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar grupo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_grupo: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM grupo
                    WHERE id_grupo = %s
                    RETURNING id_grupo;
                """, (id_grupo,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar grupo: {e}")
            raise

        finally:
            if conn:
                conn.close()
