from app.core.database import Database
from app.models.Usuario import Usuario


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuarios
                ORDER BY usuario_id ASC;
            """)

            usuarios = cursor.fetchall()
            conn.close()

            return usuarios

        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def obtener_por_id(self, usuario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuarios
                WHERE usuario_id = %s;
            """, (usuario_id,))

            usuario = cursor.fetchone()
            conn.close()

            return usuario

        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def crear(self, usuario: Usuario):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO usuarios
                (
                    facultades_id,
                    rol_id,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    correo,
                    contraseña,
                    numero_documento,
                    codigo_personal,
                    titulo_academico,
                    estado
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                RETURNING usuario_id;
            """, (
                usuario.facultades_id,
                usuario.rol_id,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.correo,
                usuario.contraseña,
                usuario.numero_documento,
                usuario.codigo_personal,
                usuario.titulo_academico,
                usuario.estado
            ))

            nuevo_id = cursor.fetchone()["usuario_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear usuario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, usuario_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM usuarios
                WHERE usuario_id = %s
                RETURNING usuario_id;
            """, (usuario_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar usuario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuarios
                SET facultades_id = %s,
                    rol_id = %s,
                    primer_nombre = %s,
                    segundo_nombre = %s,
                    primer_apellido = %s,
                    segundo_apellido = %s,
                    correo = %s,
                    contraseña = %s,
                    numero_documento = %s,
                    codigo_personal = %s,
                    titulo_academico = %s,
                    estado = %s
                WHERE usuario_id = %s
                RETURNING usuario_id;
            """, (
                usuario.facultades_id,
                usuario.rol_id,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.correo,
                usuario.contraseña,
                usuario.numero_documento,
                usuario.codigo_personal,
                usuario.titulo_academico,
                usuario.estado,
                usuario_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar usuario: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False