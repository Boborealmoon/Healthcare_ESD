from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL', 'mysql+mysqlconnector://root:root@localhost:8889/orders')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, nullable=False)
    ProductName = db.Column(db.String(50), nullable=False)
    ProductQty = db.Column(db.Integer, nullable=False)
    UnitsOrdered = db.Column(db.Integer, nullable=False)
    OrderDate = db.Column(db.Date, nullable=False)
    SupplierID = db.Column(db.Integer, nullable=False)
    SupplierContactEmail = db.Column(db.String(100))

    def __init__(self, OrderID, ProductID, ProductName, ProductQty, UnitsOrdered, OrderDate, SupplierID, SupplierContactEmail):
        self.OrderID = OrderID
        self.ProductID = ProductID
        self.ProductName = ProductName
        self.ProductQty = ProductQty
        self.UnitsOrdered = UnitsOrdered
        self.OrderDate = OrderDate
        self.SupplierID = SupplierID
        self.SupplierContactEmail = SupplierContactEmail

    def json(self):
        return {
            "OrderID": self.OrderID,
            "ProductID": self.ProductID,
            "ProductName": self.ProductName,
            "ProductQty": self.ProductQty,
            "UnitsOrdered": self.UnitsOrdered,
            "OrderDate": str(self.OrderDate),
            "SupplierID": self.SupplierID,
            "SupplierContactEmail": self.SupplierContactEmail
        }


@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    if Order.query.filter_by(OrderID=data['OrderID']).first() is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "OrderID": data['OrderID']
                },
                "message": "Order already exists."
            }
        ), 400
    

    if not all(key in data for key in ['OrderID', 'ProductID', 'ProductName', 'ProductQty', 'UnitsOrdered', 'OrderDate', 'SupplierID']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_order = Order(
        OrderID=data['OrderID'],
        ProductID=data['ProductID'],
        ProductName=data['ProductName'],
        ProductQty=data['ProductQty'],
        UnitsOrdered=data['UnitsOrdered'],
        OrderDate=data['OrderDate'],
        SupplierID=data['SupplierID'],
        SupplierContactEmail=data.get('SupplierContactEmail', None)
    )

    try:
        db.session.add(new_order)
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the order."
            }
        ), 500

    return jsonify({'message': 'Order created successfully'}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
