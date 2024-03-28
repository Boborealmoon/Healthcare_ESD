from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy import func
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL', 'mysql+mysqlconnector://root@localhost:3306/orders')
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


@app.route('/orders')
def get_all_orders():
    orderlist = db.session.scalars(db.select(Order)).all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [orders.json() for orders in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Error nigga"
        }
    ), 404


@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    lastOrderID = db.session.query(func.max(Order.OrderID)).scalar()
    newOrderID = 901 if lastOrderID is None else lastOrderID + 1    

    new_order = Order(
        OrderID= newOrderID,
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

    return jsonify({'code': 201, 'message': 'Order created successfully'}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
