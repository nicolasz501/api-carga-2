
from app.core.database import Database
from app.models.Usuario import Usuario

import bcrypt
import psycopg2
from psycopg2.errors import UniqueViolation, ForeignKeyViolation


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_usuario,
                        id_rol,
                        primer_nombre,
                        segundo_nombre,
                        primer_apellido,
                        segundo_apellido,
                        correo,
                        numero_documento,
                        estado,
                        created_at,
                        updated_at
                    FROM usuarios
                    ORDER BY id_usuario ASC;
                """)
                return cursor.fetchall()

        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, usuario_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id_usuario,
                        id_rol,
                        primer_nombre,
                        segundo_nombre,
                        primer_apellido,
                        segundo_apellido,
                        correo,
                        numero_documento,
                        estado,
                        created_at,
                        updated_at
                    FROM usuarios
                    WHERE id_usuario = %s;
                """, (usuario_id,))

                return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, usuario: Usuario):
        conn = None
        try:
            conn = self.db.get_connection()

            password_hash = bcrypt.hashpw(
                usuario.contrasena.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (
                        id_rol,
                        primer_nombre,
                        segundo_nombre,
                        primer_apellido,
                        segundo_apellido,
                        correo,
                        contrasena,
                        numero_documento,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_usuario;
                """, (
                    usuario.id_rol,
                    usuario.primer_nombre,
                    usuario.segundo_nombre,
                    usuario.primer_apellido,
                    usuario.segundo_apellido,
                    usuario.correo,
                    password_hash,
                    usuario.numero_documento,
                    usuario.estado
                ))

                nuevo = cursor.fetchone()
                conn.commit()
                return nuevo["id_usuario"]

        except UniqueViolation:
            if conn:
                conn.rollback()
            raise ValueError(
                "Ya existe un usuario con ese correo o número de documento"
            )

        except ForeignKeyViolation:
            if conn:
                conn.rollback()
            raise ValueError("El rol seleccionado no existe")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al crear usuario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def login(self, correo: str, password: str):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        u.id_usuario,
                        u.id_rol,
                        u.primer_nombre,
                        u.segundo_nombre,
                        u.primer_apellido,
                        u.segundo_apellido,
                        u.correo,
                        u.contrasena,
                        u.numero_documento,
                        u.estado,
                        r.id_roles,
                        r.nombre_rol
                    FROM usuarios AS u
                    INNER JOIN roles AS r
                        ON r.id_roles = u.id_rol
                    WHERE LOWER(u.correo) = LOWER(%s)
                      AND u.estado = TRUE
                      AND r.estado = TRUE;
                """, (correo,))

                usuario = cursor.fetchone()

                if not usuario:
                    return None

                hash_guardado = usuario["contrasena"]

                try:
                    password_valido = bcrypt.checkpw(
                        password.encode("utf-8"),
                        hash_guardado.encode("utf-8")
                    )
                except (ValueError, TypeError):
                    password_valido = False

                if not password_valido:
                    return None

                cursor.execute("""
                    SELECT
                        m.id_modulos,
                        m.nombre_modulos,
                        mr.puede_ver,
                        mr.puede_crear,
                        mr.puede_editar,
                        mr.puede_eliminar
                    FROM modulos_rol AS mr
                    INNER JOIN modulos AS m
                        ON m.id_modulos = mr.id_modulos
                    WHERE mr.id_rol = %s
                      AND m.estado = TRUE
                    ORDER BY m.id_modulos ASC;
                """, (usuario["id_rol"],))

                registros_modulos = cursor.fetchall()

                # Mantiene nombres de respuesta compatibles
                # con la estructura usada anteriormente en el frontend.
                lista_modulos = [
                    {
                        "id": m["id_modulos"],
                        "nombre": m["nombre_modulos"],
                        "puede_ver": m["puede_ver"],
                        "puede_crear": m["puede_crear"],
                        "puede_editar": m["puede_editar"],
                        "puede_eliminar": m["puede_eliminar"]
                    }
                    for m in registros_modulos
                ]

                return {
                    "usuario": {
                        "usuario_id": usuario["id_usuario"],
                        "rol_id": usuario["id_rol"],
                        "primer_nombre": usuario["primer_nombre"],
                        "segundo_nombre": usuario["segundo_nombre"],
                        "primer_apellido": usuario["primer_apellido"],
                        "segundo_apellido": usuario["segundo_apellido"],
                        "correo": usuario["correo"],
                        "numero_documento": usuario["numero_documento"],
                        "estado": usuario["estado"]
                    },
                    "rol": {
                        "rol_id": usuario["id_roles"],
                        "nombre": usuario["nombre_rol"]
                    },
                    "modulos": lista_modulos
                }

        except Exception as e:
            print(f"Error en login: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(self, usuario_id: int, usuario):
        conn = None
        try:
            conn = self.db.get_connection()

            password_hash = None

            if usuario.contrasena and usuario.contrasena.strip():
                password_hash = bcrypt.hashpw(
                    usuario.contrasena.strip().encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios
                    SET
                        id_rol = %s,
                        primer_nombre = %s,
                        segundo_nombre = %s,
                        primer_apellido = %s,
                        segundo_apellido = %s,
                        correo = %s,
                        contrasena = COALESCE(%s, contrasena),
                        numero_documento = %s,
                        estado = %s,
                        updated_at = NOW()
                    WHERE id_usuario = %s
                    RETURNING id_usuario;
                """, (
                    usuario.id_rol,
                    usuario.primer_nombre,
                    usuario.segundo_nombre,
                    usuario.primer_apellido,
                    usuario.segundo_apellido,
                    usuario.correo,
                    password_hash,
                    usuario.numero_documento,
                    usuario.estado,
                    usuario_id
                ))

                actualizado = cursor.fetchone()
                conn.commit()
                return actualizado is not None

        except UniqueViolation:
            if conn:
                conn.rollback()
            raise ValueError(
                "Ya existe otro usuario con ese correo o documento"
            )

        except ForeignKeyViolation:
            if conn:
                conn.rollback()
            raise ValueError("El rol seleccionado no existe")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar usuario: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, usuario_id: int):
        conn = None
        try:
            conn = self.db.get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM usuarios
                    WHERE id_usuario = %s
                    RETURNING id_usuario;
                """, (usuario_id,))

                eliminado = cursor.fetchone()
                conn.commit()
                return eliminado is not None

        except ForeignKeyViolation:
            if conn:
                conn.rollback()
            raise ValueError(
                "No se puede eliminar el usuario porque tiene registros asociados"
            )

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar usuario: {e}")
            raise

        finally:
            if conn:
                conn.close()
