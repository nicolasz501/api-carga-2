import os 
import psycopg2 
from psycopg2.extras import RealDictCursor 
from dotenv import load_dotenv 

# Carga las variables de entorno desde el archivo .env al entorno de ejecución de Python
load_dotenv() 


class Database: 
    
    #Clase encargada de gestionar la configuración y apertura 
    #de conexiones con la base de datos PostgreSQL.
    

    def __init__(self): 
        # Carga las credenciales y parámetros de conexión leyendo las variables de entorno
        self.host = os.getenv("DB_HOST") 
        self.database = os.getenv("DB_NAME") 
        self.user = os.getenv("DB_USER") 
        self.password = os.getenv("DB_PASSWORD") 
        self.port = os.getenv("DB_PORT") 

    def get_connection(self): 
        
        #Establece y retorna una nueva conexión a PostgreSQL.
        #Configura los cursores para retornar los resultados como diccionarios.
        
        try: 
            # Abre la conexión a la base de datos utilizando los parámetros cargados
            return psycopg2.connect( 
                host=self.host, 
                database=self.database, 
                user=self.user, 
                password=self.password, 
                port=self.port, 
                # RealDictCursor hace que el cursor devuelva los registros como diccionarios
                # (clave: nombre_columna, valor: dato) en lugar de tuplas simples (valor, valor)
                cursor_factory=RealDictCursor 
            ) 
        except Exception as e: 
            # Captura cualquier falla de red, credenciales incorrectas o servidor caído
            print(f"Error de conexión a la BD: {e}") 
            return None