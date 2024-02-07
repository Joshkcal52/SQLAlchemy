from flask import Flask
from routes.categories_routes import category
from routes.companies_routes import company
from routes.products_routes import products
from db.db import create_tables

app = Flask(__name__)
app.register_blueprint(category)
app.register_blueprint(company)
app.register_blueprint(products)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
