
from psycopg2.extras import RealDictCursor

from app.core.database import Database


class PreguntaEvaluacionRepository:

    def obtener_todos(self):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        pe.id_pregunta_evaluacion,
                        pe.id_preguntas,
                        p.texto_preguntas,
                        pe.id_evaluacion,
                        e.titulo,
                        pe.numero_orden,
                        pe.estado,
                        pe.created_at,
                        pe.updated_at
                    FROM preguntas_evaluaciones pe
                    INNER JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    INNER JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    ORDER BY
                        pe.id_evaluacion,
                        pe.numero_orden,
                        pe.id_pregunta_evaluacion
                """)
                return cursor.fetchall()
        finally:
            conexion.close()

    def obtener_por_id(self, id_pregunta_evaluacion: int):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        pe.id_pregunta_evaluacion,
                        pe.id_preguntas,
                        p.texto_preguntas,
                        pe.id_evaluacion,
                        e.titulo,
                        pe.numero_orden,
                        pe.estado,
                        pe.created_at,
                        pe.updated_at
                    FROM preguntas_evaluaciones pe
                    INNER JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    INNER JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE pe.id_pregunta_evaluacion = %s
                """, (id_pregunta_evaluacion,))
                return cursor.fetchone()
        finally:
            conexion.close()

    def obtener_por_evaluacion(self, id_evaluacion: int):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT
                        pe.id_pregunta_evaluacion,
                        pe.id_preguntas,
                        p.texto_preguntas,
                        pe.id_evaluacion,
                        e.titulo,
                        pe.numero_orden,
                        pe.estado,
                        pe.created_at,
                        pe.updated_at
                    FROM preguntas_evaluaciones pe
                    INNER JOIN preguntas p
                        ON p.id_preguntas = pe.id_preguntas
                    INNER JOIN evaluaciones e
                        ON e.id_evaluaciones = pe.id_evaluacion
                    WHERE pe.id_evaluacion = %s
                    ORDER BY pe.numero_orden ASC
                """, (id_evaluacion,))
                return cursor.fetchall()
        finally:
            conexion.close()

    def crear(self, pregunta_evaluacion):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id_preguntas
                    FROM preguntas
                    WHERE id_preguntas = %s
                      AND estado = TRUE
                """, (pregunta_evaluacion.id_preguntas,))

                if not cursor.fetchone():
                    raise ValueError("La pregunta no existe o está inactiva.")

                cursor.execute("""
                    SELECT id_evaluaciones
                    FROM evaluaciones
                    WHERE id_evaluaciones = %s
                      AND estado = TRUE
                """, (pregunta_evaluacion.id_evaluacion,))

                if not cursor.fetchone():
                    raise ValueError("La evaluación no existe o está inactiva.")

                cursor.execute("""
                    SELECT id_pregunta_evaluacion
                    FROM preguntas_evaluaciones
                    WHERE id_preguntas = %s
                      AND id_evaluacion = %s
                """, (
                    pregunta_evaluacion.id_preguntas,
                    pregunta_evaluacion.id_evaluacion
                ))

                if cursor.fetchone():
                    raise ValueError(
                        "Esta pregunta ya está asociada a esa evaluación."
                    )

                cursor.execute("""
                    INSERT INTO preguntas_evaluaciones (
                        id_preguntas,
                        id_evaluacion,
                        numero_orden,
                        estado
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING
                        id_pregunta_evaluacion,
                        id_preguntas,
                        id_evaluacion,
                        numero_orden,
                        estado,
                        created_at,
                        updated_at
                """, (
                    pregunta_evaluacion.id_preguntas,
                    pregunta_evaluacion.id_evaluacion,
                    pregunta_evaluacion.numero_orden,
                    pregunta_evaluacion.estado
                ))

                resultado = cursor.fetchone()
                conexion.commit()
                return resultado

        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def actualizar(self, id_pregunta_evaluacion: int, pregunta_evaluacion):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id_pregunta_evaluacion
                    FROM preguntas_evaluaciones
                    WHERE id_pregunta_evaluacion = %s
                """, (id_pregunta_evaluacion,))

                if not cursor.fetchone():
                    return None

                cursor.execute("""
                    SELECT id_preguntas
                    FROM preguntas
                    WHERE id_preguntas = %s
                      AND estado = TRUE
                """, (pregunta_evaluacion.id_preguntas,))

                if not cursor.fetchone():
                    raise ValueError("La pregunta no existe o está inactiva.")

                cursor.execute("""
                    SELECT id_evaluaciones
                    FROM evaluaciones
                    WHERE id_evaluaciones = %s
                      AND estado = TRUE
                """, (pregunta_evaluacion.id_evaluacion,))

                if not cursor.fetchone():
                    raise ValueError("La evaluación no existe o está inactiva.")

                cursor.execute("""
                    SELECT id_pregunta_evaluacion
                    FROM preguntas_evaluaciones
                    WHERE id_preguntas = %s
                      AND id_evaluacion = %s
                      AND id_pregunta_evaluacion <> %s
                """, (
                    pregunta_evaluacion.id_preguntas,
                    pregunta_evaluacion.id_evaluacion,
                    id_pregunta_evaluacion
                ))

                if cursor.fetchone():
                    raise ValueError(
                        "Esta pregunta ya está asociada a esa evaluación."
                    )

                cursor.execute("""
                    UPDATE preguntas_evaluaciones
                    SET
                        id_preguntas = %s,
                        id_evaluacion = %s,
                        numero_orden = %s,
                        estado = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id_pregunta_evaluacion = %s
                    RETURNING
                        id_pregunta_evaluacion,
                        id_preguntas,
                        id_evaluacion,
                        numero_orden,
                        estado,
                        created_at,
                        updated_at
                """, (
                    pregunta_evaluacion.id_preguntas,
                    pregunta_evaluacion.id_evaluacion,
                    pregunta_evaluacion.numero_orden,
                    pregunta_evaluacion.estado,
                    id_pregunta_evaluacion
                ))

                resultado = cursor.fetchone()
                conexion.commit()
                return resultado

        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def eliminar(self, id_pregunta_evaluacion: int):
        conexion = Database().get_connection()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    DELETE FROM preguntas_evaluaciones
                    WHERE id_pregunta_evaluacion = %s
                    RETURNING id_pregunta_evaluacion
                """, (id_pregunta_evaluacion,))

                resultado = cursor.fetchone()
                conexion.commit()
                return resultado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
