from flask import Flask, render_template

# Criando uma instância do Flask

app = Flask(__name__, template_folder='views') # _name_ representa o nome da aplicação


#Definindo a rota principal da aplicação '/'
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/games')
def games():
    title = 'Tarisland'
    year = 2022
    category = 'MMORPG'
    return render_template('games.html',title=title,year=year,category=category)
#Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    #Iniciando o Servidor
    app.run(host='localhost',port=5000,debug=True) # Iniciando o servidor
