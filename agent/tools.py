# agent/tools.py — Herramientas del agente para TAPITAOCA
# Generado por AgentKit

"""
Herramientas específicas del negocio de TAPITAOCA.
Estas funciones pueden extender las capacidades del agente en el futuro.
"""

import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atención del negocio."""
    info = cargar_info_negocio()
    return {
        "horario": info.get("negocio", {}).get("horario", "6:00 AM a 9:00 PM"),
        "esta_abierto": True,  # TODO: calcular según hora actual y horario
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca información relevante en los archivos de /knowledge.
    Retorna el contenido más relevante encontrado.
    """
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                # Búsqueda simple por coincidencia de texto
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."


# ════════════════════════════════════════════════════════════
# HERRAMIENTAS ESPECÍFICAS PARA TAPITAOCA
# ════════════════════════════════════════════════════════════

def obtener_menu() -> dict:
    """Retorna información del menú para futuras expansiones."""
    return {
        "desayunos": "Disponibles de 6:00 AM a 12:00 PM",
        "salados": "Disponibles de 12:00 PM a 9:00 PM",
        "dulces": "Disponibles todo el día",
        "bebidas": "Disponibles todo el día",
    }


def registrar_preferencias_cliente(telefono: str, preferencias: dict) -> bool:
    """
    Registra preferencias del cliente para futuras compras.
    Esto puede expandirse en el futuro con una base de datos dedicada.
    """
    logger.info(f"Preferencias registradas para {telefono}: {preferencias}")
    return True


# Nota: Las herramientas avanzadas como agendar citas, gestión de inventario,
# integración con sistema de pagos, etc., se pueden agregar en futuras versiones.
# Por ahora, Tapi se enfoca en tomar pedidos conversacionales y responder preguntas.
