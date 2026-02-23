"""
Cliente ZeroMQ para el servicio de Biblioteca.
Encapsula la comunicación con el servidor ZMQ usando patrón REQ-REP.
"""

import json
import zmq


class LibraryClient:
    """Cliente que se conecta al servidor ZMQ de la biblioteca."""

    def __init__(self, server_address: str = "tcp://localhost:5555"):
        self.server_address = server_address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server_address)
        # Timeout de 10 segundos para evitar bloqueos indefinidos
        self.socket.setsockopt(zmq.RCVTIMEO, 10000)
        self.socket.setsockopt(zmq.SNDTIMEO, 10000)

    def close(self):
        """Cierra el socket y el contexto ZMQ."""
        self.socket.close()
        self.context.term()

    def _send_request(self, request: dict) -> dict:
        """Envía una petición JSON y espera la respuesta."""
        try:
            self.socket.send(json.dumps(request, ensure_ascii=False).encode("utf-8"))
            raw = self.socket.recv()
            return json.loads(raw.decode("utf-8"))
        except zmq.Again:
            return {"success": False, "found": False, "message": "Timeout: el servidor no respondió a tiempo."}
        except zmq.ZMQError as e:
            return {"success": False, "found": False, "message": f"Error de conexión ZMQ: {str(e)}"}
        except Exception as e:
            return {"success": False, "found": False, "message": f"Error inesperado: {str(e)}"}

    def loan_by_isbn(self, isbn: str, borrower: str) -> dict:
        """Solicita préstamo de un libro por ISBN."""
        return self._send_request({
            "action": "Prestamo por ISBN",
            "isbn": isbn,
            "borrower": borrower,
        })

    def loan_by_title(self, title: str, borrower: str) -> dict:
        """Solicita préstamo de un libro por título."""
        return self._send_request({
            "action": "Prestamo por Titulo",
            "title": title,
            "borrower": borrower,
        })

    def query_by_isbn(self, isbn: str) -> dict:
        """Consulta un libro por ISBN."""
        return self._send_request({
            "action": "Consulta por ISBN",
            "isbn": isbn,
        })

    def return_by_isbn(self, isbn: str) -> dict:
        """Devuelve un libro por ISBN."""
        return self._send_request({
            "action": "Devolucion por ISBN",
            "isbn": isbn,
        })

