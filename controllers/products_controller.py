import psycopg2
import os
from flask import jsonify, request

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_product():
    post_data = request.form if request.form else request.json
    product_name = post_data.get("product_name")

    if not product_name:
        return jsonify({"message": "product name required"}), 400

    cursor.execute("INSERT INTO Products (product_name) VALUES (%s)", [product_name])

    conn.commit()

    return jsonify({"message": "product added"}), 201


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    results = cursor.fetchall()

    return jsonify({'products': results}), 200


def get_product_by_id(id):
    cursor.execute('SELECT * FROM Products WHERE product_id = %s', [id])
    record = cursor.fetchone()
    return jsonify({'product': record}), 200


def update_product(id):
    data = request.get_json()
    product_name = data.get('product_name')

    cursor.execute('SELECT * FROM Products WHERE product_id = %s', [id])

    if product_name is None:
        return jsonify({"message": "product name required"}), 400

    cursor.execute('UPDATE Products SET product_name = %s WHERE product_id = %s', [data['product_name'], id])
    conn.commit()
    return jsonify({'message': 'Product updated'}), 200


def delete_product(id):
    cursor.execute('SELECT * FROM Products WHERE product_id = %s', [id])
    record = cursor.fetchone()

    if record:
        cursor.execute('DELETE FROM Products WHERE product_id = %s', [id])

    conn.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200
