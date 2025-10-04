# Servidor MCP para Monitoreo de Aplicación de Pagos

Este proyecto implementa un servidor MCP (Model Context Protocol) que permite a Claude diagnosticar la salud de una aplicación de pagos usando lenguaje natural, analizando métricas del sistema, logs de aplicación y estado de la base de datos.

## 📋 Descripción del Proyecto

El sistema simula 6 meses de datos de monitoreo de una aplicación de pagos, incluyendo:

- **Métricas del Sistema**: CPU y memoria con datos cada 6 horas
- **Logs de Aplicación**: Eventos de INFO, WARN, ERROR y CRITICAL 
- **Estado de Base de Datos**: Conexiones, tiempo de respuesta, transacciones activas y uso de disco

### 🚨 Períodos con Errores Simulados

Se han introducido errores consistentes en tres períodos específicos:

1. **15 de abril de 2024** (08:30-11:00): Sobrecarga del sistema
   - CPU hasta 95.4%, Memoria hasta 97.1%
   - Timeouts de base de datos, pool de conexiones exhausted
   - Múltiples fallos de pagos, servicio caído

2. **22 de julio de 2024** (14:15-15:30): Pico de tráfico no planificado
   - CPU hasta 97.2%, Memoria hasta 96.8%
   - Respuesta lenta de queries, degradación del servicio
   - Tasa de error del 23% en pagos

3. **8 de septiembre de 2024** (16:20-17:35): Agotamiento de recursos
   - CPU hasta 98.7%, Memoria hasta 97.3%
   - Timeouts de conexión, recursos exhausted
   - Tasa de éxito de pagos del 76%

## 📁 Estructura de Archivos

```
031_MCP-Python-Test/
├── metricas.json              # Métricas de CPU y memoria (timeseries)
├── logs.json                  # Logs de la aplicación por componentes
├── db.json                    # Estado de la base de datos (timeseries)
├── payment_monitoring_server.py # Servidor MCP principal
├── test_server.py             # Script de pruebas
├── claude_desktop_config.json # Configuración para Claude Desktop
├── requirements.txt           # Dependencias Python
└── README.md                  # Esta documentación
```

## 🛠️ Herramientas Disponibles en el MCP

### 1. `get_system_metrics`
Obtiene métricas del sistema (CPU y memoria) para un rango de fechas.

**Parámetros:**
- `start_date` (opcional): Fecha inicio (YYYY-MM-DD)
- `end_date` (opcional): Fecha fin (YYYY-MM-DD)
- `metric_type`: "cpu_usage", "memory_usage" o "both"

### 2. `get_application_logs`
Obtiene logs filtrados por nivel, componente o fechas.

**Parámetros:**
- `start_date` (opcional): Fecha inicio
- `end_date` (opcional): Fecha fin  
- `level` (opcional): INFO, WARN, ERROR, CRITICAL
- `component` (opcional): payment-gateway, database, etc.

### 3. `get_database_status`
Obtiene métricas de estado de la base de datos.

**Parámetros:**
- `start_date` (opcional): Fecha inicio
- `end_date` (opcional): Fecha fin
- `metric_name` (opcional): connection_count, query_response_time, active_transactions, disk_usage

### 4. `analyze_system_health`
Analiza la salud general del sistema en un período específico.

**Parámetros:**
- `date` (requerido): Fecha a analizar (YYYY-MM-DD)
- `hours_range` (opcional): Horas alrededor de la fecha (default: 2)

### 5. `detect_anomalies`
Detecta anomalías automáticamente basándose en umbrales.

**Parámetros:**
- `start_date` (opcional): Fecha inicio para detección
- `end_date` (opcional): Fecha fin para detección

## 🚀 Instalación y Uso

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Probar el Servidor

```bash
python test_server.py
```

### 3. Ejecutar el Servidor MCP

```bash
python payment_monitoring_server.py --data-dir .
```

### 4. Configurar Claude Desktop

Copiar el contenido de `claude_desktop_config.json` a tu archivo de configuración de Claude Desktop (usualmente en `~/.config/claude-desktop/config.json` en Linux).

## 🧪 Ejemplos de Uso con Claude

Una vez configurado, puedes hacer preguntas en lenguaje natural como:

### Análisis General
- *"¿Cómo estuvo la salud del sistema el 15 de abril de 2024?"*
- *"Muéstrame las métricas de CPU y memoria de la última semana de septiembre"*
- *"¿Hubo algún problema con la base de datos en julio?"*

### Detección de Problemas
- *"Detecta todas las anomalías del mes de abril"*
- *"¿Qué errores críticos hubo entre el 20 y 25 de julio?"*
- *"Compara el rendimiento del sistema entre mayo y septiembre"*

### Análisis Específicos
- *"¿Cuál fue el tiempo de respuesta promedio de la base de datos en septiembre?"*
- *"Muéstrame todos los logs del componente payment-gateway con errores"*
- *"¿Cuándo se alcanzó el pico máximo de uso de memoria?"*

## 📊 Datos de Ejemplo

### Métricas Normales
- **CPU**: 45-55% promedio
- **Memoria**: 60-72% promedio
- **DB Response Time**: 45-55ms
- **DB Connections**: 25-35

### Métricas Durante Problemas
- **CPU**: 75-98% (crítico >90%)
- **Memoria**: 83-97% (crítico >90%)
- **DB Response Time**: 850-15000ms (crítico >5000ms)
- **DB Connections**: 68-100 (máximo 100)

## 🔧 Personalización

### Agregar Nuevas Herramientas

Para agregar nuevas funcionalidades al servidor MCP:

1. Definir la herramienta en el método `_setup_tools()`
2. Implementar el método correspondiente
3. Agregar el case en `handle_call_tool()`

### Modificar Umbrales de Anomalías

Los umbrales están definidos en el método `_detect_anomalies()`:

```python
# CPU crítico
if metric["value"] > 85:
    
# Memoria crítica  
if metric["value"] > 85:

# Query lenta
if metric["value"] > 1000:  # > 1 segundo
```

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo"
Verificar que los archivos JSON estén en el directorio correcto y sean accesibles.

### Error: "Error al parsear JSON"
Verificar que los archivos JSON tengan formato válido.

### Error: "Herramienta desconocida"
Verificar que el nombre de la herramienta coincida exactamente con las definidas.

## 🤝 Contribuciones

Este es un proyecto de demostración. Para mejoras:

1. Agregar más tipos de métricas
2. Implementar alertas automáticas  
3. Integrar con sistemas de monitoreo reales
4. Agregar visualizaciones de datos
5. Implementar machine learning para detección de anomalías

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.