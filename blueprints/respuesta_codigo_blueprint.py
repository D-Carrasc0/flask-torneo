from flask import Blueprint, request, jsonify
import sys
import io

respuesta_codigo_bp = Blueprint('respuesta_codigo_bp', __name__)

@respuesta_codigo_bp.route('/probar_codigo', methods=['POST'])
def probar_codigo():
    data = request.get_json()
    codigo = data.get('codigo', '')

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = io.StringIO()
    sys.stderr = mystderr = io.StringIO()

    exito = True
    try:
        exec(codigo, {})
    except Exception as e:
        exito = False
        print(f"Error: {e}")

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    salida = mystdout.getvalue() + mystderr.getvalue()
    return jsonify({"salida": salida, "exito": exito})