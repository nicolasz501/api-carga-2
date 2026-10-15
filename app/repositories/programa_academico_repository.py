from app.core.database import Database
from app.models.ProgramaAcademico import ProgramaAcademico


class ProgramaAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM programas_academicos
                ORDER BY programa_id ASC;
            """)

            programas = cursor.fetchall()
            conn.close()

            return programas

        except Exception as e:
            print(f"Error al obtener programas: {e}")
            return []

    def obtener_por_id(self, programa_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM programas_academicos
                WHERE programa_id = %s;
            """, (programa_id,))

            programa = cursor.fetchone()
            conn.close()

            return programa

        except Exception as e:
            print(f"Error al obtener programa: {e}")
            return None

    def crear(self, programa: ProgramaAcademico):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO programas_academicos
                (
                    facultades_id,
                    nombre_programa,
                    estado
                )
                VALUES (%s, %s, %s)
                RETURNING programa_id;
            """, (
                programa.facultades_id,
                programa.nombre_programa,
                programa.estado
            ))

            nuevo_id = cursor.fetchone()["programa_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear programa: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, programa_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM programas_academicos
                WHERE programa_id = %s
                RETURNING programa_id;
            """, (programa_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar programa: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, programa_id: int, programa: ProgramaAcademico):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE programas_academicos
                SET facultades_id = %s,
                    nombre_programa = %s,
                    estado = %s
                WHERE programa_id = %s
                RETURNING programa_id;
            """, (
                programa.facultades_id,
                programa.nombre_programa,
                programa.estado,
                programa_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar programa: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False