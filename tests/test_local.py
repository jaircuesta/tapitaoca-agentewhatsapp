# tests/test_local.py — Simulador de chat en terminal
# Generado por AgentKit para TAPITAOCA

"""
Prueba tu agente Tapi sin necesitar WhatsApp.
Simula una conversación en la terminal.
"""

import asyncio
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial, limpiar_historial

TELEFONO_TEST = "test-local-001"


async def main():
    """Loop principal del chat de prueba."""
    await inicializar_db()

    print()
    print("=" * 60)
    print("   🌟 TAPITAOCA — Test Local de Tapi 🌟")
    print("=" * 60)
    print()
    print("  Escribe mensajes como si fueras un cliente.")
    print("  Tapi responderá como lo haría con tus clientes reales.")
    print()
    print("  Comandos especiales:")
    print("    'limpiar'  — borra el historial de conversación")
    print("    'salir'    — termina el test")
    print()
    print("-" * 60)
    print()

    while True:
        try:
            mensaje = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n✅ Test finalizado. ¡Gracias por probar Tapi!")
            break

        if not mensaje:
            continue

        if mensaje.lower() == "salir":
            print("\n✅ Test finalizado. ¡Gracias por probar Tapi!")
            break

        if mensaje.lower() == "limpiar":
            await limpiar_historial(TELEFONO_TEST)
            print("[✨ Historial borrado]\n")
            continue

        # Obtener historial ANTES de guardar (brain.py agrega el mensaje actual)
        historial = await obtener_historial(TELEFONO_TEST)

        # Generar respuesta
        print("\nTapi: ", end="", flush=True)
        respuesta = await generar_respuesta(mensaje, historial)
        print(respuesta)
        print()

        # Guardar mensaje del usuario y respuesta del agente
        await guardar_mensaje(TELEFONO_TEST, "user", mensaje)
        await guardar_mensaje(TELEFONO_TEST, "assistant", respuesta)


if __name__ == "__main__":
    asyncio.run(main())
