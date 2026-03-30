from flask import Flask, render_template, request

from db import (getGeneros)

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/api/generos', methods=['get'])
def obtener_generos():
    generos = getGeneros()
    return {"generos": generos}

if __name__ == '__main__':
    app.run(debug=True)