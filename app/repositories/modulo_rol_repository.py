from app.core.database import Database
from app.models.ModuloRol import ModuloRol


class ModuloRolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos_rol
                ORDER BY modules_rol_id ASC;
            """)

            datos = cursor.fetchall()
            conn.close()

            return datos

        except Exception as e:
            print(f"Error al obtener módulos por rol: {e}")
            return []

    def obtener_por_id(self, modules_rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos_rol
                WHERE modules_rol_id = %s;
            """, (modules_rol_id,))

            dato = cursor.fetchone()
            conn.close()

            return dato

        except Exception as e:
            print(f"Error al obtener módulo por rol: {e}")
            return None

    def crear(self, modulo_rol: ModuloRol):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO modulos_rol
                (
                    role_id,
                    module_id,
                    puede_ver,
                    puede_crear,
                    puede_editar,
                    puede_eliminar,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING modules_rol_id;
            """, (
                modulo_rol.role_id,
                modulo_rol.module_id,
                modulo_rol.puede_ver,
                modulo_rol.puede_crear,
                modulo_rol.puede_editar,
                modulo_rol.puede_eliminar,
                modulo_rol.estado
            ))

            nuevo_id = cursor.fetchone()["modules_rol_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear módulo por rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, modules_rol_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulos_rol
                WHERE modules_rol_id = %s
                RETURNING modules_rol_id;
            """, (modules_rol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar módulo por rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, modules_rol_id: int, modulo_rol: ModuloRol):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE modulos_rol
                SET role_id = %s,
                    module_id = %s,
                    puede_ver = %s,
                    puede_crear = %s,
                    puede_editar = %s,
                    puede_eliminar = %s,
                    estado = %s
                WHERE modules_rol_id = %s
                RETURNING modules_rol_id;
            """, (
                modulo_rol.role_id,
                modulo_rol.module_id,
                modulo_rol.puede_ver,
                modulo_rol.puede_crear,
                modulo_rol.puede_editar,
                modulo_rol.puede_eliminar,
                modulo_rol.estado,
                modules_rol_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar módulo por rol: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False