from flask import Flask
from controllers import routes

# Criando a aplicação Flask
app = Flask(__name__, template_folder='views')

# Inicializa as rotas
routes.init_app(app)

# Inicia o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)