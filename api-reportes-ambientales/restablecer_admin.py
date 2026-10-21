
import os
import bcrypt
import psycopg2
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()


def main():
    correo = "admin@mallorquin.com"

    nueva_contrasena = getpass("Escribe la nueva contraseña: ")
    confirmar = getpass("Confirma la nueva contraseña: ")

    if not nueva_contrasena:
        print("Error: la contraseña no puede estar vacía.")
        return

    if nueva_contrasena != confirmar:
        print("Error: las contraseñas no coinciden.")
        return

    if len(nueva_contrasena) < 5:
        print("Usa una contraseña de al menos 5 caracteres.")
        return

    # Generar el hash bcrypt.
    hash_contrasena = bcrypt.hashpw(
        nueva_contrasena.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("Error: no se encontró DATABASE_URL en el archivo .env.")
        return

    try:
        with psycopg2.connect(database_url) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET contrasena_hash = %s,
                        fecha_actualizacion = NOW()
                    WHERE LOWER(TRIM(correo)) = LOWER(TRIM(%s))
                    RETURNING usuario_id, correo, estado
                    """,
                    (hash_contrasena, correo)
                )

                usuario = cursor.fetchone()

                if usuario is None:
                    print("No existe el administrador con ese correo.")
                    return

                if not usuario[2]:
                    print("La contraseña se actualizó, pero el usuario está inactivo.")

                print("Contraseña restablecida correctamente.")
                print(f"Usuario ID: {usuario[0]}")
                print(f"Correo: {usuario[1]}")
                print(f"Activo: {usuario[2]}")

    except Exception as error:
        print(f"No se pudo restablecer la contraseña: {error}")


if __name__ == "__main__":
    main()
