#!/usr/bin/env python3
"""
MCP Server Básico - Versión Extensible
Servidor MCP funcional con arquitectura preparada para crecer
"""
import json
import sys
import os
from datetime import datetime, timedelta
import random


class MCPServer:
    """Servidor MCP básico y extensible"""
    
    def __init__(self):
        self.name = "hola-mundo-server"
        self.version = "1.0.0"
        self.tools = self._init_tools()
    
    def _init_tools(self):
        """Inicializar herramientas disponibles"""
        return {
            "hola_mundo": {
                "name": "hola_mundo",
                "description": "Herramienta de saludo simple",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "nombre": {"type": "string", "description": "Nombre para el saludo"}
                    },
                    "additionalProperties": False
                }
            },
            "analizar_tickets": {
                "name": "analizar_tickets",
                "description": "Devuelve tickets de soporte para análisis por parte del LLM",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "cantidad_tickets": {
                            "type": "number",
                            "description": "Cantidad de tickets a generar (por defecto 100)",
                            "default": 1000,
                            "minimum": 1,
                            "maximum": 5000
                        },
                        "dias_atras": {
                            "type": "number", 
                            "description": "Rango de días hacia atrás para generar fechas (por defecto 60)",
                            "default": 60,
                            "minimum": 1,
                            "maximum": 365
                        }
                    },
                    "additionalProperties": False
                }
            }
        }
    
    def handle_initialize(self, params):
        """Manejar inicialización del protocolo MCP"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": self.name, "version": self.version}
        }
    
    def handle_list_tools(self):
        """Listar herramientas disponibles"""
        return {"tools": list(self.tools.values())}
    
    def handle_call_tool(self, params):
        """Ejecutar herramienta especificada"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "hola_mundo":
            return self._call_hola_mundo(arguments)
        elif tool_name == "analizar_tickets":
            return self._call_analizar_tickets(arguments)
        else:
            raise ValueError(f"Herramienta desconocida: {tool_name}")
    
    def _call_hola_mundo(self, arguments):
        """Implementación de la herramienta hola_mundo"""
        nombre = arguments.get("nombre", "Mundo")
        respuesta = {"mensaje": f"Hola {nombre}!", "status": "ok"}
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(respuesta, ensure_ascii=False)
            }]
        }
    
    def _call_analizar_tickets(self, arguments):
        """Implementación de la herramienta analizar_tickets - genera tickets sintéticos"""
        cantidad_tickets = arguments.get("cantidad_tickets", 100)
        dias_atras = arguments.get("dias_atras", 60)
        
        try:
            # Generar tickets sintéticos
            tickets_generados = self._generar_tickets_sinteticos(cantidad_tickets, dias_atras)
            
            # Agregar metadatos útiles
            info_tickets = {
                "metadatos": {
                    "total_tickets": len(tickets_generados),
                    "fecha_generacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "rango_fechas": f"Últimos {dias_atras} días",
                    "tipo_datos": "sintéticos"
                },
                "tickets": tickets_generados
            }
            
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(info_tickets, ensure_ascii=False, indent=2)
                }]
            }
            
        except Exception as e:
            raise ValueError(f"Error generando tickets: {str(e)}")
    
    def _generar_tickets_sinteticos(self, cantidad, dias_atras):
        """Generar tickets de soporte sintéticos"""
        # Configurar semilla para reproducibilidad
        random.seed(42)
        
        # Datos base para generar tickets realistas
        categorias = [
            "Problemas de Facturación",
            "Problemas Técnicos", 
            "Consultas de Cuenta",
            "Solicitudes de Funcionalidades",
            "Problemas de Seguridad"
        ]
        
        prioridades = ["Baja", "Media", "Alta", "Crítica"]
        estados = ["Abierto", "En Progreso", "Pendiente Cliente", "Resuelto", "Cerrado"]
        
        nombres = [
            "Ana Martín", "Luis González", "María García", "Carlos Rodríguez", 
            "Elena López", "José Serrano", "Carmen Ruiz", "Antonio Romero",
            "Isabel Moreno", "Miguel Sánchez", "Patricia Gil", "Francisco Torres",
            "Rosa Navarro", "Manuel Ramos", "Pilar Álvarez", "Juan Jiménez"
        ]
        
        empresas = [
            "TechSoft Solutions", "InnovaCorp", "DataMax Systems", "CloudFirst Ltd",
            "AlphaTech", "BetaSoft", "GammaCorp", "Digital Dynamics",
            "CyberCore", "SmartBiz Pro", "NextGen Analytics", "FutureFlow", "MetaData Inc"
        ]
        
        agentes = [f"Agente{i}" for i in range(1, 16)]
        
        # Plantillas de títulos y descripciones por categoría
        plantillas = {
            "Problemas de Facturación": [
                ("No recibí factura del mes de {mes}", "No recibí factura del mes de {mes}"),
                ("Error en el cálculo del IVA en factura #INV-{num}", "Error en el cálculo del IVA en factura #INV-{num}"),
                ("La factura muestra un importe incorrecto de {amount}€ en lugar de {amount2}€", "La factura muestra un importe incorrecto de {amount}€ en lugar de {amount2}€"),
                ("Cargo duplicado en mi tarjeta de crédito por {amount}€", "Cargo duplicado en mi tarjeta de crédito por {amount}€"),
                ("Diferencia entre lo presupuestado y lo facturado", "Diferencia entre lo presupuestado y lo facturado"),
                ("No puedo descargar mi factura del portal", "No puedo descargar mi factura del portal"),
                ("Error en datos fiscales de la empresa en factura", "Error en datos fiscales de la empresa en factura"),
                ("Facturación por servicios ya cancelados", "Facturación por servicios ya cancelados"),
                ("Descuento prometido no aplicado en factura de {mes}", "Descuento prometido no aplicado en factura de {mes}"),
                ("Factura en moneda incorrecta, debería ser en EUR no USD", "Factura en moneda incorrecta, debería ser en EUR no USD"),
                ("Me cobraron servicios que no contraté", "Me cobraron servicios que no contraté"),
                ("Cobro automático falló pero no recibí notificación", "Cobro automático falló pero no recibí notificación")
            ],
            "Problemas Técnicos": [
                ("No puedo iniciar sesión con mis credenciales", "No puedo iniciar sesión con mis credenciales"),
                ("Error 500 al acceder al dashboard", "Error 500 al acceder al dashboard"),
                ("La aplicación se cierra inesperadamente", "La aplicación se cierra inesperadamente"),
                ("Pérdida de datos después de la actualización", "Pérdida de datos después de la actualización"),
                ("El sistema está muy lento desde ayer", "El sistema está muy lento desde ayer"),
                ("Problema de conectividad con la API", "Problema de conectividad con la API"),
                ("La página web no carga completamente", "La página web no carga completamente"),
                ("Funcionalidad {feature} no responde", "Funcionalidad {feature} no responde"),
                ("Error de certificado SSL en el sitio web", "Error de certificado SSL en el sitio web"),
                ("Los datos no se sincronizan correctamente", "Los datos no se sincronizan correctamente")
            ],
            "Consultas de Cuenta": [
                ("¿Cómo cambio mi plan de suscripción?", "¿Cómo cambio mi plan de suscripción?"),
                ("Necesito actualizar mi información de contacto", "Necesito actualizar mi información de contacto"),
                ("¿Puedo cambiar el email principal de la cuenta?", "¿Puedo cambiar el email principal de la cuenta?"),
                ("¿Cómo recupero mi contraseña?", "¿Cómo recupero mi contraseña?"),
                ("Necesito agregar usuarios adicionales", "Necesito agregar usuarios adicionales"),
                ("Consulta sobre límites de mi plan actual", "Consulta sobre límites de mi plan actual"),
                ("¿Cómo exporto mis datos?", "¿Cómo exporto mis datos?"),
                ("Quiero cancelar mi cuenta", "Quiero cancelar mi cuenta"),
                ("Necesito certificado de usuario activo", "Necesito certificado de usuario activo")
            ],
            "Solicitudes de Funcionalidades": [
                ("¿Cuándo estará disponible la integración con {platform}?", "¿Cuándo estará disponible la integración con {platform}?"),
                ("Solicito funcionalidad de backup automático", "Solicito funcionalidad de backup automático"),
                ("Necesito reportes más detallados", "Necesito reportes más detallados"),
                ("¿Pueden agregar soporte para {tech}?", "¿Pueden agregar soporte para {tech}?"),
                ("Solicito mejora en la interfaz móvil", "Solicito mejora en la interfaz móvil"),
                ("¿Habrá versión en español próximamente?", "¿Habrá versión en español próximamente?"),
                ("Necesito API más robusta para integraciones", "Necesito API más robusta para integraciones"),
                ("¿Pueden mejorar las notificaciones por email?", "¿Pueden mejorar las notificaciones por email?")
            ],
            "Problemas de Seguridad": [
                ("Mi cuenta fue comprometida", "Mi cuenta fue comprometida"),
                ("Sospecho acceso no autorizado a mi cuenta", "Sospecho acceso no autorizado a mi cuenta"),
                ("¿Cómo reporto un posible phishing?", "¿Cómo reporto un posible phishing?"),
                ("Problema con certificados de seguridad", "Problema con certificados de seguridad"),
                ("Necesito habilitar autenticación de dos factores", "Necesito habilitar autenticación de dos factores"),
                ("¿Cómo cambio permisos de usuarios?", "¿Cómo cambio permisos de usuarios?"),
                ("Solicito información sobre encriptación de datos", "Solicito información sobre encriptación de datos"),
                ("Necesito audit log de accesos a mi cuenta", "Necesito audit log de accesos a mi cuenta")
            ]
        }
        
        tickets = []
        fecha_base = datetime.now()
        
        for i in range(1, cantidad + 1):
            # Elegir categoría con distribución realista
            categoria = random.choices(
                categorias, 
                weights=[35, 25, 20, 15, 5],  # Más problemas de facturación, menos de seguridad
                k=1
            )[0]
            
            # Elegir plantilla aleatoria para la categoría
            titulo_template, desc_template = random.choice(plantillas[categoria])
            
            # Rellenar plantillas con datos dinámicos
            titulo = titulo_template.format(
                mes=random.choice(["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]),
                num=random.randint(10000, 99999),
                amount=random.randint(100, 5000),
                amount2=random.randint(100, 5000),
                platform=random.choice(["Slack", "Teams", "Zoom", "Trello"]),
                tech=random.choice(["API", "notificaciones", "webhooks"]),
                feature=random.choice(["dashboard", "reportes", "API"])
            )
            
            descripcion = desc_template.format(
                mes=random.choice(["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]),
                num=random.randint(10000, 99999),
                amount=random.randint(100, 5000),
                amount2=random.randint(100, 5000),
                platform=random.choice(["Slack", "Teams", "Zoom", "Trello"]),
                tech=random.choice(["API", "notificaciones", "webhooks"]),
                feature=random.choice(["dashboard", "reportes", "API"])
            )
            
            # Generar fecha aleatoria en el rango especificado
            dias_random = random.randint(0, dias_atras)
            fecha_ticket = fecha_base - timedelta(days=dias_random)
            
            # Prioridad basada en categoría
            if categoria == "Problemas de Seguridad":
                prioridad = random.choice(["Alta", "Crítica"])
            elif categoria == "Problemas de Facturación":
                prioridad = random.choices(["Media", "Alta", "Crítica"], weights=[30, 50, 20])[0]
            else:
                prioridad = random.choice(prioridades)
            
            ticket = {
                "id": f"TICK-{i:05d}",
                "fecha_creacion": fecha_ticket.strftime('%Y-%m-%d %H:%M:%S'),
                "categoria": categoria,
                "prioridad": prioridad,
                "estado": random.choice(estados),
                "titulo": titulo,
                "descripcion": descripcion,
                "cliente": {
                    "nombre": random.choice(nombres),
                    "empresa": random.choice(empresas),
                    "email": f"{random.choice(nombres).lower().replace(' ', '.')}@{random.choice(empresas).lower().replace(' ', '').replace('.', '').replace(',', '')}.com"
                },
                "tiempo_resolucion_horas": random.choice([None, random.randint(1, 168)]),
                "satisfaccion_cliente": random.choice([None, random.randint(1, 5)]),
                "agente_asignado": random.choice(agentes)
            }
            
            tickets.append(ticket)
        
        # Ordenar por fecha de creación (más recientes primero)
        tickets.sort(key=lambda x: x["fecha_creacion"], reverse=True)
        
        return tickets
    
    def process_message(self, message):
        """Procesar mensaje entrante y generar respuesta"""
        method = message.get("method")
        params = message.get("params", {})
        msg_id = message.get("id")
        
        try:
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_list_tools()
            elif method == "tools/call":
                result = self.handle_call_tool(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            response = {"jsonrpc": "2.0", "result": result}
            if msg_id is not None:
                response["id"] = msg_id
                
            return response
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def run(self):
        """Ejecutar el servidor MCP"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                message = json.loads(line.strip())
                response = self.process_message(message)
                
                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception:
                # Error crítico - salir del loop
                break


def main():
    """Función principal"""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()