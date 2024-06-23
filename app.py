from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import requests
from fetch_data import fetch_marketplace_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

from models import Item, Transaction, PriceHistory, Demand

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items')
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/update_data')
def update_data():
    data = fetch_marketplace_data()
    for item_data in data:
        item = Item.query.filter_by(name=item_data['name']).first()
        if not item:
            item = Item(name=item_data['name'], description=item_data['description'], category=item_data['category'])
            db.session.add(item)
            db.session.commit()
        transaction = Transaction(item_id=item.id, type=item_data['type'], price=item_data['price'], quantity=item_data['quantity'], timestamp=item_data['timestamp'])
        db.session.add(transaction)
        db.session.commit()
        socketio.emit('update', transaction.to_dict())
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
