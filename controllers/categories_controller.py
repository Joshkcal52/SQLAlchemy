import psycopg2
import os
from flask import jsonify, request

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_category():
    post_data = request.form if request.form else request.json
    category_name = post_data.get("category_name")

    if not category_name:
        return jsonify({"message": "category name required"}), 400

    cursor.execute("INSERT INTO Categories (category_name) VALUES (%s)", [category_name])

    conn.commit()

    return jsonify({"message": "category added"}), 201


def get_all_categories():
    cursor.execute('SELECT * FROM Categories')
    results = cursor.fetchall()

    return jsonify({'categories': results}), 200


def get_category_by_id(id):
    params = {'id': id}
    cursor.execute('SELECT * FROM Categories WHERE category_id = %(id)s', params)
    record = cursor.fetchone()

    if record:
        return jsonify({'category': record}), 200

    return jsonify({'message': 'Category not found'}), 404


def update_category(id):
    data = request.get_json()

    category_exists_query = 'SELECT EXISTS(SELECT 1 FROM Categories WHERE category_id = %(id)s)'
    cursor.execute(category_exists_query, {'id': id})
    category_exists = cursor.fetchone()[0]

    if category_exists:
        if 'category_name' in data:
            update_query = 'UPDATE Categories SET category_name = %(category_name)s WHERE category_id = %(id)s'
            cursor.execute(update_query, {'category_name': data['category_name'], 'id': id})
            conn.commit()
        return jsonify({'message': 'Category updated successfully'}), 200

    return jsonify({'message': 'Category not found'}), 404


def delete_category(id):
    delete_query = 'DELETE FROM Categories WHERE category_id = %(id)s'
    cursor.execute(delete_query, {'id': id})
    conn.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200
