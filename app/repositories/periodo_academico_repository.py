
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.PeriodoAcademico import PeriodoAcademico


class PeriodoAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_periodos_academicos,
                        codigo_periodo,
                        fecha_inicio,
                        fecha_finalizar,
                        estado,
                        created_at,
                        updated_at
                    FROM periodos_academicos
                    ORDER BY id_periodos_academicos ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al obtener períodos académicos: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_periodos_academicos: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_periodos_academicos,
                        codigo_periodo,
                        fecha_inicio,
                        fecha_finalizar,
                        estado,
                        created_at,
                        updated_at
                    FROM periodos_academicos
                    WHERE id_periodos_academicos = %s;
                """, (id_periodos_academicos,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al obtener período académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, periodo: PeriodoAcademico):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO periodos_academicos (
                        codigo_periodo,
                        fecha_inicio,
                        fecha_finalizar,
                        estado
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_periodos_academicos;
                """, (
                    periodo.codigo_periodo,
                    periodo.fecha_inicio,
                    periodo.fecha_finalizar,
                    periodo.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_periodos_academicos"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear período académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(
        self,
        id_periodos_academicos: int,
        periodo: PeriodoAcademico
    ):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE periodos_academicos
                    SET
                        codigo_periodo = %s,
                        fecha_inicio = %s,
                        fecha_finalizar = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_periodos_academicos = %s
                    RETURNING id_periodos_academicos;
                """, (
                    periodo.codigo_periodo,
                    periodo.fecha_inicio,
                    periodo.fecha_finalizar,
                    periodo.estado,
                    id_periodos_academicos
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar período académico: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_periodos_academicos: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM periodos_academicos
                    WHERE id_periodos_academicos = %s
                    RETURNING id_periodos_academicos;
                """, (id_periodos_academicos,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar período académico: {e}")
            raise

        finally:
            if conn:
                conn.close()
