from flask import Blueprint, jsonify, request
from controllers.products_controller import create_product, get_all_products, get_product_by_id, update_product, delete_product

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def create_product_route():
    return create_product()


@products.route('/products', methods=['GET'])
def get_all_products_route():
    return get_all_products()


@products.route('/product/<id>', methods=['GET'])
def get_product_by_id_route(id):
    return get_product_by_id(id)


@products.route('/product/update/<id>', methods=['PUT'])
def update_product_route(id):
    return update_product(id)


@products.route('/product/delete/<id>', methods=['DELETE'])
def delete_product_route(id):
    return delete_product(id)
