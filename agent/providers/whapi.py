# agent/providers/whapi.py — Adaptador para Whapi.cloud
# Generado por AgentKit para TAPITAOCA

import os
import logging
import httpx
from fastapi import Request
from agent.providers.base import ProveedorWhatsApp, MensajeEntrante

logger = logging.getLogger("agentkit")


class ProveedorWhapi(ProveedorWhatsApp):
    """Proveedor de WhatsApp usando Whapi.cloud (REST API simple)."""

    def __init__(self):
        self.token = os.getenv("WHAPI_TOKEN")
        self.url_envio = "https://gate.whapi.cloud/messages/text"

    async def parsear_webhook(self, request: Request) -> list[MensajeEntrante]:
        """Parsea el payload de Whapi.cloud."""
        try:
            body = await request.json()
        except:
            return []

        mensajes = []
        for msg in body.get("messages", []):
            # Ignorar mensajes sin texto
            texto = msg.get("text", {})
            if isinstance(texto, dict):
                texto = texto.get("body", "")

            if not texto:
                continue

            mensajes.append(MensajeEntrante(
                telefono=msg.get("chat_id", "").replace("@s.whatsapp.net", ""),
                texto=str(texto).strip(),
                mensaje_id=msg.get("id", ""),
                es_propio=msg.get("from_me", False),
            ))
        return mensajes

    async def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        """Envía mensaje via Whapi.cloud."""
        if not self.token:
            logger.warning("WHAPI_TOKEN no configurado — mensaje no enviado")
            return False

        # Normalizar número de teléfono
        if "@s.whatsapp.net" in telefono:
            telefono = telefono.replace("@s.whatsapp.net", "")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    self.url_envio,
                    json={"to": telefono, "body": mensaje},
                    headers=headers,
                )
                if r.status_code != 200:
                    logger.error(f"Error Whapi: {r.status_code} — {r.text}")
                    return False
                return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje con Whapi: {e}")
            return False
