
from app.core.database import Database
from app.models.Respuesta import Respuesta


class RespuestaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.respuesta_id,
                    r.pregunta_id,
                    r.usuario_id,
                    r.puntaje,
                    r.comentario,
                    r.estado,
                    r.created_at,
                    r.updated_at,
                    CONCAT_WS(
                        ' ',
                        u.primer_nombre,
                        u.segundo_nombre,
                        u.primer_apellido,
                        u.segundo_apellido
                    ) AS nombre_evaluador,
                    u.correo,
                    p.texto_pregunta AS pregunta,
                    p.evaluacion_id,
                    e.titulo AS evaluacion,
                    e.tipo_evaluacion
                FROM respuestas r
                LEFT JOIN usuarios u
                    ON u.usuario_id = r.usuario_id
                LEFT JOIN preguntas p
                    ON p.pregunta_id = r.pregunta_id
                LEFT JOIN evaluaciones e
                    ON e.evaluacion_id = p.evaluacion_id
                ORDER BY r.respuesta_id ASC;
            """)

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener respuestas: {e}")
            return []

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, respuesta_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.respuesta_id,
                    r.pregunta_id,
                    r.usuario_id,
                    r.puntaje,
                    r.comentario,
                    r.estado,
                    r.created_at,
                    r.updated_at,
                    CONCAT_WS(
                        ' ',
                        u.primer_nombre,
                        u.segundo_nombre,
                        u.primer_apellido,
                        u.segundo_apellido
                    ) AS nombre_evaluador,
                    u.correo,
                    p.texto_pregunta AS pregunta,
                    p.evaluacion_id,
                    e.titulo AS evaluacion,
                    e.tipo_evaluacion
                FROM respuestas r
                LEFT JOIN usuarios u
                    ON u.usuario_id = r.usuario_id
                LEFT JOIN preguntas p
                    ON p.pregunta_id = r.pregunta_id
                LEFT JOIN evaluaciones e
                    ON e.evaluacion_id = p.evaluacion_id
                WHERE r.respuesta_id = %s;
            """, (respuesta_id,))

            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener respuesta: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def crear(self, respuesta: Respuesta):
        conn = None

        try:
            if not respuesta.usuario_id:
                raise ValueError(
                    "Se necesita el usuario que realiza la evaluación."
                )

            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO respuestas (
                    pregunta_id,
                    usuario_id,
                    puntaje,
                    comentario,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING respuesta_id;
            """, (
                respuesta.pregunta_id,
                respuesta.usuario_id,
                respuesta.puntaje,
                respuesta.comentario,
                respuesta.estado
            ))

            resultado = cursor.fetchone()
            nuevo_id = resultado["respuesta_id"]

            conn.commit()
            return nuevo_id

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear respuesta: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def crear_lote(
        self,
        respuestas: list[Respuesta],
        usuario_id: int,
        comentario: str | None = None
    ):
        conn = None

        try:
            if not usuario_id or usuario_id <= 0:
                raise ValueError("El usuario evaluador no es válido.")

            if len(respuestas) != 5:
                raise ValueError(
                    "La evaluación debe contener exactamente 5 respuestas."
                )

            pregunta_ids = [r.pregunta_id for r in respuestas]

            if len(set(pregunta_ids)) != 5:
                raise ValueError(
                    "Las cinco respuestas deben corresponder "
                    "a preguntas diferentes."
                )

            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Verificar que el usuario exista.
            cursor.execute("""
                SELECT usuario_id
                FROM usuarios
                WHERE usuario_id = %s
                  AND estado = TRUE;
            """, (usuario_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    "El usuario no existe o está inactivo."
                )

            # Verificar que las cinco preguntas existan y estén activas.
            cursor.execute("""
                SELECT pregunta_id
                FROM preguntas
                WHERE pregunta_id = ANY(%s)
                  AND estado = TRUE;
            """, (pregunta_ids,))

            preguntas_validas = {
                fila["pregunta_id"]
                for fila in cursor.fetchall()
            }

            if preguntas_validas != set(pregunta_ids):
                raise ValueError(
                    "Una o más preguntas no existen o están inactivas."
                )

            ids_creados = []

            for indice, respuesta in enumerate(respuestas):
                # Guardar el comentario general una sola vez.
                comentario_respuesta = (
                    comentario.strip()[:500]
                    if indice == 0
                    and comentario
                    and comentario.strip()
                    else None
                )

                cursor.execute("""
                    INSERT INTO respuestas (
                        pregunta_id,
                        usuario_id,
                        puntaje,
                        comentario,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING respuesta_id;
                """, (
                    respuesta.pregunta_id,
                    usuario_id,
                    respuesta.puntaje,
                    comentario_respuesta,
                    respuesta.estado
                ))

                resultado = cursor.fetchone()
                ids_creados.append(resultado["respuesta_id"])

            # Confirmar las cinco respuestas en una transacción.
            conn.commit()

            return ids_creados

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear respuestas por lote: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, respuesta_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM respuestas
                WHERE respuesta_id = %s
                RETURNING respuesta_id;
            """, (respuesta_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            return eliminado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar respuesta: {e}")
            return False

        finally:
            if conn:
                conn.close()

    def actualizar(self, respuesta_id: int, respuesta: Respuesta):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE respuestas
                SET pregunta_id = %s,
                    usuario_id = %s,
                    puntaje = %s,
                    comentario = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE respuesta_id = %s
                RETURNING respuesta_id;
            """, (
                respuesta.pregunta_id,
                respuesta.usuario_id,
                respuesta.puntaje,
                respuesta.comentario,
                respuesta.estado,
                respuesta_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar respuesta: {e}")
            return False

        finally:
            if conn:
                conn.close()
