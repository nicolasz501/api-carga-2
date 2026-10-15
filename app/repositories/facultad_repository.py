from app.core.database import Database
from app.models.Facultad import Facultad


class FacultadRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM facultades
                ORDER BY facultades_id ASC;
            """)

            facultades = cursor.fetchall()
            conn.close()

            return facultades

        except Exception as e:
            print(f"Error al obtener facultades: {e}")
            return []

    def obtener_por_id(self, facultades_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM facultades
                WHERE facultades_id = %s;
            """, (facultades_id,))

            facultad = cursor.fetchone()
            conn.close()

            return facultad

        except Exception as e:
            print(f"Error al obtener facultad: {e}")
            return None

    def crear(self, facultad: Facultad):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO facultades
                (nombre_facultades, estado)
                VALUES (%s, %s)
                RETURNING facultades_id;
            """, (
                facultad.nombre_facultades,
                facultad.estado
            ))

            nuevo_id = cursor.fetchone()["facultades_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear facultad: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, facultades_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM facultades
                WHERE facultades_id = %s
                RETURNING facultades_id;
            """, (facultades_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar facultad: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, facultades_id: int, facultad: Facultad):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE facultades
                SET nombre_facultades = %s,
                    estado = %s
                WHERE facultades_id = %s
                RETURNING facultades_id;
            """, (
                facultad.nombre_facultades,
                facultad.estado,
                facultades_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar facultad: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False