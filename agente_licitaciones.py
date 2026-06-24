import os
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 🌟 IMPORTAMOS EL NUEVO MÓDULO CRUD DE LICITACIONES
import crud_licitaciones

# Cargamos las variables de entorno del archivo .env
load_dotenv()

# Autenticación segura utilizando la variable de entorno
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def buscar_licitaciones(sector, pais, palabras_clave):
    print(f"\n🚀 Buscando licitaciones para el sector '{sector}' en {pais}...")
    
    prompt = (
        f"Busca ofertas de licitaciones públicas y privadas recientes del sector '{sector}' "
        f"en el país '{pais}' que contengan las siguientes palabras clave: {palabras_clave}."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Eres un agente experto en contratación pública y privada. "
                    "Tu objetivo es buscar licitaciones reales en internet utilizando la herramienta de búsqueda integrada. "
                    "Organiza los resultados detallando: 1. Nombre de la licitación, 2. Entidad convocante, "
                    "3. Fechas clave, 4. Monto o presupuesto, 5. Requisitos básicos, 6. Enlace de la fuente original."
                ),
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2
            )
        )
        
        # 🌟 Sección de guardado en .txt removida para centralizar todo en Postgres
        print(f"✅ ¡Búsqueda completada con éxito por Gemini!")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

# --------------------------------------------------------------------------
# INTERFAZ DE MENÚ DE USUARIO
# --------------------------------------------------------------------------

def menu_principal():
    while True:
        print("\n==================================================")
        print("   ⚙️ AGENTE DE BÚSQUEDA DE LICITACIONES (IA)")
        print("==================================================")
        print("1) Buscar y Analizar nuevas Licitaciones")
        print("2) Ver Licitaciones guardadas (Base de Datos / CRUD)")
        print("3) Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n--- CONFIGURACIÓN DE BÚSQUEDA ---")
            sector_input = input("Sector de industria (ej: Tecnología): ")
            pais_input = input("País (ej: Colombia): ")
            keywords_input = input("Palabras clave (ej: desarrollo de software): ")
            
            resultado = buscar_licitaciones(sector_input, pais_input, keywords_input)
            
            if resultado and not resultado.startswith("[Error"):
                print("\n==================================================")
                print("📋 RESULTADOS DE LICITACIONES ENCONTRADAS:")
                print("==================================================")
                print(resultado)
                print("==================================================")
                
                guardar = input("\n¿Desea guardar estos resultados en la Base de Datos? (s/n): ").strip().lower()
                if guardar == 's':
                    crud_licitaciones.guardar_licitacion_db(sector_input, pais_input, keywords_input, resultado)
                else:
                    print("⚠️ Resultados descartados. Volviendo al menú principal...")
            else:
                print(resultado)
                    
        elif opcion == "2":
            diccionario_licitaciones = crud_licitaciones.obtener_licitaciones_db()
            
            if not diccionario_licitaciones:
                print("\n📭 No hay licitaciones registradas en la base de datos aún.")
                continue
                
            print("\n--- HISTORIAL DE LICITACIONES EN EL SISTEMA ---")
            for indice, datos in diccionario_licitaciones.items():
                fecha_lista = datos['fecha'].strftime("%d/%m/%Y")
                print(f"{indice}) {datos['sector']} en {datos['pais']} — ({fecha_lista})")
            print("0) Volver al menú principal")
                
            seleccion = input("\nSeleccione el número del reporte para gestionar: ").strip()
            
            if seleccion == "0":
                continue
            elif seleccion in diccionario_licitaciones:
                licitacion_sel = diccionario_licitaciones[seleccion]
                fecha_completa = licitacion_sel['fecha'].strftime("%d/%m/%Y a las %H:%M")
                
                print("\n==================================================")
                print(f"📋 REPORTE HISTÓRICO DE CONTRATACIONES (ID: {licitacion_sel['id_db']})")
                print("==================================================")
                print(f"🏗️ Sector:        {licitacion_sel['sector']}")
                print(f"🌍 País:          {licitacion_sel['pais']}")
                print(f"🔑 Palabras Clave:{licitacion_sel['keywords']}")
                print(f"📅 Registrado el:  {fecha_completa}")
                print("--------------------------------------------------")
                print("🔬 LICITACIONES FILTRADAS POR GEMINI:")
                print(licitacion_sel['resultado'])
                print("==================================================")
                
                print("\nACCIONES:")
                print("1) Volver al listado")
                print("2) ❌ ELIMINAR este reporte permanentemente de la Base de Datos")
                
                accion = input("\nSeleccione una acción (1-2): ").strip()
                if accion == "2":
                    confirmar = input(f"¿Está seguro de borrar este historial del sector {licitacion_sel['sector']}? (s/n): ").strip().lower()
                    if confirmar == 's':
                        crud_licitaciones.eliminar_licitacion_db(licitacion_sel['id_db'])
                else:
                    print("Volviendo...")
            else:
                print("❌ Selección inválida.")
                
        elif opcion == "3":
            print("\n👋 Cerrando el sistema de Licitaciones Comercial. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()