#!/usr/bin/env python3
"""
Servidor MCP para monitoreo de aplicación de pagos
Proporciona herramientas para analizar métricas, logs y estado de la base de datos
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import argparse
import sys

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


class PaymentMonitoringServer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.server = Server("payment-monitoring")
        self._setup_tools()
    
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
    
    def _setup_tools(self):
        """Configura las herramientas disponibles en el servidor MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="get_system_metrics",
                    description="Obtiene métricas del sistema (CPU y memoria) para un rango de fechas específico",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Fecha de inicio en formato YYYY-MM-DD (opcional)"
                            },
                            "end_date": {
                                "type": "string", 
                                "description": "Fecha de fin en formato YYYY-MM-DD (opcional)"
                            },
                            "metric_type": {
                                "type": "string",
                                "enum": ["cpu_usage", "memory_usage", "both"],
                                "description": "Tipo de métrica a obtener (por defecto: both)"
                            }
                        },
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="get_application_logs",
                    description="Obtiene logs de la aplicación filtrados por nivel, componente o rango de fechas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Fecha de inicio en formato YYYY-MM-DD (opcional)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "Fecha de fin en formato YYYY-MM-DD (opcional)"
                            },
                            "level": {
                                "type": "string",
                                "enum": ["INFO", "WARN", "ERROR", "CRITICAL"],
                                "description": "Nivel de log a filtrar (opcional)"
                            },
                            "component": {
                                "type": "string",
                                "description": "Componente específico a filtrar (opcional)"
                            }
                        },
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="get_database_status",
                    description="Obtiene métricas de estado de la base de datos para un rango de fechas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Fecha de inicio en formato YYYY-MM-DD (opcional)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "Fecha de fin en formato YYYY-MM-DD (opcional)"
                            },
                            "metric_name": {
                                "type": "string",
                                "enum": ["connection_count", "query_response_time", "active_transactions", "disk_usage"],
                                "description": "Métrica específica de DB a obtener (opcional, por defecto todas)"
                            }
                        },
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="analyze_system_health",
                    description="Analiza la salud general del sistema en un período específico",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Fecha específica a analizar en formato YYYY-MM-DD"
                            },
                            "hours_range": {
                                "type": "integer",
                                "description": "Número de horas alrededor de la fecha a analizar (por defecto: 2)",
                                "default": 2
                            }
                        },
                        "required": ["date"],
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="detect_anomalies",
                    description="Detecta anomalías en el sistema basándose en umbrales predefinidos",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Fecha de inicio para la detección (opcional)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "Fecha de fin para la detección (opcional)"
                            }
                        },
                        "additionalProperties": False
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent]:
            if arguments is None:
                arguments = {}
                
            try:
                if name == "get_system_metrics":
                    result = await self._get_system_metrics(**arguments)
                elif name == "get_application_logs":
                    result = await self._get_application_logs(**arguments)
                elif name == "get_database_status":
                    result = await self._get_database_status(**arguments)
                elif name == "analyze_system_health":
                    result = await self._analyze_system_health(**arguments)
                elif name == "detect_anomalies":
                    result = await self._detect_anomalies(**arguments)
                else:
                    raise ValueError(f"Herramienta desconocida: {name}")
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
            except Exception as e:
                error_msg = f"Error ejecutando {name}: {str(e)}"
                return [types.TextContent(type="text", text=error_msg)]
    
    def _parse_date(self, date_str: str) -> datetime:
        """Convierte string de fecha a objeto datetime"""
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    
    def _filter_by_date_range(self, data: List[Dict], start_date: Optional[str], end_date: Optional[str]) -> List[Dict]:
        """Filtra datos por rango de fechas"""
        if not start_date and not end_date:
            return data
        
        filtered_data = []
        for item in data:
            item_date = self._parse_date(item['timestamp'])
            
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
    
    async def _get_system_metrics(self, start_date: Optional[str] = None, 
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
    
    async def _get_application_logs(self, start_date: Optional[str] = None,
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
    
    async def _get_database_status(self, start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 metric_name: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene estado de la base de datos"""
        db_data = self._load_json_file("db.json")
        
        filtered_metrics = self._filter_by_date_range(db_data["database_metrics"], start_date, end_date)
        
        if metric_name:
            filtered_metrics = [metric for metric in filtered_metrics if metric["metric"] == metric_name]
        
        # Agrupar métricas por tipo
        grouped_metrics = {}
        for metric in filtered_metrics:
            metric_type = metric["metric"]
            if metric_type not in grouped_metrics:
                grouped_metrics[metric_type] = []
            grouped_metrics[metric_type].append(metric)
        
        # Calcular estadísticas
        summary = {}
        for metric_type, values in grouped_metrics.items():
            metric_values = [item["value"] for item in values]
            if metric_values:
                summary[metric_type] = {
                    "avg": sum(metric_values) / len(metric_values),
                    "max": max(metric_values),
                    "min": min(metric_values),
                    "count": len(metric_values)
                }
        
        return {
            "metrics": grouped_metrics,
            "summary": summary
        }
    
    async def _analyze_system_health(self, date: str, hours_range: int = 2) -> Dict[str, Any]:
        """Analiza la salud del sistema en una fecha específica"""
        target_date = datetime.fromisoformat(date)
        start_time = target_date - timedelta(hours=hours_range)
        end_time = target_date + timedelta(hours=hours_range)
        
        start_str = start_time.strftime("%Y-%m-%d")
        end_str = end_time.strftime("%Y-%m-%d")
        
        # Obtener datos de todas las fuentes
        metrics = await self._get_system_metrics(start_str, end_str)
        logs = await self._get_application_logs(start_str, end_str)
        db_status = await self._get_database_status(start_str, end_str)
        
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
        
        # Verificar base de datos
        if "query_response_time" in db_status["summary"]:
            avg_response = db_status["summary"]["query_response_time"]["avg"]
            if avg_response > 1000:  # más de 1 segundo
                health_score -= 25
                issues.append(f"Respuesta DB lenta: {avg_response:.0f}ms")
        
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
            "logs_summary": logs["summary"],
            "db_summary": db_status["summary"]
        }
    
    async def _detect_anomalies(self, start_date: Optional[str] = None,
                              end_date: Optional[str] = None) -> Dict[str, Any]:
        """Detecta anomalías en el sistema"""
        anomalies = []
        
        # Obtener métricas del sistema
        metrics = await self._get_system_metrics(start_date, end_date)
        
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
        logs = await self._get_application_logs(start_date, end_date, level="CRITICAL")
        for log in logs["logs"]:
            anomalies.append({
                "timestamp": log["timestamp"],
                "type": "CRITICAL_LOG",
                "message": log["message"],
                "component": log["component"],
                "severity": "CRITICAL"
            })
        
        # Obtener logs de error
        error_logs = await self._get_application_logs(start_date, end_date, level="ERROR")
        for log in error_logs["logs"]:
            anomalies.append({
                "timestamp": log["timestamp"],
                "type": "ERROR_LOG", 
                "message": log["message"],
                "component": log["component"],
                "severity": "HIGH"
            })
        
        # Detectar anomalías de base de datos
        db_status = await self._get_database_status(start_date, end_date)
        if "query_response_time" in db_status["metrics"]:
            for metric in db_status["metrics"]["query_response_time"]:
                if metric["value"] > 1000:  # > 1 segundo
                    anomalies.append({
                        "timestamp": metric["timestamp"],
                        "type": "SLOW_DB_QUERY",
                        "value": metric["value"],
                        "threshold": 1000,
                        "severity": "CRITICAL" if metric["value"] > 5000 else "HIGH"
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
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="payment-monitoring",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities()
                )
            )


async def main():
    parser = argparse.ArgumentParser(description="Servidor MCP para monitoreo de aplicación de pagos")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path.cwd(),
        help="Directorio que contiene los archivos de datos JSON (por defecto: directorio actual)"
    )
    
    args = parser.parse_args()
    
    if not args.data_dir.exists():
        print(f"Error: El directorio {args.data_dir} no existe", file=sys.stderr)
        sys.exit(1)
    
    # Verificar que existan los archivos necesarios
    required_files = ["metricas.json", "logs.json", "db.json"]
    for filename in required_files:
        if not (args.data_dir / filename).exists():
            print(f"Error: No se encontró el archivo {filename} en {args.data_dir}", file=sys.stderr)
            sys.exit(1)
    
    server = PaymentMonitoringServer(args.data_dir)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())