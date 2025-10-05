# 📊 Análisis de Tickets de Soporte - MCP Server

## 🎯 ¿Qué tienes ahora?

✅ **Archivo JSON**: `tickets_soporte.json` con **2,500 tickets** de ejemplo del último mes
✅ **Herramienta MCP**: `analizar_tickets` que puede procesar y analizar los datos
✅ **Datos realistas**: 5 categorías principales con distribución y prioridades reales

## 📈 Resultados del Análisis

### Distribución por Categorías (Top 5):
1. **Problemas de Facturación**: 838 tickets (34.5%)
2. **Problemas Técnicos**: 573 tickets (23.6%)  
3. **Consultas de Cuenta**: 504 tickets (20.8%)
4. **Solicitudes de Funcionalidades**: 324 tickets (13.4%)
5. **Problemas de Seguridad**: 187 tickets (7.7%)

### 🚨 Ejemplos de Quejas Urgentes sobre Facturación:

1. **[ALTA]** "La factura muestra un importe incorrecto de 2436€ en lugar de 1561€"
2. **[ALTA]** "No recibí factura del mes de Abril"  
3. **[ALTA]** "Error en el cálculo del IVA en factura #INV-12758"

## 🔧 Cómo usar la herramienta MCP

### Análisis General
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "analizar_tickets", "arguments": {}}}' | python3 mcp_minimal.py
```

### Análisis de Categoría Específica
```bash
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "analizar_tickets", "arguments": {"categoria_filtro": "Problemas de Facturación"}}}' | python3 mcp_minimal.py
```

### Categorías Disponibles:
- "Problemas de Facturación"
- "Problemas Técnicos"
- "Consultas de Cuenta"  
- "Solicitudes de Funcionalidades"
- "Problemas de Seguridad"

## 📊 Estructura del Archivo JSON

Cada ticket contiene:
```json
{
  "id": "TICK-00001",
  "fecha_creacion": "2025-09-15 14:23:45",
  "categoria": "Problemas de Facturación",
  "prioridad": "Alta",
  "estado": "Abierto",
  "titulo": "Cargo duplicado en mi tarjeta...",
  "descripcion": "Cargo duplicado en mi tarjeta de crédito por 1250€",
  "cliente": {
    "nombre": "María García",
    "empresa": "TechSoft Solutions",
    "email": "maria.garcia@techsoftsolutions.com"
  },
  "tiempo_resolucion_horas": 24,
  "satisfaccion_cliente": 3,
  "agente_asignado": "Agente5"
}
```

## 🎯 Respuesta a tu Prompt Original

Tu herramienta MCP ahora puede responder perfectamente a este prompt:

> *"Analiza todos los tickets de soporte del último mes. Agrupa las quejas en 5 categorías principales, calcula el porcentaje de cada una y dame tres ejemplos textuales de las quejas más urgentes sobre 'problemas de facturación'"*

**Respuesta automatizada:**

📊 **Análisis de 2,426 tickets del último mes:**

**Top 5 Categorías:**
1. Problemas de Facturación: 34.5%
2. Problemas Técnicos: 23.6%
3. Consultas de Cuenta: 20.8%
4. Solicitudes de Funcionalidades: 13.4%
5. Problemas de Seguridad: 7.7%

**3 Quejas más urgentes de Facturación:**
1. [ALTA] "La factura muestra un importe incorrecto de 2436€ en lugar de 1561€"
2. [ALTA] "No recibí factura del mes de Abril"
3. [ALTA] "Error en el cálculo del IVA en factura #INV-12758"

## 🚀 Próximos Pasos

- **Conecta a Claude Desktop**: Usa la herramienta desde la interfaz
- **Personaliza análisis**: Modifica fechas, filtros o métricas
- **Agrega más datos**: Genera más tickets con diferentes patrones
- **Extiende funcionalidades**: Análisis por tiempo, agente, etc.

¡Tu MCP Server ahora es un analizador de datos de soporte completo! 🎉