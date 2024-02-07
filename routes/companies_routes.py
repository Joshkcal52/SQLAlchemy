from flask import Blueprint, jsonify, request
from controllers.companies_controller import create_company, get_all_companies, get_company_by_id, update_company, delete_company

company = Blueprint('company', __name__)


@company.route('/company', methods=['POST'])
def create_company_route():
    return create_company()


@company.route('/companies', methods=['GET'])
def get_all_companies_route():
    return get_all_companies()


@company.route('/company/<id>', methods=['GET'])
def get_company_by_id_route(id):
    return get_company_by_id(id)


@company.route('/company/update/<id>', methods=['PUT'])
def update_company_route(id):
    return update_company(id)


@company.route('/company/delete/<id>', methods=['DELETE'])
def delete_company_route(id):
    return delete_company(id)
