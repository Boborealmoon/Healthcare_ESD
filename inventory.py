from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:8889/inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# export dbURL=mysql+mysqlconnector://root:root@localhost:3306/inventory

db = SQLAlchemy(app)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String, nullable=False)
    ProductQty = db.Column(db.Integer, nullable=False)
    UnitOfMeasurement = db.Column(db.String, nullable=False)
    UnitCost = db.Column(db.Integer, nullable=False)
    SupplierID = db.Column(db.Integer, nullable=False)
    SupplierContactEmail = db.Column(db.String, nullable=False)
    Threshold = db.Column(db.Integer, nullable=False)
    UnitsToOrder = db.Column(db.Integer, nullable=False)

    def __init__(self,ProductID,
                ProductName,
                ProductQty,
                UnitOfMeasurement,
                UnitCost,
                SupplierID,
                SupplierContactEmail,
                Threshold,
                UnitsToOrder
                ):
        self.ProductID = ProductID
        self.ProductName = ProductName
        self.ProductQty = ProductQty
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitCost  = UnitCost
        self.SupplierID = SupplierID
        self.SupplierContactEmail = SupplierContactEmail
        self.Threshhold = Threshold
        self.UnitsToOrder = UnitsToOrder
        

    def json(self):
        return {"ProductID": self.ProductID, "ProductName": self.ProductName,"ProductQty": self.ProductQty,
                "UnitOfMeasurement": self.UnitOfMeasurement,"UnitCost": self.UnitCost,
                "SupplierID": self.SupplierID,"SupplierContactEmail": self.SupplierContactEmail,"Threshold": self.Threshold, "UnitsToOrder": self.UnitsToOrder}  # Convert to string


@app.route('/inventory')
def get_all_inventory():
    inventorylist = db.session.scalars(db.select(Inventory)).all()
    if len(inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [inventory.json() for inventory in inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Inventory is empty."
        }
    ), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
