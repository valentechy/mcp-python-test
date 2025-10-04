#!/usr/bin/env python3
"""
Script de prueba simplificado para demostrar el análisis de datos
Muestra las funcionalidades principales sin requerir la librería MCP
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any


class PaymentDataAnalyzer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Carga un archivo JSON desde el directorio de datos"""
        try:
            file_path = self.data_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {filename} en {self.data_dir}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al parsear JSON en {filename}: {e}")
    
    def _parse_date(self, date_str: str) -> datetime:
        """Convierte string de fecha a objeto datetime"""
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    
    def _filter_by_date_range(self, data: List[Dict], start_date: Optional[str], end_date: Optional[str]) -> List[Dict]:
        """Filtra datos por rango de fechas"""
        if not start_date and not end_date:
            return data
        
        filtered_data = []
        for item in data:
            item_date = self._parse_date(item['timestamp']).replace(tzinfo=None)
            
            if start_date:
                start_dt = datetime.fromisoformat(start_date)
                if item_date < start_dt:
                    continue
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
                if item_date >= end_dt:
                    continue
            
            filtered_data.append(item)
        
        return filtered_data
    
    def get_system_metrics(self, start_date: Optional[str] = None, 
                          end_date: Optional[str] = None,
                          metric_type: str = "both") -> Dict[str, Any]:
        """Obtiene métricas del sistema"""
        metrics_data = self._load_json_file("metricas.json")
        
        result = {"metrics": {}, "summary": {}}
        
        if metric_type in ["cpu_usage", "both"]:
            cpu_data = self._filter_by_date_range(metrics_data["cpu_usage"], start_date, end_date)
            result["metrics"]["cpu_usage"] = cpu_data
            if cpu_data:
                cpu_values = [item["value"] for item in cpu_data]
                result["summary"]["cpu_usage"] = {
                    "avg": sum(cpu_values) / len(cpu_values),
                    "max": max(cpu_values),
                    "min": min(cpu_values),
                    "count": len(cpu_values)
                }
        
        if metric_type in ["memory_usage", "both"]:
            memory_data = self._filter_by_date_range(metrics_data["memory_usage"], start_date, end_date)
            result["metrics"]["memory_usage"] = memory_data
            if memory_data:
                memory_values = [item["value"] for item in memory_data]
                result["summary"]["memory_usage"] = {
                    "avg": sum(memory_values) / len(memory_values),
                    "max": max(memory_values),
                    "min": min(memory_values),
                    "count": len(memory_values)
                }
        
        return result
    
    def get_application_logs(self, start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           level: Optional[str] = None,
                           component: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene logs de la aplicación"""
        logs_data = self._load_json_file("logs.json")
        
        filtered_logs = self._filter_by_date_range(logs_data["application_logs"], start_date, end_date)
        
        if level:
            filtered_logs = [log for log in filtered_logs if log["level"] == level]
        
        if component:
            filtered_logs = [log for log in filtered_logs if log["component"] == component]
        
        # Estadísticas por nivel
        level_counts = {}
        for log in filtered_logs:
            log_level = log["level"]
            level_counts[log_level] = level_counts.get(log_level, 0) + 1
        
        return {
            "logs": filtered_logs,
            "summary": {
                "total_count": len(filtered_logs),
                "level_distribution": level_counts,
                "date_range": {
                    "start": start_date,
                    "end": end_date
                }
            }
        }
    
    def analyze_system_health(self, date: str, hours_range: int = 2) -> Dict[str, Any]:
        """Analiza la salud del sistema en una fecha específica"""
        target_date = datetime.fromisoformat(date)
        start_time = target_date - timedelta(hours=hours_range)
        end_time = target_date + timedelta(hours=hours_range)
        
        start_str = start_time.strftime("%Y-%m-%d")
        end_str = end_time.strftime("%Y-%m-%d")
        
        # Obtener datos de todas las fuentes
        metrics = self.get_system_metrics(start_str, end_str)
        logs = self.get_application_logs(start_str, end_str)
        
        # Análisis de salud
        health_score = 100
        issues = []
        
        # Verificar CPU
        if "cpu_usage" in metrics["summary"]:
            cpu_max = metrics["summary"]["cpu_usage"]["max"]
            if cpu_max > 90:
                health_score -= 30
                issues.append(f"CPU crítico: {cpu_max:.1f}%")
            elif cpu_max > 75:
                health_score -= 15
                issues.append(f"CPU alto: {cpu_max:.1f}%")
        
        # Verificar memoria
        if "memory_usage" in metrics["summary"]:
            mem_max = metrics["summary"]["memory_usage"]["max"]
            if mem_max > 90:
                health_score -= 30
                issues.append(f"Memoria crítica: {mem_max:.1f}%")
            elif mem_max > 75:
                health_score -= 15
                issues.append(f"Memoria alta: {mem_max:.1f}%")
        
        # Verificar logs críticos
        critical_logs = logs["summary"]["level_distribution"].get("CRITICAL", 0)
        error_logs = logs["summary"]["level_distribution"].get("ERROR", 0)
        
        if critical_logs > 0:
            health_score -= 40
            issues.append(f"Logs críticos encontrados: {critical_logs}")
        
        if error_logs > 5:
            health_score -= 20
            issues.append(f"Múltiples errores: {error_logs}")
        
        # Determinar estado general
        if health_score >= 80:
            status = "HEALTHY"
        elif health_score >= 60:
            status = "WARNING"
        elif health_score >= 40:
            status = "CRITICAL"
        else:
            status = "FAILED"
        
        return {
            "date": date,
            "health_score": max(0, health_score),
            "status": status,
            "issues": issues,
            "metrics_summary": metrics["summary"],
            "logs_summary": logs["summary"]
        }
    
    def detect_anomalies(self, start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> Dict[str, Any]:
        """Detecta anomalías en el sistema"""
        anomalies = []
        
        # Obtener métricas del sistema
        metrics = self.get_system_metrics(start_date, end_date)
        
        # Detectar anomalías de CPU
        if "cpu_usage" in metrics["metrics"]:
            for metric in metrics["metrics"]["cpu_usage"]:
                if metric["value"] > 85:
                    anomalies.append({
                        "timestamp": metric["timestamp"],
                        "type": "HIGH_CPU",
                        "value": metric["value"],
                        "threshold": 85,
                        "severity": "CRITICAL" if metric["value"] > 95 else "HIGH"
                    })
        
        # Detectar anomalías de memoria
        if "memory_usage" in metrics["metrics"]:
            for metric in metrics["metrics"]["memory_usage"]:
                if metric["value"] > 85:
                    anomalies.append({
                        "timestamp": metric["timestamp"],
                        "type": "HIGH_MEMORY",
                        "value": metric["value"],
                        "threshold": 85,
                        "severity": "CRITICAL" if metric["value"] > 95 else "HIGH"
                    })
        
        # Obtener logs críticos
        logs = self.get_application_logs(start_date, end_date, level="CRITICAL")
        for log in logs["logs"]:
            anomalies.append({
                "timestamp": log["timestamp"],
                "type": "CRITICAL_LOG",
                "message": log["message"],
                "component": log["component"],
                "severity": "CRITICAL"
            })
        
        # Ordenar por timestamp
        anomalies.sort(key=lambda x: x["timestamp"])
        
        # Estadísticas
        severity_counts = {}
        type_counts = {}
        for anomaly in anomalies:
            severity = anomaly["severity"]
            anomaly_type = anomaly["type"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            type_counts[anomaly_type] = type_counts.get(anomaly_type, 0) + 1
        
        return {
            "anomalies": anomalies,
            "summary": {
                "total_count": len(anomalies),
                "severity_distribution": severity_counts,
                "type_distribution": type_counts,
                "date_range": {
                    "start": start_date,
                    "end": end_date
                }
            }
        }


def main():
    """Función principal de prueba"""
    print("🚀 Demostración del Analizador de Datos de Monitoreo de Pagos")
    print("=" * 65)
    
    # Configurar rutas
    current_dir = Path.cwd()
    
    # Verificar archivos necesarios
    required_files = ["metricas.json", "logs.json", "db.json"]
    for filename in required_files:
        if not (current_dir / filename).exists():
            print(f"❌ Error: No se encuentra {filename}")
            return
    
    print("✅ Todos los archivos de datos encontrados")
    
    try:
        analyzer = PaymentDataAnalyzer(current_dir)
        
        print("\n🔍 Prueba 1: Obtener métricas del sistema completas")
        print("-" * 50)
        
        metrics_result = analyzer.get_system_metrics(metric_type="both")
        print(f"📊 Métricas encontradas:")
        print(f"   - CPU: {len(metrics_result['metrics'].get('cpu_usage', []))} puntos de datos")
        print(f"   - Memoria: {len(metrics_result['metrics'].get('memory_usage', []))} puntos de datos")
        
        if 'cpu_usage' in metrics_result['summary']:
            cpu_summary = metrics_result['summary']['cpu_usage']
            print(f"   - CPU promedio: {cpu_summary['avg']:.1f}%, máximo: {cpu_summary['max']:.1f}%")
        
        if 'memory_usage' in metrics_result['summary']:
            mem_summary = metrics_result['summary']['memory_usage']
            print(f"   - Memoria promedio: {mem_summary['avg']:.1f}%, máximo: {mem_summary['max']:.1f}%")
        
        print("\n🔍 Prueba 2: Analizar logs críticos")
        print("-" * 50)
        
        logs_result = analyzer.get_application_logs(level="CRITICAL")
        print(f"📋 Logs críticos encontrados: {logs_result['summary']['total_count']}")
        
        for i, log in enumerate(logs_result['logs'][:5]):  # Mostrar solo los primeros 5
            timestamp = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
            print(f"   {i+1}. {timestamp.strftime('%Y-%m-%d %H:%M')} | {log['component']} | {log['message'][:60]}...")
        
        print("\n🔍 Prueba 3: Analizar salud del sistema en fechas problemáticas")
        print("-" * 50)
        
        problem_dates = ["2024-04-15", "2024-07-22", "2024-09-08"]
        
        for date in problem_dates:
            health_result = analyzer.analyze_system_health(date, hours_range=3)
            print(f"\n📅 {date}:")
            print(f"   - Puntuación de salud: {health_result['health_score']}/100")
            print(f"   - Estado: {health_result['status']}")
            print(f"   - Problemas encontrados: {len(health_result['issues'])}")
            
            for issue in health_result['issues'][:3]:  # Mostrar solo los primeros 3
                print(f"     • {issue}")
        
        print("\n🔍 Prueba 4: Detectar anomalías en abril (mes problemático)")
        print("-" * 50)
        
        anomalies_result = analyzer.detect_anomalies("2024-04-01", "2024-04-30")
        print(f"⚠️  Anomalías detectadas en abril: {anomalies_result['summary']['total_count']}")
        print(f"📊 Distribución por severidad: {anomalies_result['summary']['severity_distribution']}")
        
        # Mostrar anomalías críticas
        critical_anomalies = [a for a in anomalies_result['anomalies'] if a['severity'] == 'CRITICAL']
        print(f"\n🚨 Anomalías críticas ({len(critical_anomalies)}):")
        
        for anomaly in critical_anomalies[:5]:
            timestamp = datetime.fromisoformat(anomaly['timestamp'].replace('Z', '+00:00'))
            anomaly_type = anomaly['type']
            
            if 'value' in anomaly:
                print(f"   • {timestamp.strftime('%m-%d %H:%M')} | {anomaly_type}: {anomaly['value']:.1f}")
            else:
                message = anomaly.get('message', 'N/A')[:50] + "..." if len(anomaly.get('message', '')) > 50 else anomaly.get('message', 'N/A')
                print(f"   • {timestamp.strftime('%m-%d %H:%M')} | {anomaly_type}: {message}")
        
        print("\n🔍 Prueba 5: Comparación día normal vs día problemático")
        print("-" * 50)
        
        # Día normal
        normal_health = analyzer.analyze_system_health("2024-06-15", hours_range=2)
        problem_health = analyzer.analyze_system_health("2024-04-15", hours_range=2)
        
        print(f"📊 Comparación de salud del sistema:")
        print(f"   Día normal (15 junio):      Salud={normal_health['health_score']}/100, Estado={normal_health['status']}")
        print(f"   Día problemático (15 abril): Salud={problem_health['health_score']}/100, Estado={problem_health['status']}")
        
        print(f"\n📈 Diferencia de problemas:")
        print(f"   Día normal: {len(normal_health['issues'])} problemas")
        print(f"   Día problemático: {len(problem_health['issues'])} problemas")
        
        print("\n🔍 Prueba 6: Análisis de componentes más problemáticos")
        print("-" * 50)
        
        error_logs = analyzer.get_application_logs(level="ERROR")
        component_errors = {}
        
        for log in error_logs['logs']:
            component = log['component']
            component_errors[component] = component_errors.get(component, 0) + 1
        
        print("🏗️  Errores por componente:")
        sorted_components = sorted(component_errors.items(), key=lambda x: x[1], reverse=True)
        for component, count in sorted_components:
            print(f"   • {component}: {count} errores")
        
        print("\n✅ ¡Análisis completado exitosamente!")
        print("\n🎯 Resumen de capacidades demostradas:")
        print("   ✓ Análisis de métricas de CPU y memoria")
        print("   ✓ Filtrado y análisis de logs por nivel y componente")
        print("   ✓ Evaluación automática de salud del sistema")
        print("   ✓ Detección de anomalías con umbrales configurables")
        print("   ✓ Comparación de períodos normales vs problemáticos")
        print("   ✓ Análisis estadístico de componentes más problemáticos")
        
        print("\n📦 Para usar con Claude Desktop:")
        print("   1. Instalar: pip install mcp")
        print("   2. Configurar claude_desktop_config.json")
        print("   3. Reiniciar Claude Desktop")
        print("   4. ¡Analizar datos con lenguaje natural!")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()