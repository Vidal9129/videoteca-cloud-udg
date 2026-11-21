import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('recursos_cloud.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS recursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            url_medio TEXT NOT NULL
        );
    ''')
    # Insertar 2 registros de ejemplo si la tabla está vacía
    count = conn.execute('SELECT COUNT(*) FROM recursos').fetchone()[0]
    if count == 0:
        conn.execute('''
            INSERT INTO recursos (titulo, plataforma, descripcion, url_medio)
            VALUES (?, ?, ?, ?)
        ''', (
            'Arquitectura Cloud Computing - Conferencia',
            'YouTube (Streaming Cloud)',
            'Video explicativo sobre modelos IaaS, PaaS y SaaS en la nube moderna.',
            'https://www.youtube.com/watch?v=M988_fsOSWo'
        ))
        conn.execute('''
            INSERT INTO recursos (titulo, plataforma, descripcion, url_medio)
            VALUES (?, ?, ?, ?)
        ''', (
            'Documentación Técnica y Manuales PDF',
            'Google Drive (Almacenamiento Cloud)',
            'Repositorio de documentos académicos y guías de despliegue en la nube.',
            'https://drive.google.com'
        ))
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    recursos = conn.execute('SELECT * FROM recursos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', recursos=recursos)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    plataforma = request.form['plataforma']
    descripcion = request.form['descripcion']
    url_medio = request.form['url_medio']

    if titulo and plataforma and descripcion and url_medio:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO recursos (titulo, plataforma, descripcion, url_medio)
            VALUES (?, ?, ?, ?)
        ''', (titulo, plataforma, descripcion, url_medio))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recursos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)