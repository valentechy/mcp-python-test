import json
import random
from datetime import datetime, timedelta

def generar_tickets_soporte():
    """Generar miles de tickets de soporte de ejemplo"""
    
    # Categorías principales y sus subcategorías
    categorias = {
        "Problemas de Facturación": [
            "Cargo duplicado en mi tarjeta de crédito por {amount}€",
            "No recibí factura del mes de {month}",
            "Error en el cálculo del IVA en factura #{invoice_num}",
            "Me cobraron servicios que no contraté",
            "La factura muestra un importe incorrecto de {amount}€ en lugar de {correct_amount}€",
            "No puedo descargar mi factura del portal",
            "Diferencia entre lo presupuestado y lo facturado",
            "Cobro automático falló pero no recibí notificación",
            "Facturación por servicios ya cancelados",
            "Error en datos fiscales de la empresa en factura",
            "Descuento prometido no aplicado en factura de {month}",
            "Factura en moneda incorrecta, debería ser en EUR no USD"
        ],
        "Problemas Técnicos": [
            "La aplicación se cierra inesperadamente",
            "No puedo iniciar sesión con mis credenciales",
            "Error 500 al acceder al dashboard",
            "Los datos no se sincronizan correctamente",
            "Problema de conectividad con la API",
            "La página web no carga completamente",
            "Funcionalidad {feature} no responde",
            "Pérdida de datos después de la actualización",
            "Error de certificado SSL en el sitio web",
            "El sistema está muy lento desde ayer"
        ],
        "Consultas de Cuenta": [
            "¿Cómo cambio mi plan de suscripción?",
            "Necesito actualizar mi información de contacto",
            "Quiero cancelar mi cuenta",
            "¿Cómo recupero mi contraseña?",
            "Necesito agregar usuarios adicionales",
            "¿Puedo cambiar el email principal de la cuenta?",
            "Consulta sobre límites de mi plan actual",
            "¿Cómo exporto mis datos?",
            "Necesito certificado de usuario activo"
        ],
        "Solicitudes de Funcionalidades": [
            "¿Cuándo estará disponible la integración con {service}?",
            "Necesito reportes más detallados",
            "¿Pueden agregar soporte para {feature}?",
            "Solicito mejora en la interfaz móvil",
            "¿Habrá versión en español próximamente?",
            "Necesito API más robusta para integraciones",
            "Solicito funcionalidad de backup automático",
            "¿Pueden mejorar las notificaciones por email?"
        ],
        "Problemas de Seguridad": [
            "Sospecho acceso no autorizado a mi cuenta",
            "Necesito habilitar autenticación de dos factores",
            "¿Cómo reporto un posible phishing?",
            "Mi cuenta fue comprometida",
            "Necesito audit log de accesos a mi cuenta",
            "¿Cómo cambio permisos de usuarios?",
            "Solicito información sobre encriptación de datos",
            "Problema con certificados de seguridad"
        ]
    }
    
    # Niveles de prioridad
    prioridades = {
        "Problemas de Facturación": ["Alta", "Crítica", "Media", "Alta", "Crítica"],
        "Problemas Técnicos": ["Alta", "Crítica", "Media", "Baja"],
        "Consultas de Cuenta": ["Media", "Baja", "Media"],
        "Solicitudes de Funcionalidades": ["Baja", "Media"],
        "Problemas de Seguridad": ["Crítica", "Alta", "Crítica"]
    }
    
    estados = ["Abierto", "En Progreso", "Resuelto", "Cerrado", "Pendiente Cliente"]
    
    nombres = [
        "María García", "Carlos Rodríguez", "Ana Martín", "Luis González", 
        "Elena López", "Miguel Sánchez", "Carmen Ruiz", "Francisco Torres",
        "Isabel Moreno", "Juan Jiménez", "Pilar Álvarez", "Antonio Romero",
        "Rosa Navarro", "Manuel Ramos", "Patricia Gil", "José Serrano"
    ]
    
    empresas = [
        "TechSoft Solutions", "InnovaCorp", "DataMax Systems", "CloudFirst Ltd",
        "NextGen Analytics", "SmartBiz Pro", "Digital Dynamics", "FutureFlow",
        "MetaData Inc", "CyberCore", "AlphaTech", "BetaSoft", "GammaCorp"
    ]
    
    tickets = []
    
    # Generar fecha base (último mes)
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    for i in range(1, 2501):  # Generar 2500 tickets
        # Seleccionar categoría con distribución realista
        categoria_pesos = [0.35, 0.25, 0.20, 0.12, 0.08]  # Facturación tiene más peso
        categoria = random.choices(list(categorias.keys()), weights=categoria_pesos)[0]
        
        # Generar fecha aleatoria en el último mes
        dias_random = random.randint(0, 30)
        fecha_ticket = fecha_inicio + timedelta(days=dias_random)
        
        # Seleccionar descripción y rellenar variables si es necesario
        descripcion_base = random.choice(categorias[categoria])
        descripcion = descripcion_base.format(
            amount=random.randint(50, 5000),
            correct_amount=random.randint(50, 5000),
            month=random.choice(["Enero", "Febrero", "Marzo", "Abril", "Mayo"]),
            invoice_num=f"INV-{random.randint(10000, 99999)}",
            service=random.choice(["Salesforce", "HubSpot", "Slack", "Zoom"]),
            feature=random.choice(["dashboard", "reportes", "API", "notificaciones"])
        )
        
        # Crear ticket
        ticket = {
            "id": f"TICK-{i:05d}",
            "fecha_creacion": fecha_ticket.strftime("%Y-%m-%d %H:%M:%S"),
            "categoria": categoria,
            "prioridad": random.choice(prioridades[categoria]),
            "estado": random.choice(estados),
            "titulo": descripcion[:60] + "..." if len(descripcion) > 60 else descripcion,
            "descripcion": descripcion,
            "cliente": {
                "nombre": random.choice(nombres),
                "empresa": random.choice(empresas),
                "email": f"{random.choice(nombres).lower().replace(' ', '.')}@{random.choice(empresas).lower().replace(' ', '')}.com"
            },
            "tiempo_resolucion_horas": random.randint(1, 168) if random.random() > 0.3 else None,
            "satisfaccion_cliente": random.randint(1, 5) if random.random() > 0.4 else None,
            "agente_asignado": f"Agente{random.randint(1, 15)}"
        }
        
        tickets.append(ticket)
    
    return tickets

def main():
    print("🎫 Generando tickets de soporte...")
    tickets = generar_tickets_soporte()
    
    # Guardar en archivo JSON
    with open('tickets_soporte.json', 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generados {len(tickets)} tickets de soporte")
    
    # Mostrar estadísticas rápidas
    categorias_count = {}
    facturacion_urgentes = []
    
    for ticket in tickets:
        cat = ticket['categoria']
        categorias_count[cat] = categorias_count.get(cat, 0) + 1
        
        # Recopilar tickets urgentes de facturación
        if cat == "Problemas de Facturación" and ticket['prioridad'] in ['Alta', 'Crítica']:
            facturacion_urgentes.append(ticket)
    
    print("\n📊 Distribución por categorías:")
    total = len(tickets)
    for categoria, count in sorted(categorias_count.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (count / total) * 100
        print(f"  {categoria}: {count} tickets ({porcentaje:.1f}%)")
    
    print(f"\n🚨 Tickets urgentes de facturación: {len(facturacion_urgentes)}")
    print("\n📋 Ejemplos de quejas urgentes de facturación:")
    for i, ticket in enumerate(facturacion_urgentes[:3], 1):
        print(f"{i}. [{ticket['prioridad']}] {ticket['descripcion']}")
    
    print(f"\n💾 Archivo 'tickets_soporte.json' creado con éxito")

if __name__ == "__main__":
    main()