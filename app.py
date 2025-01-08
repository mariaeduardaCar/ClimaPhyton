from flask import Flask, request, jsonify, render_template
import requests
from models import db, Clima
from config import Configuracao
from flask_cors import CORS

aplicativo = Flask(__name__)
CORS(aplicativo)
aplicativo.config.from_object(Configuracao)
db.init_app(aplicativo)

with aplicativo.app_context():
    db.create_all()

@aplicativo.route('/')
def home():
    return render_template('index.html')

@aplicativo.route('/clima', methods=['GET'])
def obter_clima():
    cidade = request.args.get('cidade')
    if not cidade:
        return jsonify({"erro": "Cidade é obrigatória"}), 400
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={Configuracao.CHAVE_API_CLIMA}&units=metric'
    resposta = requests.get(url)
    
    if resposta.status_code != 200:
        return jsonify({"erro": "Não foi possível obter os dados do clima"}), 500

    dados = resposta.json()
    temperatura = dados['main']['temp']
    descricao = dados['weather'][0]['description']
    
    # Salvar os dados no banco
    clima = Clima(cidade=cidade, temperatura=temperatura, descricao=descricao)
    db.session.add(clima)
    db.session.commit()

    return jsonify({
        'cidade': cidade,
        'temperatura': temperatura,
        'descricao': descricao
    })

@aplicativo.route('/historico', methods=['GET'])
def obter_historico():
    # Buscar todos os registros de clima no banco de dados
    registros = Clima.query.all()
    historico = []
    
    for registro in registros:
        historico.append({
            'cidade': registro.cidade,
            'temperatura': registro.temperatura,
            'descricao': registro.descricao
        })
    
    # Se não houver histórico, retorna uma mensagem
    if not historico:
        return jsonify({'message': 'Nenhum dado de clima encontrado.'}), 404

    return jsonify(historico)

if __name__ == '__main__':
    aplicativo.run(debug=True)
