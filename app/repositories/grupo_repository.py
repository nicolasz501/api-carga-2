from app.core.database import Database
from app.models.Grupo import Grupo


class GrupoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM grupos
                ORDER BY grupos_id ASC;
            """)

            grupos = cursor.fetchall()
            conn.close()

            return grupos

        except Exception as e:
            print(f"Error al obtener grupos: {e}")
            return []

    def obtener_por_id(self, grupos_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM grupos
                WHERE grupos_id = %s;
            """, (grupos_id,))

            grupo = cursor.fetchone()
            conn.close()

            return grupo

        except Exception as e:
            print(f"Error al obtener grupo: {e}")
            return None

    def crear(self, grupo: Grupo):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO grupos
                (
                    asignaturas_id,
                    periodos_id,
                    nombre_grupos,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING grupos_id;
            """, (
                grupo.asignaturas_id,
                grupo.periodos_id,
                grupo.nombre_grupos,
                grupo.estado
            ))

            nuevo_id = cursor.fetchone()["grupos_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear grupo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, grupos_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM grupos
                WHERE grupos_id = %s
                RETURNING grupos_id;
            """, (grupos_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar grupo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, grupos_id: int, grupo: Grupo):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE grupos
                SET asignaturas_id = %s,
                    periodos_id = %s,
                    nombre_grupos = %s,
                    estado = %s
                WHERE grupos_id = %s
                RETURNING grupos_id;
            """, (
                grupo.asignaturas_id,
                grupo.periodos_id,
                grupo.nombre_grupos,
                grupo.estado,
                grupos_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar grupo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False