from app.core.database import Database
from app.models.Horario import Horario


class HorarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM horarios
                ORDER BY horario_id ASC;
            """)

            horarios = cursor.fetchall()
            conn.close()

            return horarios

        except Exception as e:
            print(f"Error al obtener horarios: {e}")
            return []

    def obtener_por_id(self, horario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM horarios
                WHERE horario_id = %s;
            """, (horario_id,))

            horario = cursor.fetchone()
            conn.close()

            return horario

        except Exception as e:
            print(f"Error al obtener horario: {e}")
            return None

    def crear(self, horario: Horario):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO horarios
                (
                    carga_id,
                    dia_laborales,
                    hora_inicio,
                    hora_finalizar,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING horario_id;
            """, (
                horario.carga_id,
                horario.dia_laborales,
                horario.hora_inicio,
                horario.hora_finalizar,
                horario.estado
            ))

            nuevo_id = cursor.fetchone()["horario_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear horario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, horario_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM horarios
                WHERE horario_id = %s
                RETURNING horario_id;
            """, (horario_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar horario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, horario_id: int, horario: Horario):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE horarios
                SET carga_id = %s,
                    dia_laborales = %s,
                    hora_inicio = %s,
                    hora_finalizar = %s,
                    estado = %s
                WHERE horario_id = %s
                RETURNING horario_id;
            """, (
                horario.carga_id,
                horario.dia_laborales,
                horario.hora_inicio,
                horario.hora_finalizar,
                horario.estado,
                horario_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar horario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False