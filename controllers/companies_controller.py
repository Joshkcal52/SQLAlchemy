from flask import jsonify, request

from db import db
from models.company import Companies


def create_company(req):
    post_data = req.form if req.form else req.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_company = Companies(values['company_name'])

    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()

    values['company_id'] = query.company_id

    return jsonify({"message": "company created", "result": values}), 200


def get_all_companies():
    query = db.session.query(Companies).all()
    if not query:
        return jsonify({'message': 'There are no companies'}), 404
    companies_list = []

    for companies in query:
        companies_list.append({
            'company_name': companies.company_name,
            'company_id': companies.company_id
        })

    return jsonify({'companies': companies_list}), 200


def get_company_by_id(id):
    query = db.session.query(Companies).filter(Companies.company_id == id).first()
    if not query:
        return jsonify({'message': 'There are no companies'}), 404
    companies_list = []

    companies_list.append({
        'company_name': query.company_name,
        'company_id': query.company_id
    })

    return jsonify({'companies': companies_list}), 200


def update_company(req, id):
    post_data = req.form if req.form else req.json
    query = db.session.query(Companies).filter(Companies.company_id == id).first()
    if not query:
        return jsonify({'message': 'There are no companies matching that id'}), 404

    query.company_name = post_data.get('company_name', query.company_name)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({'message': 'company did not update'}), 400

    updated_record = {
        "company_name": query.company_name
    }

    return jsonify({'message': 'company updated', "updated company name": updated_record}), 200


def delete_company(id):
    query = db.session.query(Companies).filter(Companies.company_id == id).first()
    if not query:
        return jsonify({'message': 'There are no companies matching that id'}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({'message': 'company was not deleted'}), 400

    return jsonify({'message': 'Company deleted successfully'}), 200
