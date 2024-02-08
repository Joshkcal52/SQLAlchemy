import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname = {database_name}")
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(255) UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES Companies(company_id),
            company_name VARCHAR(255) UNIQUE NOT NULL,
            price INTEGER,
            description VARCHAR(255),
            active BOOLEAN DEFAULT TRUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductsCategories (
            product_id INTEGER REFERENCES Products(product_id),
            category_id INTEGER REFERENCES Categories(category_id),
            PRIMARY KEY (product_id, category_id)
        )
    ''')

    conn.commit()

    # cursor.execute("INSERT INTO Companies (company_name) VALUES (%s) RETURNING company_id", ('Company Name',))
    # company_id = cursor.fetchone()[0]

    # cursor.execute("INSERT INTO Categories (category_name) VALUES (%s) RETURNING category_id", ('Category Name',))
    # category_id = cursor.fetchone()[0]

    # cursor.execute("""
    #     INSERT INTO Products (company_id, company_name, price, description, active)
    #     VALUES (%s, %s, %s, %s, %s) RETURNING product_id
    # """, (company_id, 'Company Name', 100, 'Product Description', True))
    # product_id = cursor.fetchone()[0]

    # cursor.execute("INSERT INTO ProductsCategories (product_id, category_id) VALUES (%s, %s)", (product_id, category_id))

    # cursor.execute('SELECT * FROM Companies')
    # print(cursor.fetchall())

    # cursor.execute('SELECT * FROM Categories')
