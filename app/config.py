import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Carga las variables del .env una sola vez, al importar este módulo
load_dotenv()


def get_model() -> ChatGoogleGenerativeAI:
    """Crea el modelo que usarán todos los agentes.

    Tenerlo en una función evita repetir la configuración en cada agente:
    si mañana cambias de modelo, de temperatura o de proveedor, se cambia aquí.
    """
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        temperature=0,   # respuestas estables, importante cuando un agente consume la salida de otro
        max_retries=3,   # reintenta ante errores temporales (503, 429)
    )