<<<<<<< HEAD
from google import genai
from google.genai import types
import datetime

# Autenticación con tu clave directa para la fase de Prototipo (PoC)
API_KEY = "API KEY AQUI"
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
        
        # Guardado automático en archivo de texto
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Crea un texto como 20260614_131500
        nombre_limpio_sector = sector.replace(" ", "_")
        nombre_limpio_pais = pais.replace(" ", "_")
        nombre_archivo = f"Licitaciones_{nombre_limpio_sector}_{nombre_limpio_pais}_{timestamp}.txt"
        
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(response.text)
            
        print(f"✅ ¡Búsqueda completada! Resultados guardados en el archivo: {nombre_archivo}")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    print("=== AGENTE DE BÚSQUEDA DE LICITACIONES ===")
    sector_input = input("Sector de industria (ej: Tecnología): ")
    pais_input = input("País (ej: Colombia): ")
    keywords_input = input("Palabras clave (ej: desarrollo de software): ")
    
    resultado = buscar_licitaciones(sector_input, pais_input, keywords_input)
    
    print("\n==================================================")
    print("📋 RESULTADOS DE LICITACIONES:")
    print("==================================================")
=======
from google import genai
from google.genai import types
import datetime

# Autenticación con tu clave directa para la fase de Prototipo (PoC)
API_KEY = "API KEY AQUI"
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
        
        # Guardado automático en archivo de texto
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Crea un texto como 20260614_131500
        nombre_limpio_sector = sector.replace(" ", "_")
        nombre_limpio_pais = pais.replace(" ", "_")
        nombre_archivo = f"Licitaciones_{nombre_limpio_sector}_{nombre_limpio_pais}_{timestamp}.txt"
        
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(response.text)
            
        print(f"✅ ¡Búsqueda completada! Resultados guardados en el archivo: {nombre_archivo}")
        return response.text
        
    except Exception as e:
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    print("=== AGENTE DE BÚSQUEDA DE LICITACIONES ===")
    sector_input = input("Sector de industria (ej: Tecnología): ")
    pais_input = input("País (ej: Colombia): ")
    keywords_input = input("Palabras clave (ej: desarrollo de software): ")
    
    resultado = buscar_licitaciones(sector_input, pais_input, keywords_input)
    
    print("\n==================================================")
    print("📋 RESULTADOS DE LICITACIONES:")
    print("==================================================")
>>>>>>> 8e3e3b3 (.)
    print(resultado)