from app.core.database import Database
from app.models.Evaluacion import Evaluacion


class EvaluacionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM evaluaciones
                ORDER BY evaluacion_id ASC;
            """)

            evaluaciones = cursor.fetchall()
            conn.close()

            return evaluaciones

        except Exception as e:
            print(f"Error al obtener evaluaciones: {e}")
            return []

    def obtener_por_id(self, evaluacion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM evaluaciones
                WHERE evaluacion_id = %s;
            """, (evaluacion_id,))

            evaluacion = cursor.fetchone()
            conn.close()

            return evaluacion

        except Exception as e:
            print(f"Error al obtener evaluación: {e}")
            return None

    def crear(self, evaluacion: Evaluacion):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            if evaluacion.fecha_envio is None:

                cursor.execute("""
                    INSERT INTO evaluaciones
                    (
                        carga_id,
                        periodo_id,
                        tipo_evaluacion,
                        titulo,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING evaluacion_id;
                """, (
                    evaluacion.carga_id,
                    evaluacion.periodo_id,
                    evaluacion.tipo_evaluacion,
                    evaluacion.titulo,
                    evaluacion.estado
                ))

            else:

                cursor.execute("""
                    INSERT INTO evaluaciones
                    (
                        carga_id,
                        periodo_id,
                        tipo_evaluacion,
                        titulo,
                        fecha_envio,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING evaluacion_id;
                """, (
                    evaluacion.carga_id,
                    evaluacion.periodo_id,
                    evaluacion.tipo_evaluacion,
                    evaluacion.titulo,
                    evaluacion.fecha_envio,
                    evaluacion.estado
                ))

            nuevo_id = cursor.fetchone()["evaluacion_id"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error al crear evaluación: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return None

    def eliminar(self, evaluacion_id: int):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM evaluaciones
                WHERE evaluacion_id = %s
                RETURNING evaluacion_id;
            """, (evaluacion_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error al eliminar evaluación: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False

    def actualizar(self, evaluacion_id: int, evaluacion: Evaluacion):
        conn = None

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE evaluaciones
                SET carga_id = %s,
                    periodo_id = %s,
                    tipo_evaluacion = %s,
                    titulo = %s,
                    estado = %s
                WHERE evaluacion_id = %s
                RETURNING evaluacion_id;
            """, (
                evaluacion.carga_id,
                evaluacion.periodo_id,
                evaluacion.tipo_evaluacion,
                evaluacion.titulo,
                evaluacion.estado,
                evaluacion_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error al actualizar evaluación: {e}")

            if conn:
                conn.rollback()
                conn.close()

            return False