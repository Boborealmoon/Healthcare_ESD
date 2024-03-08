from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@localhost/smuclinic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Order model
class Order(db.Model):
    __tablename__ = 'orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(50), nullable=False)
    ProductQty = db.Column(db.Integer, nullable=False)
    UnitsOrdered = db.Column(db.Integer, nullable=False)
    OrderDate = db.Column(db.Date, nullable=False)
    SupplierID = db.Column(db.Integer, nullable=False)
    SupplierContactEmail = db.Column(db.String(100))

# API route to create an order
@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()

    if not all(key in data for key in ['ProductID', 'ProductName', 'ProductQty', 'UnitsOrdered', 'OrderDate', 'SupplierID']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_order = Order(
        ProductID=data['ProductID'],
        ProductName=data['ProductName'],
        ProductQty=data['ProductQty'],
        UnitsOrdered=data['UnitsOrdered'],
        OrderDate=data['OrderDate'],
        SupplierID=data['SupplierID'],
        SupplierContactEmail=data.get('SupplierContactEmail', None)
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

if __name__ == '__main__':
    # Create the database tables before running the app
    db.create_all()
    app.run(debug=True)
