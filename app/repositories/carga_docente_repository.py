from app.core.database import Database
from app.models.CargaDocente import CargaDocente


class CargaDocenteRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM carga_docente
                ORDER BY carga_id ASC;
            """)

            cargas = cursor.fetchall()
            conn.close()

            return cargas

        except Exception as e:
            print(f"Error al obtener cargas docentes: {e}")
            return []

    def obtener_por_id(self, carga_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM carga_docente
                WHERE carga_id = %s;
            """, (carga_id,))

            carga = cursor.fetchone()
            conn.close()

            return carga

        except Exception as e:
            print(f"Error al obtener carga docente: {e}")
            return None

    def crear(self, carga: CargaDocente):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO carga_docente
                (
                    user_id,
                    periodo_id,
                    id_grupo,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING carga_id;
            """, (
                carga.user_id,
                carga.periodo_id,
                carga.id_grupo,
                carga.estado
            ))

            nuevo_id = cursor.fetchone()["carga_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear carga docente: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, carga_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM carga_docente
                WHERE carga_id = %s
                RETURNING carga_id;
            """, (carga_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar carga docente: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, carga_id: int, carga: CargaDocente):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE carga_docente
                SET user_id = %s,
                    periodo_id = %s,
                    id_grupo = %s,
                    estado = %s
                WHERE carga_id = %s
                RETURNING carga_id;
            """, (
                carga.user_id,
                carga.periodo_id,
                carga.id_grupo,
                carga.estado,
                carga_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar carga docente: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False