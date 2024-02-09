from flask import jsonify, request
from db import db
from models.products import Products


def create_product(req):
    post_data = req.form if req.form else req.json

    product_name = post_data.get('product_name')
    price = post_data.get('price')
    company_id = post_data.get('company_id')

    if not post_data.get('description'):
        description = ''
    else:
        description = post_data.get('description')

    new_product = Products(product_name=product_name, description=description, price=price, company_id=company_id)

    try:
        db.session.add(new_product)
        db.session.commit()
        new_product_details = {
            "product_id": new_product.product_id,
            "product_name": new_product.product_name,
            "description": new_product.description,
            "price": new_product.price,
            "company_id": new_product.company_id
        }
        return jsonify({"message": "Product created", 'new_product': new_product_details}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "Unable to create product"}), 400


def get_all_products():
    products = Products.query.all()

    products_list = [{
        'product_id': product.product_id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'company_id': product.company_id
    } for product in products]

    return jsonify({'products': products_list}), 200


def get_product_by_id(id):
    product = Products.query.get(id)

    if product:
        product_details = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'company_id': product.company_id
        }

        return jsonify({'product': product_details}), 200

    return jsonify({'message': 'Product not found'}), 404


def update_product(id):
    data = request.get_json()
    product = Products.query.get(id)

    if product:
        if 'product_name' in data:
            product.product_name = data['product_name']

        try:
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200

        except:
            db.session.rollback()
            return jsonify({'message': 'Product update failed'}), 500

    return jsonify({'message': 'Product not found'}), 404


def delete_product(id):
    product = Products.query.get(id)

    if product:
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200

        except:
            db.session.rollback()
            return jsonify({'message': 'Product deletion failed'}), 500

    return jsonify({'message': 'Product not found'}), 404
