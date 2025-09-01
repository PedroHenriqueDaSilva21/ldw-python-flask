from flask import render_template, request, redirect, url_for

def init_app(app):
    destinos = []
    dicas = []

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/destinos', methods=['GET', 'POST'])
    def destinos_page():
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            descricao = request.form.get('descricao')
            dica = request.form.get('dica')
            if titulo and descricao and dica:
                destinos.append({'titulo': titulo, 'descricao': descricao, 'dica': dica})
                return redirect(url_for('destinos_page'))
        return render_template('destinos.html', destinos=destinos)

    @app.route('/dicas', methods=['GET', 'POST'])
    def dicas_page():
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            contexto = request.form.get('contexto')
            conteudo = request.form.get('conteudo')
            if titulo and contexto and conteudo:
                dicas.append({'titulo': titulo, 'contexto': contexto, 'conteudo': conteudo})
                return redirect(url_for('dicas_page'))
        return render_template('dicas.html', dicas=dicas)
