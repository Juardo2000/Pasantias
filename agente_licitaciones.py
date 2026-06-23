from google import genai 
from google.genai import types

# Inicializamos el cliente con tu API Key
# Este objeto 'client' es el encargado de autenticar y conectar tu script con los servidores de Google AI Studio.
API_KEY = "API KEY AQUI"
client = genai.Client(api_key=API_KEY)

def buscar_licitaciones(sector, pais, palabras_clave):
    # Mensaje informativo en la terminal para que el usuario sepa que el proceso inició.
    print(f"\n🚀 Buscando licitaciones para el sector '{sector}' en {pais}...")
    
    # Creamos un prompt específico combinando las variables del usuario
    # Aquí se empaquetan dinámicamente las entradas de la terminal en una sola instrucción para el modelo.
    prompt = (
        f"Busca ofertas de licitaciones públicas y privadas recientes del sector '{sector}' "
        f"en el país '{pais}' que contengan las siguientes palabras clave: {palabras_clave}."
    )
    
    try:
        # Aquí se hace la llamada oficial a la API de Gemini utilizando la configuración agéntica.
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Especificamos el modelo (Gemini 2.5 Flash), ideal para velocidad y tareas con herramientas.
            contents=prompt,
            config=types.GenerateContentConfig(
                # LE ENSEÑAMOS A GEMINI CÓMO ACTUAR
                # El 'system_instruction' define el rol experto del agente y delimita estrictamente cómo estructurar los datos extraídos.
                system_instruction=(
                    "Eres un agente experto en contratación pública y privada. "
                    "Tu objetivo es buscar licitaciones reales en internet utilizando la herramienta de búsqueda integrada. "
                    "Organiza los resultados en formato de lista clara o tabla para cada licitación encontrada, "
                    "detallando estrictamente: 1. Nombre de la licitación, 2. Entidad convocante, "
                    "3. Fechas clave (límite de entrega), 4. Monto o presupuesto (si está disponible), "
                    "5. Requisitos básicos, 6. Enlace de la fuente original."
                ),
                # 🌟 ESTA LÍNEA ACTIVA LA BÚSQUEDA EN INTERNET EN TIEMPO REAL
                # Activa el 'Grounding' nativo. Le da permiso a Gemini de crear queries, consultar Google y leer los resultados web en vivo.
                tools=[types.Tool(google_search=types.GoogleSearch())],
                # La temperatura baja (0.2) asegura respuestas factuales y precisas, minimizando el riesgo de que el modelo invente datos.
                temperature=0.2
            )
        )
        # Retorna el texto final ya procesado y formateado por el agente.
        return response.text
    except Exception as e:
        # En caso de cualquier falla (red, clave, cuota), captura el error y evita que el programa se rompa abruptamente.
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    # Entrada del flujo por terminal (CLI) para interactuar directamente desde VS Code.
    print("=== AGENTE DE BÚSQUEDA DE LICITACIONES ===")
    sector_input = input("Sector de industria (ej: Tecnología, Construcción): ")
    pais_input = input("País (ej: Colombia, México, España): ")
    keywords_input = input("Palabras clave (ej: desarrollo de software, plataformas web): ")
    
    # Se invoca la función del agente pasándole las variables recolectadas.
    resultado = buscar_licitaciones(sector_input, pais_input, keywords_input)
    
    # Imprime en la consola el reporte limpio que devolvió el agente.
    print("\n==================================================")
    print("📋 RESULTADOS DE LICITACIONES ENCONTRADAS:")
    print("==================================================")
    print(resultado)