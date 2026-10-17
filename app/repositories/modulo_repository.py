
from app.core.database import Database
from app.models.Modulo import Modulo

from psycopg2.errors import ForeignKeyViolation


class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_modulos,
                        nombre_modulos,
                        estado,
                        created_at,
                        updated_at
                    FROM modulos
                    ORDER BY id_modulos ASC;
                """)

                return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener módulos: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, modulos_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_modulos,
                        nombre_modulos,
                        estado,
                        created_at,
                        updated_at
                    FROM modulos
                    WHERE id_modulos = %s;
                """, (modulos_id,))

                return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener módulo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, modulo: Modulo):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO modulos (
                        nombre_modulos,
                        estado
                    )
                    VALUES (%s, %s)
                    RETURNING id_modulos;
                """, (
                    modulo.nombre_modulos,
                    modulo.estado
                ))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado["id_modulos"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear módulo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, modulos_id: int, modulo: Modulo):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE modulos
                    SET
                        nombre_modulos = %s,
                        estado = %s,
                        updated_at = NOW()
                    WHERE id_modulos = %s
                    RETURNING id_modulos;
                """, (
                    modulo.nombre_modulos,
                    modulo.estado,
                    modulos_id
                ))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar módulo: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, modulos_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM modulos
                    WHERE id_modulos = %s
                    RETURNING id_modulos;
                """, (modulos_id,))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado is not None

        except ForeignKeyViolation:
            if conn:
                conn.rollback()

            raise ValueError(
                "No se puede eliminar el módulo porque tiene "
                "permisos asociados en modulos_rol."
            )

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar módulo: {e}")
            raise

        finally:
            if conn:
                conn.close()
