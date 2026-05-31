from flask import Flask, render_template_string, request
import random
import string

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Contraseñas Avanzado</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 650px; margin: 40px auto; padding: 20px; background-color: #f0f2f5; color: #333; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 25px; }
        h2 { margin-top: 0; color: #1a73e8; border-bottom: 2px solid #e8f0fe; padding-bottom: 10px; }
        
        /* Estilos base de inputs */
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        input[type="text"]:focus, input[type="password"]:focus { border-color: #1a73e8; outline: none; }
        
        /* Contenedor relativo para posicionar el botón dentro del input */
        .input-group { position: relative; margin: 10px 0 20px 0; }
        .input-group input { margin: 0; padding-right: 85px; /* Evita que el texto se empalme con el botón */ }
        
        /* Botón de alternancia de visibilidad */
        .toggle-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: transparent; color: #5f6368; border: none; padding: 5px 10px; width: auto; font-size: 14px; font-weight: 500; cursor: pointer; transition: color 0.2s; }
        .toggle-btn:hover { background: transparent; color: #1a73e8; }

        button.btn-main { background-color: #1a73e8; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; transition: background 0.2s; }
        button.btn-main:hover { background-color: #1557b0; }
        .hidden { display: none !important; }
        
        .pass-list { background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #1a73e8; margin-top: 15px; }
        .pass-item { font-family: 'Courier New', Courier, monospace; font-size: 18px; font-weight: bold; color: #202124; margin: 10px 0; letter-spacing: 1px; word-break: break-all; }
        .req-list { font-size: 14px; list-style-type: none; padding-left: 0; margin-bottom: 20px; }
        .req-list li { margin: 6px 0; padding-left: 20px; position: relative; }
        .req-list li::before { content: "✕"; position: absolute; left: 0; color: #d93025; font-weight: bold; }
        .req-list li.valid::before { content: "✓"; color: #1e7e34; }
        .valid { color: #1e7e34; font-weight: 500; }
        .invalid { color: #d93025; }
        #btnSubmit { background-color: #28a745; margin-top: 15px; }
        #btnSubmit:hover { background-color: #218838; }
        
        .gen-input { margin: 10px 0 20px 0 !important; }
    </style>
</head>
<body>

    <div class="card">
        <h2>Generador de Contraseñas Inteligente</h2>
        <p>Introduce de 1 a 3 palabras o frases para transformarlas con el método de sustitución e intercalado dinámico:</p>
        <form method="POST" action="/">
            <input type="text" class="gen-input" name="frases" placeholder="Ej: Tiger, Lily, Runs" required value="{{ request.form.get('frases', '') }}">
            <button type="submit" class="btn-main">Generar 3 Sugerencias Seguras</button>
        </form>

        {% if passwords %}
            <h3>Sugerencias Generadas:</h3>
            <div class="pass-list">
                {% for pwd in passwords %}
                    <div class="pass-item">{{ pwd }}</div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <div class="card">
        <h2>Validador de Seguridad en Tiempo Real</h2>
        <p>Introduce una contraseña para verificar si cumple los requisitos estructurales estrictos:</p>
        
        <!-- Implementación del grupo de entrada con botón de visibilidad -->
        <div class="input-group">
            <input type="password" id="passInput" placeholder="Escribe tu contraseña aquí..." onkeyup="validatePassword()">
            <button type="button" id="toggleBtn" class="toggle-btn" onclick="togglePasswordVisibility()">Mostrar</button>
        </div>
        
        <ul class="req-list">
            <li id="req-len">Mínimo 12 caracteres</li>
            <li id="req-upp">Letras mayúsculas (A-Z)</li>
            <li id="req-low">Letras minúsculas (a-z)</li>
            <li id="req-num">Números (0-9)</li>
            <li id="req-sym">Símbolos (!, @, #, $, %, etc.)</li>
        </ul>

        <button id="btnSubmit" class="btn-main hidden" onclick="alert('Acceso concedido de forma segura.')">Ingresar al Sistema</button>
    </div>

    <script>
    
        function validatePassword() {
            const pwd = document.getElementById('passInput').value;
            const btn = document.getElementById('btnSubmit');
            
            const isLen = pwd.length >= 12;
            const isUpp = /[A-Z]/.test(pwd);
            const isLow = /[a-z]/.test(pwd);
            const isNum = /[0-9]/.test(pwd);
            const isSym = /[\\W_]/.test(pwd);
            # const isSym = /[\W_]/.test(pwd);

            updateStatus('req-len', isLen);
            updateStatus('req-upp', isUpp);
            updateStatus('req-low', isLow);
            updateStatus('req-num', isNum);
            updateStatus('req-sym', isSym);

            if(isLen && isUpp && isLow && isNum && isSym) {
                btn.classList.remove('hidden');
            } else {
                btn.classList.add('hidden');
            }
        }

        function updateStatus(elementId, isValid) {
            const el = document.getElementById(elementId);
            if(isValid) {
                el.className = 'valid';
            } else {
                el.className = 'invalid';
            }
        }

        // Función nativa para alternar el atributo de tipo del input
        function togglePasswordVisibility() {
            const pwdInput = document.getElementById('passInput');
            const toggleBtn = document.getElementById('toggleBtn');
            
            if (pwdInput.type === 'password') {
                pwdInput.type = 'text';
                toggleBtn.textContent = 'Ocultar';
            } else {
                pwdInput.type = 'password';
                toggleBtn.textContent = 'Mostrar';
            }
        }
    </script>
</body>
</html>
"""

def aplicar_leet_y_alternancia(palabra, variante):
    mapas = [
        {'i': '!', 'I': '!', 'e': '3', 'E': '3', 'a': '@', 'A': '@', 'o': '0', 'O': '0', 's': '$', 'S': '$', 't': '7', 'T': '7'},
        {'i': '1', 'I': '1', 'e': '3', 'E': '3', 'a': '4', 'A': '4', 'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '!', 'T': '!'},
        {'i': '!', 'I': '!', 'e': '3', 'E': '3', 'a': '@', 'A': '@', 'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7'}
    ]
    
    m = mapas[variante % len(mapas)]
    resultado = []
    
    for idx, char in enumerate(palabra):
        if char in m:
            resultado.append(m[char])
        else:
            if idx == len(palabra) - 1 and variante == 0: 
                resultado.append(char.upper())
            elif idx % 2 == 0:
                resultado.append(char.upper())
            else:
                resultado.append(char.lower())
                
    return "".join(resultado)

def generar_tres_contrasenas(frases_input):
    palabras = [p.strip() for p in frases_input.split(',')]
    palabras = [p for p in palabras if p][:3] 
    
    if not palabras:
        palabras = ["Segura", "Password", "App"]
        
    while len(palabras) < 3:
        palabras.append(random.choice(["Alfa", "Delta", "Zeta", "Omega", "Code"]))

    sugerencias = []
    
    for i in range(3):
        p1_t = aplicar_leet_y_alternancia(palabras[0], i)
        p2_t = aplicar_leet_y_alternancia(palabras[1], i + 1)
        p3_t = aplicar_leet_y_alternancia(palabras[2], i + 2)
        
        if i == 0:
            pwd = f"{p1_t}{p2_t}{p3_t}"
        elif i == 1:
            pwd = f"{p1_t}{p3_t}{p2_t}"
        else:
            pwd = f"{p3_t}{p1_t}{p2_t}"
            
        if not any(char.isdigit() for char in pwd):
            pwd += random.choice(string.digits)
        if not any(char in "!@#$%^&*()_+-=[]{}|;':,./<>?" for char in pwd):
            pwd += random.choice("!@#$%")
            
        while len(pwd) < 12:
            pwd += random.choice(string.ascii_uppercase) + random.choice(string.digits) + random.choice("!@#$")
            
        sugerencias.append(pwd)
        
    return sugerencias

@app.route('/', methods=['GET', 'POST'])
def index():
    passwords = []
    if request.method == 'POST':
        frases = request.form.get('frases', '')
        passwords = generar_tres_contrasenas(frases)
    
    return render_template_string(HTML_TEMPLATE, passwords=passwords)

# if __name__ == '__main__':
#     app.run(debug=True)
import os

if __name__ == '__main__':
    # Esto permite que Render asigne el puerto automaticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)