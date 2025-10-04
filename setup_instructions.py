#!/usr/bin/env python3
"""
Instrucciones para configurar el servidor MCP en Fedora
"""

def main():
    print("🚀 Configuración del Servidor MCP en Fedora")
    print("=" * 50)
    print()
    
    print("✅ ESTADO ACTUAL:")
    print("   • MCP instalado correctamente")
    print("   • Datos de prueba generados (6 meses)")
    print("   • Análisis de datos funcionando")
    print()
    
    print("🔧 CONFIGURACIÓN PARA CLAUDE DESKTOP:")
    print()
    print("1. Instalar Claude Desktop desde:")
    print("   https://claude.ai/download")
    print()
    
    print("2. Crear/editar el archivo de configuración:")
    print("   ~/.config/claude-desktop/config.json")
    print()
    
    print("3. Agregar esta configuración:")
    config = """{
  "mcpServers": {
    "payment-monitoring": {
      "command": "python3",
      "args": [
        "/home/surver/001_IT/001_Personal_Projects/031_MCP-Python-Test/payment_monitoring_server_fixed.py",
        "--data-dir",
        "/home/surver/001_IT/001_Personal_Projects/031_MCP-Python-Test"
      ],
      "env": {
        "PYTHONPATH": "/home/surver/001_IT/001_Personal_Projects/031_MCP-Python-Test"
      }
    }
  }
}"""
    print(config)
    print()
    
    print("4. Reiniciar Claude Desktop")
    print()
    
    print("🎯 EJEMPLOS DE USO CON CLAUDE:")
    print()
    examples = [
        "¿Qué pasó el 15 de abril de 2024 que causó problemas?",
        "Analiza la salud del sistema durante julio de 2024",
        "Muéstrame todas las anomalías detectadas en septiembre",
        "Compara el rendimiento entre mayo y septiembre",
        "¿Cuáles son los componentes que más errores generan?",
        "¿Cuándo se alcanzaron los picos máximos de CPU y memoria?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   {i}. \"{example}\"")
    
    print()
    print("📊 DATOS DISPONIBLES:")
    print("   • CPU y Memoria: 62 puntos de datos en 6 meses")
    print("   • Logs: 75+ eventos de aplicación")
    print("   • DB: Métricas de conexiones y rendimiento")
    print("   • 3 períodos problemáticos simulados con errores correlacionados")
    print()
    
    print("🚨 PERÍODOS PROBLEMÁTICOS:")
    print("   • 15 abril 2024: Sobrecarga del sistema (CPU 95%, Mem 97%)")
    print("   • 22 julio 2024: Pico de tráfico (degradación del servicio)")
    print("   • 8 sept 2024: Agotamiento recursos (tasa éxito 76%)")
    print()
    
    print("✅ El servidor está listo para usar con Claude Desktop!")
    print("   Una vez configurado, podrás hacer preguntas en lenguaje natural")
    print("   sobre el estado y la salud de tu aplicación de pagos.")


if __name__ == "__main__":
    main()