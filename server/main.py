"""
Punto de entrada del servidor ZeroMQ de la Biblioteca.
Lee host/puerto desde config.json.
"""

import json
import os

from server.library_service import run_service

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    cfg = load_config()
    host = cfg["server"]["host"]
    port = cfg["server"]["port"]
    bind_address = f"tcp://{host}:{port}"

    print("=" * 50)
    print("  Servidor ZeroMQ de Biblioteca")
    print(f"  Dirección: {bind_address}")
    print("=" * 50)
    print()
    run_service(bind_address)


if __name__ == "__main__":
    main()

