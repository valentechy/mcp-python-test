# MCP Server Completo - Ejemplo Básico

Este es un servidor MCP (Model Context Protocol) completo que incluye todas las características principales tanto del lado del servidor como las capacidades del cliente.

## Características Implementadas

### Lado del Servidor

1. **Resource** (`get_data_resource`)
   - URI: `example://data`
   - Proporciona datos de ejemplo
   - Los recursos representan datos que el servidor expone

2. **Prompt** (`analyze_prompt`)
   - Plantilla reutilizable para análisis
   - Parámetro: `topic` (tema a analizar)
   - Genera un prompt estructurado

3. **Tools** (Herramientas)
   - `calculate_sum`: Suma dos números
   - `echo`: Devuelve el texto de entrada
   - `example_use_client_features`: Demuestra el uso de capacidades del cliente

### Capacidades del Cliente

El servidor está configurado para usar estas capacidades del cliente cuando estén disponibles:

1. **Sampling**
   - Permite al servidor solicitar completions de LLM al cliente
   - Útil para generar contenido usando el modelo del cliente

2. **Roots**
   - Permite listar raíces del sistema de archivos del cliente
   - Útil para navegación y acceso a archivos

3. **Elicitation**
   - Permite al servidor solicitar información interactiva al usuario
   - Útil para obtener confirmaciones o datos adicionales

## Instalación

```bash
# Instalar dependencias
pip install mcp
```

## Uso

### Ejecutar el servidor

```bash
python simple_echo.py
```

### Configuración en Claude Desktop

Añade esto a tu archivo de configuración de Claude Desktop:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "complete-mcp-server": {
      "command": "python",
      "args": ["/ruta/completa/a/simple_echo.py"]
    }
  }
}
```

## Ejemplos de Uso

### Usar la herramienta calculate_sum

```
Usa la herramienta calculate_sum para sumar 5 y 3
```

### Usar el recurso

```
Muéstrame el contenido del recurso example://data
```

### Usar el prompt

```
Usa el prompt analyze_prompt con el tema "Inteligencia Artificial"
```

## Estructura del Código

```python
# 1. Importaciones
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent, EmbeddedResource

# 2. Crear servidor con capacidades
mcp = FastMCP("Complete MCP Server", capabilities={...})

# 3. Definir recursos
@mcp.resource("uri://path")
def get_resource(): ...

# 4. Definir prompts
@mcp.prompt()
def my_prompt(param: str): ...

# 5. Definir herramientas
@mcp.tool()
def my_tool(param: str): ...

# 6. Ejecutar servidor
if __name__ == "__main__":
    mcp.run()
```

## Expandir el Servidor

Para añadir más funcionalidad:

1. **Nuevos Resources**: Añade más decoradores `@mcp.resource()`
2. **Nuevos Prompts**: Añade más decoradores `@mcp.prompt()`
3. **Nuevas Tools**: Añade más decoradores `@mcp.tool()`
4. **Usar Sampling**: Descomentar el código en `example_use_client_features`
5. **Usar Roots**: Implementar lógica para acceder al sistema de archivos
6. **Usar Elicitation**: Implementar diálogos interactivos con el usuario

## Notas Importantes

- Las capacidades del cliente (sampling, roots, elicitation) solo funcionan si el cliente las implementa
- El servidor puede verificar qué capacidades están disponibles antes de usarlas
- Este es un ejemplo básico diseñado para ser ampliado según tus necesidades

## Recursos Adicionales

- [Documentación MCP](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
