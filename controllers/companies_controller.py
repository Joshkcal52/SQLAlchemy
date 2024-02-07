import psycopg2
from flask import jsonify, request


def db_conn():
    try:
        return psycopg2.connect(
            dbname="postgres_assignment",
            user="josh",
            host="localhost",
        )
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise


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


def create_company():
    post_data = request.form if request.form else request.json
    company_name = post_data.get("company_name")

    query = '''
        INSERT INTO CompaniesTable (company_name)
        VALUES (%s)
    '''

    execute_query(query, [company_name])


def get_all_companies():
    query = 'SELECT * FROM CompaniesTable'
    rows = execute_query(query, fetchall=True)

    companies_data = [dict(row) for row in rows]

    return jsonify({'companies': companies_data})


def get_company_by_id(id):
    query = 'SELECT * FROM CompaniesTable WHERE company_id = %s'
    params = (id,)

    company_data = execute_query(query, params=params, fetchall=False)

    if company_data:
        return jsonify(dict(company_data))
    return jsonify({'message': 'Company not found'}), 404


def update_company(id):
    data = request.get_json()

    company_exists = execute_query('SELECT EXISTS(SELECT 1 FROM CompaniesTable WHERE company_id = %s)', (id,), fetchall=False)

    if company_exists:
        try:
            if 'company_name' in data:
                execute_query('UPDATE CompaniesTable SET company_name = %s WHERE company_id = %s', (data['company_name'], id))

            return jsonify({'message': 'Company updated successfully'}), 204

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Company not found'}), 404


def delete_company(id):
    try:
        query = 'DELETE FROM CompaniesTable WHERE company_id = %s'
        execute_query(query, (id,))
        return jsonify({'message': 'Company deleted successfully'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
