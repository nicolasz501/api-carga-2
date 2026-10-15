from app.core.database import Database
from app.models.Modulo import Modulo


class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                ORDER BY modulos_id ASC;
            """)

            modulos = cursor.fetchall()
            conn.close()

            return modulos

        except Exception as e:
            print(f"Error al obtener módulos: {e}")
            return []

    def obtener_por_id(self, modulos_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                WHERE modulos_id = %s;
            """, (modulos_id,))

            modulo = cursor.fetchone()
            conn.close()

            return modulo

        except Exception as e:
            print(f"Error al obtener módulo: {e}")
            return None

    def crear(self, modulo: Modulo):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO modulos
                (nombre_modulo, estado)
                VALUES (%s, %s)
                RETURNING modulos_id;
            """, (
                modulo.nombre_modulo,
                modulo.estado
            ))

            nuevo_id = cursor.fetchone()["modulos_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear módulo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, modulos_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulos
                WHERE modulos_id = %s
                RETURNING modulos_id;
            """, (modulos_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar módulo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, modulos_id: int, modulo: Modulo):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE modulos
                SET nombre_modulo = %s,
                    estado = %s
                WHERE modulos_id = %s
                RETURNING modulos_id;
            """, (
                modulo.nombre_modulo,
                modulo.estado,
                modulos_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar módulo: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False