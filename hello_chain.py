import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Lee el archivo .env
load_dotenv()

# WRAPPER
model = ChatGoogleGenerativeAI(
    # Modelo tomado de .env (GEMINI_MODEL)
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    # 0 = respuestas lo más estables y predecibles posible (útil para agentes)
    temperature=0,
    max_retries=3,
    timeout=30,
)

# PROMPT TEMPLATE: mensaje con huecos ({concepto}) que se rellenan al ejecutar.
# "system" define cómo se comporta el modelo; "human" es la petición concreta.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un asistente conciso. Responde en español."),
        ("human", "Explica en dos frases qué es {concepto}."),
    ]
)

# CADENA: el símbolo | pasa la salida de cada paso como entrada del siguiente.
# prompt (rellena la plantilla) -> model (llama a Gemini) -> parser (extrae el texto)
# El parser convierte la respuesta del modelo en un string simple.
chain = prompt | model | StrOutputParser()

# Este bloque solo corre si ejecutas el archivo directamente (python hello_chain.py)
if __name__ == "__main__":
    # invoke recibe un diccionario cuyas claves coinciden con los huecos del prompt
    print(chain.invoke({"concepto": "el encadenamiento de prompts"}))