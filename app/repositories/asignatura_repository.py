from app.core.database import Database
from app.models.Asignatura import Asignatura


class AsignaturaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM asignaturas ORDER BY asignatura_id ASC;")

            asignaturas = cursor.fetchall()
            conn.close()

            return asignaturas

        except Exception as e:
            print(f"Error al obtener asignaturas: {e}")
            return []

    def obtener_por_id(self, asignatura_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM asignaturas WHERE asignatura_id = %s;", (asignatura_id,))

            asignatura = cursor.fetchone()
            conn.close()

            return asignatura

        except Exception as e:
            print(f"Error al obtener asignatura: {e}")
            return None

    def crear(self, asignatura: Asignatura):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO asignaturas
                (
                    programa_id,
                    codigo_asignatura,
                    nombres_asignaturas,
                    creditos,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING asignatura_id;
            """, (
                asignatura.programa_id,
                asignatura.codigo_asignatura,
                asignatura.nombres_asignaturas,
                asignatura.creditos,
                asignatura.estado
            ))

            nuevo_id = cursor.fetchone()["asignatura_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear asignatura: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, asignatura_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM asignaturas
                WHERE asignatura_id = %s
                RETURNING asignatura_id;
            """, (asignatura_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar asignatura: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, asignatura_id: int, asignatura: Asignatura):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE asignaturas
                SET programa_id = %s,
                    codigo_asignatura = %s,
                    nombres_asignaturas = %s,
                    creditos = %s,
                    estado = %s
                WHERE asignatura_id = %s
                RETURNING asignatura_id;
            """, (
                asignatura.programa_id,
                asignatura.codigo_asignatura,
                asignatura.nombres_asignaturas,
                asignatura.creditos,
                asignatura.estado,
                asignatura_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar asignatura: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False