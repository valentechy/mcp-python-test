"""
MCP Server Completo - Ejemplo Básico
Incluye: Resources, Prompts, Tools (servidor)
Cliente: Sampling, Roots, Elicitation
"""

from mcp.server.fastmcp import FastMCP, Context
from dataclasses import dataclass


# Definir estructura de datos para elicitation
@dataclass
class UserInfo:
    """Información del usuario solicitada mediante elicitation"""
    name: str
    age: int


# Crear servidor básico
# Nota: FastMCP configura automáticamente las capacidades básicas del servidor
mcp = FastMCP("Complete MCP Server")


@mcp.tool()
async def collect_user_info(ctx: Context) -> str:
    """
    Recopila información del usuario mediante prompts interactivos.
    Usa elicitation para obtener nombre y edad del usuario.
    
    Returns:
        Mensaje con la información recopilada o estado de la operación
    """
    result = await ctx.elicit(
        message="Por favor proporciona tu información personal",
        response_type=UserInfo
    )
    
    if result.action == "accept":
        user = result.data
        return f"¡Hola {user.name}! Tienes {user.age} años. ¡Bienvenido al MCP Server!"
    elif result.action == "decline":
        return "❌ Información no proporcionada (rechazada por el usuario)"
    else:  # cancel
        return "⚠️ Operación cancelada por el usuario"

# ============================================================
# SERVIDOR: RESOURCE
# ============================================================
@mcp.resource("example://data")
def get_data_resource() -> str:
    """
    Recurso básico que devuelve datos de ejemplo.
    Los recursos representan datos que el servidor expone.
    """
    return "Este es un recurso de ejemplo con datos básicos."


# ============================================================
# SERVIDOR: PROMPT
# ============================================================
@mcp.prompt()
def analyze_prompt(topic: str) -> str:
    """
    Prompt básico para analizar un tema.
    Los prompts son plantillas reutilizables.
    
    Args:
        topic: El tema a analizar
    """
    return f"""Analiza el siguiente tema en detalle:

Tema: {topic}

Por favor proporciona:
1. Una descripción general
2. Puntos clave
3. Consideraciones importantes"""


# ============================================================
# SERVIDOR: TOOL
# ============================================================
@mcp.tool()
def calculate_sum(a: float, b: float) -> float:
    """
    Herramienta básica que suma dos números.
    Las tools son funciones que el cliente puede invocar.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        La suma de a y b
    """
    return a + b


# ============================================================
# HERRAMIENTA DE INFORMACIÓN
# ============================================================

@mcp.tool()
def server_info() -> dict:
    """
    Devuelve información sobre las capacidades del servidor.
    
    Returns:
        Información sobre el servidor y sus características
    """
    return {
        "server_name": "Complete MCP Server",
        "version": "1.0.0",
        "features": {
            "resources": "Expone datos mediante URIs (ejemplo: example://data)",
            "prompts": "Plantillas reutilizables para generar prompts",
            "tools": "Funciones que el cliente puede invocar",
            "elicitation": "Solicitud interactiva de información al usuario"
        },
        "available_tools": [
            "calculate_sum", 
            "echo", 
            "server_info",
            "collect_user_info (con elicitation - solicita nombre y edad)"
        ],
        "available_resources": ["example://data"],
        "available_prompts": ["analyze_prompt"]
    }


# ============================================================
# TOOL ADICIONAL: ECHO
# ============================================================
@mcp.tool()
def echo(text: str) -> str:
    """
    Herramienta simple que devuelve el texto de entrada.
    
    Args:
        text: Texto a hacer eco
    
    Returns:
        El texto de entrada
    """
    return f"Echo: {text}"

if __name__ == "__main__":
    # Iniciar el servidor
    mcp.run()