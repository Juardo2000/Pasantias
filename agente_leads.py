import os
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 🌟 IMPORTAMOS EL NUEVO MÓDULO CRUD QUE CREASTE
import crud_leads

# Cargamos las variables de entorno del archivo .env
load_dotenv()

# Autenticación segura utilizando la variable de entorno
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

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
        
        print(f"✅ ¡Análisis completado con éxito por Gemini!")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

# --------------------------------------------------------------------------
# INTERFAZ DE MENÚ DE USUARIO
# --------------------------------------------------------------------------

def menu_principal():
    while True:
        print("\n==================================================")
        print("   ⚙️ SISTEMA DE GESTIÓN DE LEADS CON IA")
        print("==================================================")
        print("1) Buscar e Investigar nuevo Lead")
        print("2) Ver Leads existentes (Base de Datos / CRUD)")
        print("3) Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n--- BÚSQUEDA DE NUEVO LEAD ---")
            nombre_input = input("Nombre completo: ")
            correo_input = input("Correo electrónico: ")
            empresa_input = input("Nombre de la empresa: ")
            
            perfil_completo = enriquecer_lead(nombre_input, correo_input, empresa_input)
            
            if perfil_completo and not perfil_completo.startswith("[Error"):
                print("\n==================================================")
                print("💼 PERFIL DE COMPAÑÍA Y LEAD ENRIQUECIDO:")
                print("==================================================")
                print(perfil_completo)
                print("==================================================")
                
                guardar = input("\n¿Desea guardar este lead en la Base de Datos? (s/n): ").strip().lower()
                if guardar == 's':
                    # 🌟 Llamamos a la función usando el módulo crud_leads
                    crud_leads.guardar_lead_db(nombre_input, correo_input, empresa_input, perfil_completo)
                else:
                    print("⚠️ Lead no guardado. Volviendo al menú para seguir buscando...")
            else:
                print(perfil_completo)
                    
        elif opcion == "2":
            # 🌟 Llamamos a la función usando el módulo crud_leads
            diccionario_leads = crud_leads.obtain_leads_db() if hasattr(crud_leads, 'obtain_leads_db') else crud_leads.obtener_leads_db()
            
            if not diccionario_leads:
                print("\n📭 No hay leads registrados en la base de datos aún.")
                continue
                
            print("\n--- LEADS EXISTENTES EN EL SISTEMA ---")
            for indice, datos in diccionario_leads.items():
                fecha_lista = datos['fecha'].strftime("%d/%m/%Y")
                print(f"{indice}) {datos['nombre']} — [{datos['empresa']}] ({fecha_lista})")
                
            print("0) Volver al menú principal")
                
            seleccion = input("\nSeleccione el número del lead para gestionar: ").strip()
            
            if seleccion == "0":
                continue
            elif seleccion in diccionario_leads:
                lead_seleccionado = diccionario_leads[seleccion]
                fecha_completa = lead_seleccionado['fecha'].strftime("%d/%m/%Y a las %H:%M")
                
                print("\n==================================================")
                print(f"📋 REPORTE DE INTELIGENCIA COMERCIAL (ID HISTÓRICO: {lead_seleccionado['id_db']})")
                print("==================================================")
                print(f"👤 Nombre:  {lead_seleccionado['nombre']}")
                print(f"📧 Correo:  {lead_seleccionado['correo']}")
                print(f"🏢 Empresa: {lead_seleccionado['empresa']}")
                print(f"📅 Fecha de registro: {fecha_completa}")
                print("--------------------------------------------------")
                print("🔬 INVESTIGACIÓN RETENIDA EN POSTGRESQL:")
                print(lead_seleccionado['perfil'])
                print("==================================================")
                
                # Sub-menú de acciones dentro del lead seleccionado (Ver o Eliminar)
                print("\nACCIONES:")
                print("1) Volver al listado")
                print("2) ❌ ELIMINAR este lead del sistema permanentemente")
                
                accion = input("\nSeleccione una acción (1-2): ").strip()
                if accion == "2":
                    confirmar = input(f"¿Está seguro de borrar a {lead_seleccionado['nombre']}? (s/n): ").strip().lower()
                    if confirmar == 's':
                        # 🌟 Llamamos a la función DELETE de nuestro módulo CRUD
                        crud_leads.eliminar_lead_db(lead_seleccionado['id_db'])
                else:
                    print("Volviendo...")
            else:
                print("❌ Selección inválida.")
                
        elif opcion == "3":
            print("\n👋 Cerrando el sistema de Inteligencia Comercial. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()