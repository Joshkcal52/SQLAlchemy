import psycopg2
from flask import jsonify, request


def db_conn():
    return psycopg2.connect(
        dbname="postgres_assignment",
        user="josh",
        host="localhost",
    )


def execute_query(query, params=None, fetchall=False):
    conn = db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()

        if fetchall:
            return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def create_product():
    data = request.get_json()
    new_product = {
        'company_id': data['company_id'],
        'company_name': data['company_name'],
        'price': data['price'],
        'description': data['description'],
        'active': data['active']
    }

    try:
        query = '''
            INSERT INTO ProductsTable (company_id, company_name, price, description, active)
            VALUES (%s, %s, %s, %s, %s)
        '''
        execute_query(query, (new_product['company_id'], new_product['company_name'], new_product['price'],
                              new_product['description'], new_product['active']))
        return jsonify({'message': 'Product created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_all_products():
    query = 'SELECT * FROM ProductsTable'
    products_data = execute_query(query, fetchall=True)
    return jsonify({'products': [dict(row) for row in products_data]})


def get_product_by_id(id):
    query = 'SELECT * FROM ProductsTable WHERE product_id = %s'
    params = (id,)

    product_data = execute_query(query, params=params, fetchall=False)

    if product_data:
        return jsonify(dict(product_data))
    return jsonify({'message': 'Product not found'}), 404


def update_product(id):
    data = request.get_json()

    try:
        query = '''
            UPDATE ProductsTable
            SET company_id = %s, company_name = %s, price = %s, description = %s, active = %s
            WHERE product_id = %s
        '''
        execute_query(query, (data['company_id'], data['company_name'], data['price'],
                              data['description'], data['active'], id))
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_product(id):
    try:
        query = 'DELETE FROM ProductsTable WHERE product_id = %s'
        execute_query(query, (id,))
        return jsonify({'message': 'Product deleted successfully'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
