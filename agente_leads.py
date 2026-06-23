from google import genai
from google.genai import types
import datetime
# 🌟 Importamos la librería necesaria para PostgreSQL
import psycopg2 

# Autenticación con tu clave directa para la fase de Prototipo (PoC)
API_KEY = "API KEY AQUI"
client = genai.Client(api_key=API_KEY)

# ⚙️ CONFIGURACIÓN DE TU BASE DE DATOS EN AIVEN (POSTGRESQL)
DB_CONFIG = {
    "dbname": "defaultdb",
    "user": "avnadmin",
    "password": "AVNS_pj3KkVLaBNj-EQAwJVe",
    "host": "pasantias-proyectogrupo3.l.aivencloud.com",
    "port": "24529",
    "sslmode": "require"  # Obligatorio para conectar con el SSL de Aiven
}

def conectar_db():
    """Establece la conexión con PostgreSQL en Aiven."""
    return psycopg2.connect(**DB_CONFIG)

def enriquecer_lead(nombre, correo, empresa):
    print(f"\n🔍 Investigando fuentes públicas para el lead: {nombre} ({empresa})...")
    
    prompt = (
        f"Realiza una investigación profunda en internet sobre:\n"
        f"- Nombre: {nombre}\n"
        f"- Correo: {correo}\n"
        f"- Empresa: {empresa}"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Eres un agente de Inteligencia Comercial de alta precisión. Tu tarea es enriquecer "
                    "datos de leads usando únicamente información pública y legal disponible en internet.\n\n"
                    "Estructura el perfil final de la siguiente manera:\n"
                    "1. PERFIL DE LA PERSONA: Cargo actual, trayectoria, áreas de especialización y enlaces.\n"
                    "2. ÁNGULO DE CONEXIÓN: Sugiere una idea o gancho personalizado para contactar a esta persona."
                ),
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.3
            )
        )
        
        # 🌟 Eliminamos las líneas que generaban el timestamp y abrían el archivo .txt
        print(f"✅ ¡Análisis completado con éxito por Gemini!")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

def guardar_lead_db(nombre, correo, empresa, perfil):
    """Inserta el nuevo lead enriquecido en la tabla de PostgreSQL."""
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
    """Recupera todos los leads guardados y los mapea en un diccionario."""
    leads_dict = {}
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo, empresa, perfil_enriquecido FROM leads ORDER BY id ASC;")
        rows = cursor.fetchall()
        
        # Mapeamos usando el índice incremental (1, 2, 3...) como clave del diccionario de selección
        for indice, row in enumerate(rows, start=1):
            leads_dict[str(indice)] = {
                "id_db": row[0],
                "nombre": row[1],
                "correo": row[2],
                "empresa": row[3],
                "perfil": row[4]
            }
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")
    return leads_dict

# --------------------------------------------------------------------------
# INTERFAZ DE MENÚ DE USUARIO
# --------------------------------------------------------------------------

def menu_principal():
    while True:
        print("\n==================================================")
        print("   ⚙️ SISTEMA DE GESTIÓN DE LEADS CON IA")
        print("==================================================")
        print("1) Buscar e Investigar nuevo Lead")
        print("2) Ver Leads existentes (Base de Datos)")
        print("3) Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n--- BÚSQUEDA DE NUEVO LEAD ---")
            nombre_input = input("Nombre completo: ")
            correo_input = input("Correo electrónico: ")
            empresa_input = input("Nombre de la empresa: ")
            
            perfil_completo = enriquecer_lead(nombre_input, correo_input, empresa_input)
            
            # Verificamos si la respuesta no es un error
            if perfil_completo and not perfil_completo.startswith("[Error"):
                print("\n==================================================")
                print("💼 PERFIL DE COMPAÑÍA Y LEAD ENRIQUECIDO:")
                print("==================================================")
                print(perfil_completo)
                print("==================================================")
                
                # Permite decidir si guardar o seguir buscando sin almacenar
                guardar = input("\n¿Desea guardar este lead en la Base de Datos? (s/n): ").strip().lower()
                if guardar == 's':
                    guardar_lead_db(nombre_input, correo_input, empresa_input, perfil_completo)
                else:
                    print("⚠️ Lead no guardado. Volviendo al menú para seguir buscando...")
            else:
                print(perfil_completo)
                    
        elif opcion == "2":
            diccionario_leads = obtener_leads_db()
            
            if not diccionario_leads:
                print("\n📭 No hay leads registrados en la base de datos aún.")
                continue
                
            print("\n--- LEADS EXISTENTES EN EL SISTEMA ---")
            for indice, datos in diccionario_leads.items():
                print(f"{indice}) {datos['nombre']} — [{datos['empresa']}]")
            print("0) Volver al menú principal")
                
            seleccion = input("\nSeleccione el número del lead para ver el reporte: ").strip()
            
            if seleccion == "0":
                continue
            elif seleccion in diccionario_leads:
                lead_seleccionado = diccionario_leads[seleccion]
                print("\n==================================================")
                print(f"📋 REPORTE DE INTELIGENCIA COMERCIAL (ID HISTÓRICO: {lead_seleccionado['id_db']})")
                print("==================================================")
                print(f"👤 Nombre:  {lead_seleccionado['nombre']}")
                print(f"📧 Correo:  {lead_seleccionado['correo']}")
                print(f"🏢 Empresa: {lead_seleccionado['empresa']}")
                print("--------------------------------------------------")
                print("🔬 INVESTIGACIÓN RETENIDA EN POSTGRESQL:")
                print(lead_seleccionado['perfil'])
                print("==================================================")
                input("\nPresione Enter para continuar...")
            else:
                print("❌ Selección inválida.")
                
        elif opcion == "3":
            print("\n👋 Cerrando el sistema de Inteligencia Comercial. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()