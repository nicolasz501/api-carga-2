from app.core.database import Database
from app.models.PeriodoAcademico import PeriodoAcademico


class PeriodoAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    periodo_id,
                    codigo_periodo,
                    fecha_inicio,
                    fecha_finalizar,
                    estado,
                    created_at,
                    updated_at
                FROM periodos_academicos
                ORDER BY periodo_id ASC;
            """)

            periodos = cursor.fetchall()

            return periodos

        except Exception as e:
            print(f"Error al obtener períodos: {e}")
            return []

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, periodo_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    periodo_id,
                    codigo_periodo,
                    fecha_inicio,
                    fecha_finalizar,
                    estado,
                    created_at,
                    updated_at
                FROM periodos_academicos
                WHERE periodo_id = %s;
            """, (periodo_id,))

            periodo = cursor.fetchone()

            return periodo

        except Exception as e:
            print(f"Error al obtener período: {e}")
            return None

        finally:
            if conn:
                conn.close()


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

            resultado = cursor.fetchone()

            conn.commit()

            if resultado:
                return resultado["periodo_id"]

            return None

        except Exception as e:
            print(f"Error al crear período: {e}")

            if conn:
                conn.rollback()

            return None

        finally:
            if conn:
                conn.close()


    def actualizar(
        self,
        periodo_id: int,
        periodo: PeriodoAcademico
    ):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE periodos_academicos
                SET
                    codigo_periodo = %s,
                    fecha_inicio = %s,
                    fecha_finalizar = %s,
                    estado = %s,
                    updated_at = NOW()
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

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar período: {e}")

            if conn:
                conn.rollback()

            return False

        finally:
            if conn:
                conn.close()


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

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar período: {e}")

            if conn:
                conn.rollback()

            return False

        finally:
            if conn:
                conn.close()