import psycopg2
import os
from flask import jsonify, request


database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_company():
    post_data = request.form if request.form else request.json
    company_name = post_data.get("company_name")

    if not company_name:
        return jsonify({"message": "company name required"}), 400

    cursor.execute("INSERT INTO Companies (company_name) VALUES (%s)", [company_name])

    conn.commit()

    return jsonify({"message": "company added"}), 201


def get_all_companies():
    cursor.execute('SELECT * FROM Companies')
    results = cursor.fetchall()

    return jsonify({'companies': results}), 200


def get_company_by_id(id):
    cursor.execute('SELECT * FROM Companies WHERE company_id = %s', [id])
    record = cursor.fetchone()
    return jsonify({'company': record}), 200


def update_company(id):
    data = request.get_json()
    company_name = data.get('company_name')

    cursor.execute('SELECT * FROM Companies WHERE company_id = %s', [id])

    if company_name is None:
        return jsonify({"message": "company name required"}), 400

    cursor.execute('UPDATE Companies SET company_name = %s WHERE company_id = %s', [data['company_name'], id])
    conn.commit()
    return jsonify({'message': 'Company updated'}), 200


def delete_company(id):
    cursor.execute('SELECT * FROM Companies WHERE company_id = %s', [id])
    record = cursor.fetchone()

    if record:
        cursor.execute('DELETE FROM Companies WHERE company_id = %s', [id])

    conn.commit()

    return jsonify({'message': 'Company deleted successfully'}), 200
