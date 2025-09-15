from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import urllib3

# listas em memória
destinos = []
dicas = []

# desativa warning caso façamos verify=False em fallback
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def init_app(app: Flask):

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/destinos', methods=['GET', 'POST'])
    def destinos_page():
        global destinos
        # ===== POST: cadastra destino manual =====
        if request.method == 'POST':
            titulo = request.form.get('titulo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            dica = request.form.get('dica', '').strip()

            if titulo and descricao and dica:
                destinos.append({'titulo': titulo, 'descricao': descricao, 'dica': dica})
                flash(f'Destino "{titulo}" cadastrado!', 'success')
                return redirect(url_for('destinos_page'))
            else:
                flash('Preencha todos os campos para cadastrar.', 'danger')
                return redirect(url_for('destinos_page'))

        # ===== GET: busca países da API com campos específicos =====
        api_destinos = []
        url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,region,languages"

        data = []
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.SSLError:
            try:
                resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10, verify=False)
                resp.raise_for_status()
                data = resp.json()
                flash("Aviso: conexão com API feita sem verificação de certificado (verify=False).", 'warning')
            except Exception as e:
                flash(f"Erro ao acessar API de países (SSL fallback falhou): {e}", 'warning')
                print("API erro (SSL fallback):", e)
        except Exception as e:
            flash(f"Erro ao acessar API de países: {e}", 'warning')
            print("API erro:", e)

        # Trata formatos inesperados
        items = data if isinstance(data, list) else []

        # Monta lista com até 10 países
        for c in items[:10]:
            titulo = c.get('name', {}).get('common') or c.get('name', {}).get('official') or "País Desconhecido"
            flags = c.get('flags', {})
            bandeira = flags.get('png') or flags.get('svg') or None

            capital = c.get('capital')
            capital_str = capital[0] if isinstance(capital, list) and capital else capital or "Não informada"

            region = c.get('region') or "Região não informada"

            languages = c.get('languages', {})
            lang = list(languages.values())[0] if isinstance(languages, dict) and languages else "Idioma não informado"

            descricao = f"Capital: {capital_str} | Região: {region}"
            dica_text = f"Idioma: {lang} | Capital: {capital_str}"

            api_destinos.append({
                'titulo': titulo,
                'descricao': descricao,
                'dica': dica_text,
                'bandeira': bandeira
            })

        # Combina manuais + API
        all_destinos = destinos + api_destinos

        return render_template('destinos.html', destinos=all_destinos)

    @app.route('/dicas', methods=['GET', 'POST'])
    def dicas_page():
        global dicas
        if request.method == 'POST':
            titulo = request.form.get('titulo', '').strip()
            contexto = request.form.get('contexto', '').strip()
            conteudo = request.form.get('conteudo', '').strip()
            if titulo and contexto and conteudo:
                dicas.append({'titulo': titulo, 'contexto': contexto, 'conteudo': conteudo})
                flash(f'Dica "{titulo}" cadastrada!', 'success')
                return redirect(url_for('dicas_page'))
            else:
                flash('Preencha todos os campos!', 'danger')
                return redirect(url_for('dicas_page'))
        return render_template('dicas.html', dicas=dicas)
