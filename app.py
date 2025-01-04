from flask import Flask, render_template, request, jsonify
from models import db, Stock
from utils import calculate_performance
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stocks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_stocks():
    if request.method == 'POST':
        data = request.json
        stock = Stock(
            name=data['name'],
            purchase_price=data['purchase_price'],
            quantity=data['quantity'],
            purchase_date=data['purchase_date']
        )
        db.session.add(stock)
        db.session.commit()
        return jsonify({'message': 'Stock added successfully'}), 201
    elif request.method == 'GET':
        stocks = Stock.query.all()
        return jsonify([s.to_dict() for s in stocks])
    elif request.method == 'PUT':
        data = request.json
        stock = Stock.query.get(data['id'])
        if stock:
            stock.name = data['name']
            stock.purchase_price = data['purchase_price']
            stock.quantity = data['quantity']
            stock.purchase_date = data['purchase_date']
            db.session.commit()
            return jsonify({'message': 'Stock updated successfully'})
        return jsonify({'error': 'Stock not found'}), 404
    elif request.method == 'DELETE':
        stock_id = request.json['id']
        stock = Stock.query.get(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()
            return jsonify({'message': 'Stock deleted successfully'})
        return jsonify({'error': 'Stock not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
