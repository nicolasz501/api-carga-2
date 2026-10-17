
from app.core.database import Database
from app.models.Rol import Rol

from psycopg2.errors import ForeignKeyViolation


class RolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_roles,
                        nombre_rol,
                        estado,
                        created_at,
                        updated_at
                    FROM roles
                    ORDER BY id_roles ASC;
                """)

                return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener roles: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, rol_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_roles,
                        nombre_rol,
                        estado,
                        created_at,
                        updated_at
                    FROM roles
                    WHERE id_roles = %s;
                """, (rol_id,))

                return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, rol: Rol):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO roles (nombre_rol, estado)
                    VALUES (%s, %s)
                    RETURNING id_roles;
                """, (
                    rol.nombre_rol,
                    rol.estado
                ))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado["id_roles"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, rol_id: int, rol: Rol):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE roles
                    SET
                        nombre_rol = %s,
                        estado = %s,
                        updated_at = NOW()
                    WHERE id_roles = %s
                    RETURNING id_roles;
                """, (
                    rol.nombre_rol,
                    rol.estado,
                    rol_id
                ))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, rol_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM roles
                    WHERE id_roles = %s
                    RETURNING id_roles;
                """, (rol_id,))

                resultado = cursor.fetchone()
                conn.commit()

                return resultado is not None

        except ForeignKeyViolation:
            if conn:
                conn.rollback()

            raise ValueError(
                "No se puede eliminar el rol porque tiene usuarios "
                "o permisos asociados."
            )

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar rol: {e}")
            raise

        finally:
            if conn:
                conn.close()
