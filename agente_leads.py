from google import genai
from google.genai import types

# Inicializamos el cliente con tu API Key
# Clave que autentica la conexión segura de tu entorno local de VS Code con los servidores de Google AI Studio.
API_KEY = "API KEY AQUI"
client = genai.Client(api_key=API_KEY)

def enriquecer_lead(nombre, correo, empresa):
    # Mensaje informativo en la consola que indica las variables iniciales recopiladas que se van a investigar.
    print(f"\n🔍 Investigando fuentes públicas para el lead: {nombre} ({empresa})...")
    
    # Creamos un prompt específico combinando las variables del usuario
    # Datos básicos proporcionados que servirán como punto de partida para el rastreo del agente en internet.
    prompt = (
        f"Realiza una investigación profunda en internet sobre el siguiente perfil:\n"
        f"- Nombre de la persona: {nombre}\n"
        f"- Correo corporativo: {correo}\n"
        f"- Nombre de la empresa: {empresa}\n"
    )
    
    try:
        # Se realiza la llamada oficial al modelo generativo inyectando las herramientas de búsqueda.
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Se utiliza Gemini 2.5 Flash por su velocidad y eficiencia con herramientas externas.
            contents=prompt,
            config=types.GenerateContentConfig(
                # El 'system_instruction' moldea el comportamiento del modelo para que actúe bajo un rol comercial estricto.
                # También le define las fuentes de datos válidas (públicas) y las secciones exactas del reporte final.
                system_instruction=(
                    "Eres un agente de Inteligencia Comercial de alta precisión. Tu tarea es enriquecer "
                    "datos de leads usando únicamente información pública y legal disponible en internet (como LinkedIn público, "
                    "webs corporativas, comunicados de prensa, etc.).\n\n"
                    "Estructura el perfil final de la siguiente manera:\n"
                    "1. PERFIL DE LA PERSONA: Cargo actual, trayectoria, áreas de especialización y enlaces a perfiles públicos.\n"
                    "2. ÁNGULO DE CONEXIÓN: Sugiere una idea o gancho personalizado para contactar a esta persona basándote en lo descubierto."
                ),
                # 🌟 Activamos nuevamente la búsqueda en vivo de Google
                # Habilita el módulo de Grounding para que el agente navegue por Google en tiempo real de forma autónoma.
                tools=[types.Tool(google_search=types.GoogleSearch())],
                # Una temperatura moderadamente baja (0.3) le da un margen mínimo de flexibilidad para redactar el 'ángulo de conexión' 
                # sin riesgo de que invente datos falsos sobre la persona o la empresa.
                temperature=0.2
            )
        )
        # Retorna el texto del perfil comercial estructurado y listo para el usuario.
        return response.text
    except Exception as e:
        # Bloque de seguridad que captura errores de red o autenticación, mostrando el fallo sin colapsar la terminal.
        return f"[Error en el Agente]: {e}"

if __name__ == "__main__":
    # Interfaz de línea de comandos (CLI) interactiva para ejecutar las pruebas directamente en VS Code.
    print("=== AGENTE DE ENRIQUECIMIENTO DE LEADS ===")
    nombre_input = input("Nombre completo (o aproximado): ")
    correo_input = input("Correo electrónico: ")
    empresa_input = input("Nombre de la empresa: ")
    
    # Se ejecuta la función enviando los inputs de texto limpios.
    perfil_completo = enriquecer_lead(nombre_input, correo_input, empresa_input)
    
    # Despliegue del informe de inteligencia comercial generado autónomamente por el agente.
    print("\n==================================================")
    print("💼 PERFIL DE COMPAÑÍA Y LEAD ENRIQUECIDO:")
    print("==================================================")
    print(perfil_completo)