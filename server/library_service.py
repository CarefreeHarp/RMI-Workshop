"""
Servicio de Biblioteca sobre ZeroMQ.
Recibe peticiones JSON por un socket REP y responde con JSON.
"""

import json
import zmq
from server.db import (
    get_book_by_isbn,
    loan_book,
    loan_book_by_title,
    return_book,
)


# Acciones soportadas
ACTIONS = {
    "Prestamo por ISBN",
    "Prestamo por Titulo",
    "Consulta por ISBN",
    "Devolucion por ISBN",
}


def handle_request(message: dict) -> dict:
    """Despacha una petición JSON al handler correspondiente."""
    action = message.get("action")

    if action not in ACTIONS:
        return {"success": False, "message": f"Acción desconocida: {action}"}

    if action == "Prestamo por ISBN":
        return _loan_by_isbn(message)
    elif action == "Prestamo por Titulo":
        return _loan_by_title(message)
    elif action == "Consulta por ISBN":
        return _query_by_isbn(message)
    elif action == "Devolucion por ISBN":
        return _return_by_isbn(message)


def _loan_by_isbn(msg: dict) -> dict:
    isbn = msg.get("isbn", "").strip()
    borrower = msg.get("borrower", "").strip()

    if not isbn:
        return {"success": False, "message": "El ISBN es requerido."}
    if not borrower:
        return {"success": False, "message": "El nombre del prestatario es requerido."}

    success, message, book_data = loan_book(isbn, borrower)
    result = {"success": success, "message": message}
    if book_data:
        result["book"] = book_data
    return result


def _loan_by_title(msg: dict) -> dict:
    title = msg.get("title", "").strip()
    borrower = msg.get("borrower", "").strip()

    if not title:
        return {"success": False, "message": "El título es requerido."}
    if not borrower:
        return {"success": False, "message": "El nombre del prestatario es requerido."}

    success, message, book_data = loan_book_by_title(title, borrower)
    result = {"success": success, "message": message}
    if book_data:
        result["book"] = book_data
    return result


def _query_by_isbn(msg: dict) -> dict:
    isbn = msg.get("isbn", "").strip()

    if not isbn:
        return {"found": False, "message": "El ISBN es requerido."}

    book_data = get_book_by_isbn(isbn)
    if book_data:
        return {
            "found": True,
            "message": f"Libro encontrado: '{book_data['titulo']}'",
            "book": book_data,
        }
    else:
        return {"found": False, "message": f"No se encontró un libro con ISBN: {isbn}"}


def _return_by_isbn(msg: dict) -> dict:
    isbn = msg.get("isbn", "").strip()

    if not isbn:
        return {"success": False, "message": "El ISBN es requerido."}

    success, message = return_book(isbn)
    return {"success": success, "message": message}


def run_service(bind_address: str = "tcp://*:5555"):
    """Inicia el loop del servicio ZMQ (socket REP)."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(bind_address)

    print(f"  Servicio ZMQ escuchando en: {bind_address}")
    print("  Esperando peticiones...\n")

    try:
        while True:
            # Recibir petición JSON
            raw = socket.recv()
            try:
                request = json.loads(raw.decode("utf-8"))
                print(f"  ← Petición recibida: {request.get('action', '?')}")
                response = handle_request(request)
            except json.JSONDecodeError:
                response = {"success": False, "message": "JSON inválido."}
            except Exception as e:
                response = {"success": False, "message": f"Error interno: {str(e)}"}

            # Enviar respuesta JSON
            socket.send(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            print(f"  → Respuesta enviada: {'OK' if response.get('success') or response.get('found') else 'ERROR'}")
    except KeyboardInterrupt:
        print("\n  Deteniendo servicio...")
    finally:
        socket.close()
        context.term()
        print("  Servicio detenido.")

