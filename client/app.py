"""
Aplicación web Flask con HTMX para la interfaz gráfica de la Biblioteca.
Se conecta al servidor ZeroMQ para realizar operaciones.
"""

from flask import Flask, render_template, request
from client.grpc_client import LibraryClient

app = Flask(__name__)

# Cliente gRPC global
grpc_client = LibraryClient()


@app.route("/")
def index():
    """Página principal con las 4 operaciones."""
    return render_template("index.html")


@app.route("/loan-isbn", methods=["POST"])
def loan_isbn():
    """Préstamo de libro por ISBN (HTMX partial)."""
    isbn = request.form.get("isbn", "").strip()
    borrower = request.form.get("borrower", "").strip()
    result = grpc_client.loan_by_isbn(isbn, borrower)
    return render_template("partials/loan_result.html", result=result)


@app.route("/loan-title", methods=["POST"])
def loan_title():
    """Préstamo de libro por título (HTMX partial)."""
    title = request.form.get("title", "").strip()
    borrower = request.form.get("borrower", "").strip()
    result = grpc_client.loan_by_title(title, borrower)
    return render_template("partials/loan_result.html", result=result)


@app.route("/query-isbn", methods=["POST"])
def query_isbn():
    """Consulta de libro por ISBN (HTMX partial)."""
    isbn = request.form.get("isbn", "").strip()
    result = grpc_client.query_by_isbn(isbn)
    return render_template("partials/query_result.html", result=result)


@app.route("/return-isbn", methods=["POST"])
def return_isbn():
    """Devolución de libro por ISBN (HTMX partial)."""
    isbn = request.form.get("isbn", "").strip()
    result = grpc_client.return_by_isbn(isbn)
    return render_template("partials/return_result.html", result=result)


if __name__ == "__main__":
    print("=" * 50)
    print(" Cliente Web de Biblioteca iniciado")
    print(" Abrir en: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
