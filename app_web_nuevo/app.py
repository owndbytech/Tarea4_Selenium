from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Base de datos temporal en memoria
piezas_db = [
    {'id': 1, 'nombre': 'Bujía', 'precio': '150'},
    {'id': 2, 'nombre': 'Filtro de Aceite', 'precio': '450'}
]

@app.route('/')
def index():
    return render_template('index.html', piezas=piezas_db)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre_pieza') # Cambiado para coincidir con HTML
    precio = request.form.get('precio_pieza') # Cambiado para coincidir con HTML
    if nombre and precio:
        nueva_id = piezas_db[-1]['id'] + 1 if piezas_db else 1
        nueva_pieza = {'id': nueva_id, 'nombre': nombre, 'precio': precio}
        piezas_db.append(nueva_pieza)
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pieza = next((p for p in piezas_db if p['id'] == id), None)
    if request.method == 'POST':
        pieza['nombre'] = request.form.get('nombre_pieza')
        pieza['precio'] = request.form.get('precio_pieza')
        return redirect('/')
    return render_template('editar.html', pieza=pieza)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    global piezas_db
    piezas_db = [p for p in piezas_db if p['id'] != id]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)