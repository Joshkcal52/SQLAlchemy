import psycopg2


def create_tables():
    conn = psycopg2.connect(
        host="localhost",
        user="josh",
        dbname="postgres_assignment"
    )

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE CompaniesTable (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE CategoriesTable (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(255) UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE ProductsTable (
            product_id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES CompaniesTable(company_id),
            company_name VARCHAR(255) UNIQUE NOT NULL,
            price INTEGER,
            description VARCHAR(255),
            active BOOLEAN DEFAULT TRUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE ProductsCategoriesTable (
            product_id INTEGER REFERENCES ProductsTable(product_id),
            category_id INTEGER REFERENCES CategoriesTable(category_id),
            PRIMARY KEY (product_id, category_id)
        )
    ''')

    cursor.execute("INSERT INTO CompaniesTable (company_name) VALUES (%s) RETURNING company_id", ('Company Name',))
    company_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO CategoriesTable (category_name) VALUES (%s) RETURNING category_id", ('Category Name',))
    category_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO ProductsTable (company_id, company_name, price, description, active)
        VALUES (%s, %s, %s, %s, %s) RETURNING product_id
    """, (company_id, 'Company Name', 100, 'Product Description', True))
    product_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO ProductsCategoriesTable (product_id, category_id) VALUES (%s, %s)", (product_id, category_id))

    cursor.execute('SELECT * FROM CompaniesTable')
    print(cursor.fetchall())

    cursor.execute('SELECT * FROM CategoriesTable')
