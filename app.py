from flask import Flask
import os

from routes.categories_routes import category
from routes.companies_routes import company
from routes.products_routes import products
from db import create_tables

app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

app = Flask(__name__)
app.register_blueprint(category)
app.register_blueprint(company)
app.register_blueprint(products)

if __name__ == "__main__":
    create_tables()
    app.run(host=app_host, port=app_port)
