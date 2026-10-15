from app.core.database import Database
from app.models.Rol import Rol


class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM roles
                ORDER BY rol_id ASC;
            """)

            roles = cursor.fetchall()
            conn.close()

            return roles

        except Exception as e:
            print(f"Error al obtener roles: {e}")
            return []

    def obtener_por_id(self, rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM roles
                WHERE rol_id = %s;
            """, (rol_id,))

            rol = cursor.fetchone()
            conn.close()

            return rol

        except Exception as e:
            print(f"Error al obtener rol: {e}")
            return None

    def crear(self, rol: Rol):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO roles
                (nombre_rol, estado)
                VALUES (%s, %s)
                RETURNING rol_id;
            """, (
                rol.nombre_rol,
                rol.estado
            ))

            nuevo_id = cursor.fetchone()["rol_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, rol_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM roles
                WHERE rol_id = %s
                RETURNING rol_id;
            """, (rol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, rol_id: int, rol: Rol):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE roles
                SET nombre_rol = %s,
                    estado = %s
                WHERE rol_id = %s
                RETURNING rol_id;
            """, (
                rol.nombre_rol,
                rol.estado,
                rol_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False