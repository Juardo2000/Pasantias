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

def guardar_lead_db(nombre, correo, empresa, perfil):
    """[CREATE] Inserta el nuevo lead enriquecido en la tabla de PostgreSQL."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = """
            INSERT INTO leads (nombre, correo, empresa, perfil_enriquecido) 
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (nombre, correo, empresa, perfil))
        conn.commit()
        cursor.close()
        conn.close()
        print("💾 ¡Lead guardado exitosamente en la base de datos de Aiven!")
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")

def obtener_leads_db():
    """[READ] Recupera todos los leads guardados incluyendo su fecha de registro."""
    leads_dict = {}
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo, empresa, perfil_enriquecido, fecha_creacion FROM leads ORDER BY id ASC;")
        rows = cursor.fetchall()
        
        for indice, row in enumerate(rows, start=1):
            leads_dict[str(indice)] = {
                "id_db": row[0],
                "nombre": row[1],
                "correo": row[2],
                "empresa": row[3],
                "perfil": row[4],
                "fecha": row[5]
            }
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")
    return leads_dict

def eliminar_lead_db(id_db):
    """[DELETE] Elimina un lead específico de la base de datos usando su ID real de PostgreSQL."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "DELETE FROM leads WHERE id = %s;"
        cursor.execute(query, (id_db,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"🗑️ ¡Lead con ID {id_db} eliminado permanentemente de Aiven!")
        return True
    except Exception as e:
        print(f"❌ Error al eliminar el registro: {e}")
        return False