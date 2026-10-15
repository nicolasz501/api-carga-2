from app.core.database import Database
from app.models.PeriodoAcademico import PeriodoAcademico


class PeriodoAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM periodos_academicos
                ORDER BY periodo_id ASC;
            """)

            periodos = cursor.fetchall()
            conn.close()

            return periodos

        except Exception as e:
            print(f"Error al obtener períodos: {e}")
            return []

    def obtener_por_id(self, periodo_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM periodos_academicos
                WHERE periodo_id = %s;
            """, (periodo_id,))

            periodo = cursor.fetchone()
            conn.close()

            return periodo

        except Exception as e:
            print(f"Error al obtener período: {e}")
            return None

    def crear(self, periodo: PeriodoAcademico):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO periodos_academicos
                (
                    codigo_periodo,
                    fecha_inicio,
                    fecha_finalizar,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING periodo_id;
            """, (
                periodo.codigo_periodo,
                periodo.fecha_inicio,
                periodo.fecha_finalizar,
                periodo.estado
            ))

            nuevo_id = cursor.fetchone()["periodo_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear período: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, periodo_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM periodos_academicos
                WHERE periodo_id = %s
                RETURNING periodo_id;
            """, (periodo_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar período: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, periodo_id: int, periodo: PeriodoAcademico):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE periodos_academicos
                SET codigo_periodo = %s,
                    fecha_inicio = %s,
                    fecha_finalizar = %s,
                    estado = %s
                WHERE periodo_id = %s
                RETURNING periodo_id;
            """, (
                periodo.codigo_periodo,
                periodo.fecha_inicio,
                periodo.fecha_finalizar,
                periodo.estado,
                periodo_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar período: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False