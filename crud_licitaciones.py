import os
import psycopg2
from dotenv import load_dotenv

# Cargamos las variables de entorno del archivo .env
load_dotenv()

# ⚙️ CONFIGURACIÓN DE TU BASE DE DATOS EN AIVEN (POSTGRESQL)
DB_CONFIG = {
    "dbname": "defaultdb",
    "user": "avnadmin",
    "password": os.environ.get("DB_PASSWORD"),
    "host": "pasantias-proyectogrupo3.l.aivencloud.com",
    "port": "24529",
    "sslmode": "require"
}

def conectar_db():
    """Establece la conexión con PostgreSQL en Aiven."""
    return psycopg2.connect(**DB_CONFIG)

def guardar_licitacion_db(sector, pais, palabras_clave, resultado):
    """[CREATE] Inserta una nueva búsqueda de licitación en la base de datos."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = """
            INSERT INTO licitaciones (sector, pais, palabras_clave, resultado_busqueda) 
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (sector, pais, palabras_clave, resultado))
        conn.commit()
        cursor.close()
        conn.close()
        print("💾 ¡Resultados de licitación guardados exitosamente en Aiven!")
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")

def obtener_licitaciones_db():
    """[READ] Recupera todas las licitaciones registradas."""
    licitaciones_dict = {}
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, sector, pais, palabras_clave, resultado_busqueda, fecha_creacion FROM licitaciones ORDER BY id ASC;")
        rows = cursor.fetchall()
        
        for indice, row in enumerate(rows, start=1):
            licitaciones_dict[str(indice)] = {
                "id_db": row[0],
                "sector": row[1],
                "pais": row[2],
                "keywords": row[3],
                "resultado": row[4],
                "fecha": row[5]
            }
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")
    return licitaciones_dict

def eliminar_licitacion_db(id_db):
    """[DELETE] Elimina un reporte de licitaciones permanentemente."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "DELETE FROM licitaciones WHERE id = %s;"
        cursor.execute(query, (id_db,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"🗑️ ¡Registro de licitación con ID {id_db} eliminado de Aiven!")
        return True
    except Exception as e:
        print(f"❌ Error al eliminar el registro: {e}")
        return False