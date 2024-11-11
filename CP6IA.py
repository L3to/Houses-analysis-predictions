from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('modelo.pkl')

def prever_preco(novas_casas):
    novas_casas = pd.DataFrame(novas_casas)
    preco_predito = model.predict(novas_casas)
    preco_predito = [f"R${round(preco, 2):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') for preco in preco_predito]
    return preco_predito

@app.route('/prever_preco', methods=['GET'])
def prever():
    try:
        dados = {
            'bedrooms': request.args.getlist('bedrooms', type=int),
            'bathrooms': request.args.getlist('bathrooms', type=int),
            'sqft_living': request.args.getlist('sqft_living', type=int),
            'sqft_lot': request.args.getlist('sqft_lot', type=int),
            'floors': request.args.getlist('floors', type=int),
            'waterfront': request.args.getlist('waterfront', type=int),
            'view': request.args.getlist('view', type=int),
            'condition': request.args.getlist('condition', type=int),
            'grade': request.args.getlist('grade', type=int),
            'sqft_above': request.args.getlist('sqft_above', type=int),
            'sqft_basement': request.args.getlist('sqft_basement', type=int),
            'yr_built': request.args.getlist('yr_built', type=int),
            'yr_renovated': request.args.getlist('yr_renovated', type=int),
            'zipcode': request.args.getlist('zipcode', type=int),
            'lat': request.args.getlist('lat', type=float),
            'long': request.args.getlist('long', type=float),
            'sqft_living15': request.args.getlist('sqft_living15', type=int),
            'sqft_lot15': request.args.getlist('sqft_lot15', type=int)
        }

        if not dados or len(dados['bedrooms']) == 0:
            return jsonify({'error': 'Dados insuficientes'}), 400

        precos = prever_preco(dados)
        
        return jsonify({'precos': precos}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
