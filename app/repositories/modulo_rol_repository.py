
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.ModuloRol import ModuloRol


class ModuloRolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_modulos_rol,
                        id_rol,
                        id_modulos,
                        puede_ver,
                        puede_crear,
                        puede_editar,
                        puede_eliminar,
                        estado,
                        created_at,
                        updated_at
                    FROM modulos_rol
                    ORDER BY id_modulos_rol ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar módulos por rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_modulos_rol: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        id_modulos_rol,
                        id_rol,
                        id_modulos,
                        puede_ver,
                        puede_crear,
                        puede_editar,
                        puede_eliminar,
                        estado,
                        created_at,
                        updated_at
                    FROM modulos_rol
                    WHERE id_modulos_rol = %s;
                """, (id_modulos_rol,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar módulo por rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, modulo_rol: ModuloRol):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO modulos_rol (
                        id_rol,
                        id_modulos,
                        puede_ver,
                        puede_crear,
                        puede_editar,
                        puede_eliminar,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_modulos_rol;
                """, (
                    modulo_rol.id_rol,
                    modulo_rol.id_modulos,
                    modulo_rol.puede_ver,
                    modulo_rol.puede_crear,
                    modulo_rol.puede_editar,
                    modulo_rol.puede_eliminar,
                    modulo_rol.estado
                ))

                nuevo = cursor.fetchone()
                conn.commit()

                return nuevo["id_modulos_rol"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear módulo por rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_modulos_rol: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM modulos_rol
                    WHERE id_modulos_rol = %s
                    RETURNING id_modulos_rol;
                """, (id_modulos_rol,))

                eliminado = cursor.fetchone()
                conn.commit()

                return eliminado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar módulo por rol: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(
        self,
        id_modulos_rol: int,
        modulo_rol: ModuloRol
    ):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE modulos_rol
                    SET
                        id_rol = %s,
                        id_modulos = %s,
                        puede_ver = %s,
                        puede_crear = %s,
                        puede_editar = %s,
                        puede_eliminar = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_modulos_rol = %s
                    RETURNING id_modulos_rol;
                """, (
                    modulo_rol.id_rol,
                    modulo_rol.id_modulos,
                    modulo_rol.puede_ver,
                    modulo_rol.puede_crear,
                    modulo_rol.puede_editar,
                    modulo_rol.puede_eliminar,
                    modulo_rol.estado,
                    id_modulos_rol
                ))

                actualizado = cursor.fetchone()
                conn.commit()

                return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar módulo por rol: {e}")
            raise

        finally:
            if conn:
                conn.close()
