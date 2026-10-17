
from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.Respuesta import Respuesta


class RespuestaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        r.id_respuestas,
                        r.id_pregunta_evaluacion,
                        r.id_usuario,
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
                        p.texto_preguntas AS pregunta,
                        pe.id_evaluacion,
                        e.titulo AS evaluacion,
                        e.tipo_evaluacion
                    FROM respuestas r
                    LEFT JOIN usuarios u
                        ON u.id_usuario = r.id_usuario
                    LEFT JOIN preguntas_evaluaciones pe
                        ON pe.id_pregunta_evaluacion =
                           r.id_pregunta_evaluacion
                    LEFT JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    LEFT JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    ORDER BY r.id_respuestas ASC;
                """)

                return [dict(fila) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"Error al listar respuestas: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_respuestas: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        r.id_respuestas,
                        r.id_pregunta_evaluacion,
                        r.id_usuario,
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
                        p.texto_preguntas AS pregunta,
                        pe.id_evaluacion,
                        e.titulo AS evaluacion,
                        e.tipo_evaluacion
                    FROM respuestas r
                    LEFT JOIN usuarios u
                        ON u.id_usuario = r.id_usuario
                    LEFT JOIN preguntas_evaluaciones pe
                        ON pe.id_pregunta_evaluacion =
                           r.id_pregunta_evaluacion
                    LEFT JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    LEFT JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE r.id_respuestas = %s;
                """, (id_respuestas,))

                fila = cursor.fetchone()
                return dict(fila) if fila else None

        except Exception as e:
            print(f"Error al consultar respuesta: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def crear(self, respuesta: Respuesta):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Comprobar que el usuario exista y esté activo.
                cursor.execute("""
                    SELECT id_usuario
                    FROM usuarios
                    WHERE id_usuario = %s
                      AND estado = TRUE;
                """, (respuesta.id_usuario,))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "El usuario no existe o está inactivo."
                    )

                # Comprobar que la pregunta de la evaluación exista
                # y que tanto la pregunta como la evaluación estén activas.
                cursor.execute("""
                    SELECT pe.id_pregunta_evaluacion
                    FROM preguntas_evaluaciones pe
                    JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE pe.id_pregunta_evaluacion = %s
                      AND pe.estado = TRUE
                      AND p.estado = TRUE
                      AND e.estado = TRUE;
                """, (respuesta.id_pregunta_evaluacion,))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "La pregunta de evaluación no existe o está inactiva."
                    )

                cursor.execute("""
                    INSERT INTO respuestas (
                        id_pregunta_evaluacion,
                        id_usuario,
                        puntaje,
                        comentario,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_respuestas;
                """, (
                    respuesta.id_pregunta_evaluacion,
                    respuesta.id_usuario,
                    respuesta.puntaje,
                    respuesta.comentario,
                    respuesta.estado
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila["id_respuestas"]

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al crear respuesta: {e}")
            raise

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
            if usuario_id <= 0:
                raise ValueError("El usuario evaluador no es válido.")

            if len(respuestas) != 5:
                raise ValueError(
                    "La evaluación debe contener exactamente 5 respuestas."
                )

            ids_preguntas_evaluacion = [
                r.id_pregunta_evaluacion for r in respuestas
            ]

            if len(set(ids_preguntas_evaluacion)) != 5:
                raise ValueError(
                    "Las cinco respuestas deben corresponder "
                    "a preguntas diferentes."
                )

            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Validar al usuario.
                cursor.execute("""
                    SELECT id_usuario
                    FROM usuarios
                    WHERE id_usuario = %s
                      AND estado = TRUE;
                """, (usuario_id,))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "El usuario no existe o está inactivo."
                    )

                # Validar las cinco preguntas y verificar que pertenezcan
                # a la misma evaluación.
                cursor.execute("""
                    SELECT
                        pe.id_pregunta_evaluacion,
                        pe.id_evaluacion
                    FROM preguntas_evaluaciones pe
                    JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE pe.id_pregunta_evaluacion = ANY(%s)
                      AND pe.estado = TRUE
                      AND p.estado = TRUE
                      AND e.estado = TRUE;
                """, (ids_preguntas_evaluacion,))

                filas = cursor.fetchall()

                if len(filas) != 5:
                    raise ValueError(
                        "Una o más preguntas no existen o están inactivas."
                    )

                evaluacion_ids = {
                    fila["id_evaluacion"] for fila in filas
                }

                if len(evaluacion_ids) != 1:
                    raise ValueError(
                        "Las cinco preguntas deben pertenecer "
                        "a la misma evaluación."
                    )

                ids_creados = []

                # Guardar las cinco respuestas en una sola transacción.
                # El comentario general se almacena una sola vez.
                comentario_general = (
                    comentario.strip()
                    if comentario and comentario.strip()
                    else None
                )

                for indice, respuesta in enumerate(respuestas):
                    comentario_respuesta = (
                        comentario_general if indice == 0 else None
                    )

                    cursor.execute("""
                        INSERT INTO respuestas (
                            id_pregunta_evaluacion,
                            id_usuario,
                            puntaje,
                            comentario,
                            estado
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id_respuestas;
                    """, (
                        respuesta.id_pregunta_evaluacion,
                        usuario_id,
                        respuesta.puntaje,
                        comentario_respuesta,
                        respuesta.estado
                    ))

                    fila = cursor.fetchone()
                    ids_creados.append(fila["id_respuestas"])

                conn.commit()
                return ids_creados

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al registrar respuestas por lote: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def actualizar(
        self,
        id_respuestas: int,
        respuesta: Respuesta
    ):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id_usuario
                    FROM usuarios
                    WHERE id_usuario = %s
                      AND estado = TRUE;
                """, (respuesta.id_usuario,))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "El usuario no existe o está inactivo."
                    )

                cursor.execute("""
                    SELECT pe.id_pregunta_evaluacion
                    FROM preguntas_evaluaciones pe
                    JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE pe.id_pregunta_evaluacion = %s
                      AND pe.estado = TRUE
                      AND p.estado = TRUE
                      AND e.estado = TRUE;
                """, (respuesta.id_pregunta_evaluacion,))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "La pregunta de evaluación no existe o está inactiva."
                    )

                cursor.execute("""
                    UPDATE respuestas
                    SET
                        id_pregunta_evaluacion = %s,
                        id_usuario = %s,
                        puntaje = %s,
                        comentario = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_respuestas = %s
                    RETURNING id_respuestas;
                """, (
                    respuesta.id_pregunta_evaluacion,
                    respuesta.id_usuario,
                    respuesta.puntaje,
                    respuesta.comentario,
                    respuesta.estado,
                    id_respuestas
                ))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al actualizar respuesta: {e}")
            raise

        finally:
            if conn:
                conn.close()

    def eliminar(self, id_respuestas: int):
        conn = None

        try:
            conn = self.db.get_connection()

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM respuestas
                    WHERE id_respuestas = %s
                    RETURNING id_respuestas;
                """, (id_respuestas,))

                fila = cursor.fetchone()
                conn.commit()

                return fila is not None

        except Exception as e:
            if conn:
                conn.rollback()

            print(f"Error al eliminar respuesta: {e}")
            raise

        finally:
            if conn:
                conn.close()
