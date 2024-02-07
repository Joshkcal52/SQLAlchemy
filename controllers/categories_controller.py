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


def create_category():
    post_data = request.form if request.form else request.json
    category_name = post_data.get("category_name")

    query = '''
        INSERT INTO CategoriesTable (category_name)
        VALUES (%s)
    '''

    execute_query(query, [category_name])


def get_all_categories():
    query = 'SELECT * FROM CategoriesTable'
    rows = execute_query(query, fetchall=True)

    categories_data = [dict(row) for row in rows]

    return jsonify({'categories': categories_data})


def get_category_by_id(id):
    query = 'SELECT * FROM CategoriesTable WHERE category_id = %s'
    params = (id,)

    category_data = execute_query(query, params=params, fetchall=False)

    if category_data:
        return jsonify(dict(category_data))
    return jsonify({'message': 'Category not found'}), 404


def update_category(id):
    data = request.get_json()

    category_exists = execute_query('SELECT EXISTS(SELECT 1 FROM CategoriesTable WHERE category_id = %s)', (id,), fetchall=False)

    if category_exists:
        try:
            if 'category_name' in data:
                execute_query('UPDATE CategoriesTable SET category_name = %s WHERE category_id = %s', (data['category_name'], id))

            return jsonify({'message': 'Category updated successfully'}), 204

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Category not found'}), 404


def delete_category(id):
    try:
        query = 'DELETE FROM CategoriesTable WHERE category_id = %s'
        execute_query(query, (id,))
        return jsonify({'message': 'Category deleted successfully'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
