
from app.core.database import Database
from app.models.Usuario import Usuario

import bcrypt
from psycopg2.errors import UniqueViolation, ForeignKeyViolation


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    # --------------------------------------------------
    # GENERAR HASH DE CONTRASEÑA
    # --------------------------------------------------
    @staticmethod
    def generar_hash(contrasena: str) -> str:
        if not contrasena or not contrasena.strip():
            raise ValueError("La contraseña no puede estar vacía")

        return bcrypt.hashpw(
            contrasena.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    # --------------------------------------------------
    # VERIFICAR CONTRASEÑA
    # --------------------------------------------------
    @staticmethod
    def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
        if not contrasena or not hash_guardado:
            return False

        try:
            return bcrypt.checkpw(
                contrasena.encode("utf-8"),
                hash_guardado.encode("utf-8")
            )
        except (ValueError, TypeError):
            return False

    # --------------------------------------------------
    # LISTAR USUARIOS
    # --------------------------------------------------
    def obtener_todos(self):
        conn = self.db.get_connection()

        try:
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

        finally:
            conn.close()

    # --------------------------------------------------
    # OBTENER USUARIO POR ID
    # --------------------------------------------------
    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()

        try:
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

        finally:
            conn.close()

    # --------------------------------------------------
    # CREAR USUARIO: GUARDA LA CONTRASEÑA CON BCRYPT
    # --------------------------------------------------
    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()

        try:
            password_hash = self.generar_hash(usuario.contrasena)

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
            conn.rollback()
            raise ValueError(
                "Ya existe un usuario con ese correo o número de documento"
            )

        except ForeignKeyViolation:
            conn.rollback()
            raise ValueError("El rol seleccionado no existe")

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    # --------------------------------------------------
    # INICIAR SESIÓN: VERIFICA BCRYPT
    # --------------------------------------------------
    def login(self, correo: str, password: str):
        conn = self.db.get_connection()

        try:
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

                if not self.verificar_contrasena(
                    password,
                    usuario["contrasena"]
                ):
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

                lista_modulos = [
                    {
                        "id": modulo["id_modulos"],
                        "nombre": modulo["nombre_modulos"],
                        "puede_ver": modulo["puede_ver"],
                        "puede_crear": modulo["puede_crear"],
                        "puede_editar": modulo["puede_editar"],
                        "puede_eliminar": modulo["puede_eliminar"]
                    }
                    for modulo in registros_modulos
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

        finally:
            conn.close()

    # --------------------------------------------------
    # ACTUALIZAR USUARIO
    # Si envía una contraseña nueva, genera un hash.
    # Si no la envía, conserva el hash actual.
    # --------------------------------------------------
    def actualizar(self, usuario_id: int, usuario):
        conn = self.db.get_connection()

        try:
            password_hash = None
            contrasena_nueva = getattr(usuario, "contrasena", None)

            if contrasena_nueva is not None:
                if contrasena_nueva.strip():
                    password_hash = self.generar_hash(contrasena_nueva)
                else:
                    password_hash = None

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
            conn.rollback()
            raise ValueError(
                "Ya existe otro usuario con ese correo o documento"
            )

        except ForeignKeyViolation:
            conn.rollback()
            raise ValueError("El rol seleccionado no existe")

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    # --------------------------------------------------
    # ELIMINAR USUARIO
    # --------------------------------------------------
    def eliminar(self, usuario_id: int):
        conn = self.db.get_connection()

        try:
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
            conn.rollback()
            raise ValueError(
                "No se puede eliminar el usuario porque tiene registros asociados"
            )

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
