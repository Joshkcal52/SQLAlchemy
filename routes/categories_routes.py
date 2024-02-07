from flask import Blueprint
from controllers.categories_controller import create_category, get_all_categories, get_category_by_id, update_category, delete_category

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def create_category_route():
    return create_category()


@category.route('/categories', methods=['GET'])
def get_all_categories_route():
    return get_all_categories()


@category.route('/category/<id>', methods=['GET'])
def get_category_by_id_route(id):
    return get_category_by_id(id)


@category.route('/category/update/<id>', methods=['PUT'])
def update_category_route(id):
    return update_category(id)


@category.route('/category/delete/<id>', methods=['DELETE'])
def delete_category_by_id_route(id):
    return delete_category(id)
