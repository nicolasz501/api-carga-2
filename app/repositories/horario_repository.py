
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Horario import Horario


class HorarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_horarios,
                        id_carga,
                        dia_laborales,
                        hora_iniciar,
                        hora_finalizar,
                        estado,
                        created_at,
                        updated_at
                    FROM horarios
                    ORDER BY id_horarios ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar horarios: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_horarios: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_horarios,
                        id_carga,
                        dia_laborales,
                        hora_iniciar,
                        hora_finalizar,
                        estado,
                        created_at,
                        updated_at
                    FROM horarios
                    WHERE id_horarios = %s;
                """, (id_horarios,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar horario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, horario: Horario):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO horarios (
                        id_carga,
                        dia_laborales,
                        hora_iniciar,
                        hora_finalizar,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_horarios;
                """, (
                    horario.id_carga,
                    horario.dia_laborales,
                    horario.hora_iniciar,
                    horario.hora_finalizar,
                    horario.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_horarios"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear horario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, id_horarios: int, horario: Horario):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE horarios
                    SET
                        id_carga = %s,
                        dia_laborales = %s,
                        hora_iniciar = %s,
                        hora_finalizar = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_horarios = %s
                    RETURNING id_horarios;
                """, (
                    horario.id_carga,
                    horario.dia_laborales,
                    horario.hora_iniciar,
                    horario.hora_finalizar,
                    horario.estado,
                    id_horarios
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar horario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_horarios: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM horarios
                    WHERE id_horarios = %s
                    RETURNING id_horarios;
                """, (id_horarios,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar horario: {e}")
            raise

        finally:
            if conn:
                conn.close()
