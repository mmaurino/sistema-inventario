from flask import Flask, render_template

app = Flask(__name__)

# Importamos las rutas después de crear la app
from routes import *

# Imprimimos las rutas disponibles para verificar
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
