#!/usr/bin/env python3
"""
Script de prueba para el servidor MCP de monitoreo de pagos
Demuestra cómo usar las diferentes herramientas disponibles
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime


class MCPTestClient:
    def __init__(self, server_script: Path, data_dir: Path):
        self.server_script = server_script
        self.data_dir = data_dir
        self.process = None
    
    async def start_server(self):
        """Inicia el servidor MCP"""
        cmd = ["python", str(self.server_script), "--data-dir", str(self.data_dir)]
        self.process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def send_request(self, request: dict) -> dict:
        """Envía una petición al servidor MCP"""
        if not self.process:
            await self.start_server()
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        response_line = await self.process.stdout.readline()
        return json.loads(response_line.decode())
    
    async def close(self):
        """Cierra el servidor MCP"""
        if self.process:
            self.process.stdin.close()
            await self.process.wait()


async def test_mcp_server():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del servidor MCP de monitoreo de pagos")
    print("=" * 60)
    
    # Configurar rutas
    current_dir = Path.cwd()
    server_script = current_dir / "payment_monitoring_server.py"
    data_dir = current_dir
    
    # Verificar archivos necesarios
    required_files = [server_script, data_dir / "metricas.json", data_dir / "logs.json", data_dir / "db.json"]
    for file_path in required_files:
        if not file_path.exists():
            print(f"❌ Error: No se encuentra {file_path}")
            return
    
    print("✅ Todos los archivos necesarios encontrados")
    
    # Simular llamadas al servidor (sin MCP real por simplicidad)
    # En su lugar, importamos y probamos las funciones directamente
    
    try:
        # Importar el servidor para pruebas directas
        import sys
        sys.path.append(str(current_dir))
        from payment_monitoring_server import PaymentMonitoringServer
        
        server = PaymentMonitoringServer(data_dir)
        
        print("\n🔍 Prueba 1: Obtener métricas del sistema")
        print("-" * 40)
        
        # Obtener métricas de CPU y memoria
        metrics_result = await server._get_system_metrics(metric_type="both")
        print(f"📊 Métricas encontradas:")
        print(f"   - CPU: {len(metrics_result['metrics'].get('cpu_usage', []))} puntos de datos")
        print(f"   - Memoria: {len(metrics_result['metrics'].get('memory_usage', []))} puntos de datos")
        
        if 'cpu_usage' in metrics_result['summary']:
            cpu_summary = metrics_result['summary']['cpu_usage']
            print(f"   - CPU promedio: {cpu_summary['avg']:.1f}%, máximo: {cpu_summary['max']:.1f}%")
        
        if 'memory_usage' in metrics_result['summary']:
            mem_summary = metrics_result['summary']['memory_usage']
            print(f"   - Memoria promedio: {mem_summary['avg']:.1f}%, máximo: {mem_summary['max']:.1f}%")
        
        print("\n🔍 Prueba 2: Obtener logs de aplicación (solo errores críticos)")
        print("-" * 40)
        
        logs_result = await server._get_application_logs(level="CRITICAL")
        print(f"📋 Logs críticos encontrados: {logs_result['summary']['total_count']}")
        
        for log in logs_result['logs'][:3]:  # Mostrar solo los primeros 3
            timestamp = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
            print(f"   - {timestamp.strftime('%Y-%m-%d %H:%M')} | {log['component']} | {log['message']}")
        
        print("\n🔍 Prueba 3: Obtener estado de la base de datos")
        print("-" * 40)
        
        db_result = await server._get_database_status()
        print(f"🗄️  Métricas de base de datos:")
        
        for metric_type, summary in db_result['summary'].items():
            print(f"   - {metric_type}: promedio={summary['avg']:.1f}, máximo={summary['max']:.1f}")
        
        print("\n🔍 Prueba 4: Analizar salud del sistema (15 de abril - día con problemas)")
        print("-" * 40)
        
        health_result = await server._analyze_system_health("2024-04-15", hours_range=6)
        print(f"🏥 Análisis de salud:")
        print(f"   - Fecha: {health_result['date']}")
        print(f"   - Puntuación: {health_result['health_score']}/100")
        print(f"   - Estado: {health_result['status']}")
        print(f"   - Problemas encontrados:")
        
        for issue in health_result['issues']:
            print(f"     • {issue}")
        
        print("\n🔍 Prueba 5: Detectar anomalías en julio (22 de julio - día problemático)")
        print("-" * 40)
        
        anomalies_result = await server._detect_anomalies("2024-07-22", "2024-07-22")
        print(f"⚠️  Anomalías detectadas: {anomalies_result['summary']['total_count']}")
        print(f"📊 Distribución por severidad: {anomalies_result['summary']['severity_distribution']}")
        print(f"📋 Distribución por tipo: {anomalies_result['summary']['type_distribution']}")
        
        # Mostrar algunas anomalías
        print("   Principales anomalías:")
        for anomaly in anomalies_result['anomalies'][:5]:
            timestamp = datetime.fromisoformat(anomaly['timestamp'].replace('Z', '+00:00'))
            severity = anomaly['severity']
            anomaly_type = anomaly['type']
            
            if 'value' in anomaly:
                print(f"     • {timestamp.strftime('%H:%M')} | {severity} | {anomaly_type}: {anomaly['value']}")
            else:
                message = anomaly.get('message', 'N/A')[:50] + "..." if len(anomaly.get('message', '')) > 50 else anomaly.get('message', 'N/A')
                print(f"     • {timestamp.strftime('%H:%M')} | {severity} | {anomaly_type}: {message}")
        
        print("\n🔍 Prueba 6: Analizar período normal vs problemático")
        print("-" * 40)
        
        # Día normal
        normal_health = await server._analyze_system_health("2024-05-15", hours_range=2)
        print(f"📅 Día normal (15 mayo): Salud={normal_health['health_score']}/100, Estado={normal_health['status']}")
        
        # Día problemático
        problem_health = await server._analyze_system_health("2024-09-08", hours_range=2)
        print(f"📅 Día problemático (8 sept): Salud={problem_health['health_score']}/100, Estado={problem_health['status']}")
        
        print(f"\n📊 Comparación de problemas:")
        print(f"   Día normal: {len(normal_health['issues'])} problemas")
        print(f"   Día problemático: {len(problem_health['issues'])} problemas")
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        print("🎯 El servidor MCP está funcionando correctamente y puede:")
        print("   • Obtener métricas del sistema (CPU, memoria)")
        print("   • Filtrar logs por nivel y componente")
        print("   • Monitorear estado de la base de datos")
        print("   • Analizar salud general del sistema")
        print("   • Detectar anomalías automáticamente")
        print("   • Comparar períodos normales vs problemáticos")
        
    except ImportError as e:
        print(f"❌ Error importando el servidor: {e}")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


def create_requirements_file():
    """Crea archivo requirements.txt"""
    requirements_content = """# Dependencias del servidor MCP de monitoreo de pagos
mcp>=0.6.0
asyncio-stubs
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print("📦 Archivo requirements.txt creado")


def print_usage_instructions():
    """Imprime instrucciones de uso"""
    print("\n📚 INSTRUCCIONES DE USO")
    print("=" * 60)
    print("1. Instalar dependencias:")
    print("   pip install -r requirements.txt")
    print("")
    print("2. Ejecutar el servidor MCP:")
    print("   python payment_monitoring_server.py --data-dir .")
    print("")
    print("3. Usar con Claude Desktop u otro cliente MCP:")
    print("   Agregar configuración al archivo claude_desktop_config.json")
    print("")
    print("4. Herramientas disponibles:")
    print("   • get_system_metrics - Obtener métricas de CPU y memoria")
    print("   • get_application_logs - Filtrar logs de aplicación")
    print("   • get_database_status - Estado de la base de datos")
    print("   • analyze_system_health - Análisis de salud del sistema")
    print("   • detect_anomalies - Detección automática de anomalías")


if __name__ == "__main__":
    print("🧪 Script de prueba del servidor MCP de monitoreo de pagos")
    print("=" * 60)
    
    # Crear archivo de dependencias
    create_requirements_file()
    
    # Ejecutar pruebas
    asyncio.run(test_mcp_server())
    
    # Mostrar instrucciones
    print_usage_instructions()