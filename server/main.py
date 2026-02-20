"""
Punto de entrada del servidor ZeroMQ de la Biblioteca.
Inicia el servicio en tcp://*:5555.
"""

from server.library_service import run_service


def main():
    print("=" * 50)
    print("  Servidor ZeroMQ de Biblioteca")
    print("  Puerto: 5555")
    print("=" * 50)
    print()
    run_service("tcp://*:5555")


if __name__ == "__main__":
    main()

