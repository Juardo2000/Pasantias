<<<<<<< HEAD
from google import genai
from google.genai import types
import datetime

# Autenticación con tu clave directa para la fase de Prototipo (PoC)
API_KEY = "API KEY AQUI"
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
        
        # Guardado automático en archivo de texto
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_limpio = nombre.replace(" ", "_")
        empresa_limpia = empresa.replace(" ", "_")
        nombre_archivo = f"Perfil_{nombre_limpio}_{empresa_limpia}_{timestamp}.txt"

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(response.text)
            
        print(f"✅ ¡Análisis completado! Perfil guardado en el archivo: {nombre_archivo}")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    print("=== AGENTE DE ENRIQUECIMIENTO DE LEADS ===")
    nombre_input = input("Nombre completo: ")
    correo_input = input("Correo electrónico: ")
    empresa_input = input("Nombre de la empresa: ")
    
    perfil_completo = enriquecer_lead(nombre_input, correo_input, empresa_input)
    
    print("\n==================================================")
    print("💼 PERFIL DE COMPAÑÍA Y LEAD ENRIQUECIDO:")
    print("==================================================")
=======
from google import genai
from google.genai import types
import datetime

# Autenticación con tu clave directa para la fase de Prototipo (PoC)
API_KEY = "API KEY AQUI "
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
        
        # Guardado automático en archivo de texto
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_limpio = nombre.replace(" ", "_")
        empresa_limpia = empresa.replace(" ", "_")
        nombre_archivo = f"Perfil_{nombre_limpio}_{empresa_limpia}_{timestamp}.txt"

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(response.text)
            
        print(f"✅ ¡Análisis completado! Perfil guardado en el archivo: {nombre_archivo}")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    print("=== AGENTE DE ENRIQUECIMIENTO DE LEADS ===")
    nombre_input = input("Nombre completo: ")
    correo_input = input("Correo electrónico: ")
    empresa_input = input("Nombre de la empresa: ")
    
    perfil_completo = enriquecer_lead(nombre_input, correo_input, empresa_input)
    
    print("\n==================================================")
    print("💼 PERFIL DE COMPAÑÍA Y LEAD ENRIQUECIDO:")
    print("==================================================")
>>>>>>> 8e3e3b3 (.)
    print(perfil_completo)