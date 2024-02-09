from flask import jsonify, request
from db import db
from models.category import Categories


def create_category(req):
    post_data = req.form if req.form else req.json

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({"message": "category name is required"}), 400

    new_category = Categories(category_name)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "category added"}), 201
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400


def get_all_categories():
    categories = Categories.query.all()

    categories_list = [{'category_name': category.category_name, 'category_id': category.category_id} for category in categories]

    return jsonify({'categories': categories_list}), 200


def get_category_by_id(id):
    category = Categories.query.get(id)

    if category:
        return jsonify({'category': {'category_name': category.category_name, 'category_id': category.category_id}}), 200

    return jsonify({'message': 'Category not found'}), 404


def update_category(id):
    data = request.get_json()
    category = Categories.query.get(id)

    if category:
        if 'category_name' in data:
            category.category_name = data['category_name']
            try:
                db.session.commit()
                return jsonify({'message': 'Category updated successfully'}), 200
            except:
                db.session.rollback()
                return jsonify({'message': 'Category update failed'}), 500

    return jsonify({'message': 'Category not found'}), 404


def delete_category(id):
    category = Categories.query.get(id)

    if category:
        try:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category deleted successfully'}), 200
        except:
            db.session.rollback()
            return jsonify({'message': 'Category deletion failed'}), 500

    return jsonify({'message': 'Category not found'}), 404
