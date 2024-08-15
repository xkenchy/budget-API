from flask import Blueprint, request, jsonify
from services.budget_service import *

form_bp = Blueprint('form_bp', __name__)

@form_bp.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    price = data.get('price')
    category = data.get('category')
    item = data.get('item')
    if not price or not category or not item:
        return jsonify({"error": "Missing data"}), 400

    insert_purchase(price, category, item)
    return jsonify({"message": "Purchase record inserted successfully"}), 200

@form_bp.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = get_month_to_date_purchases()
    return jsonify(purchases), 200

@form_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = get_purchase_categories()
    return jsonify(categories), 200
@form_bp.route('/budget-left', methods=['GET'])
def budget_left():
    remaining_budget = get_budget_left()
    if remaining_budget is not None:
        return jsonify({"remaining_budget": remaining_budget}), 200
    else:
        return jsonify({"error": "Unable to calculate remaining budget"}), 500
@form_bp.route('/update-monthly-data', methods=['POST'])
def update_monthly_data():
    data = request.get_json()
    monthly_inc = data.get('monthly_inc')
    monthly_save = data.get('monthly_save')
    reoccurrings = data.get('reoccurrings')

    # Calculate the total mandatory cost from the reoccurrings list
    total_mandatory = sum(item['amount'] for item in reoccurrings)

    if monthly_inc is None or monthly_save is None or reoccurrings is None:
        return jsonify({"error": "Missing data"}), 400

    upsert_user_monthly_data(monthly_inc, monthly_save, total_mandatory, reoccurrings)
    return jsonify({"message": "User's monthly data and recurring expenses upserted successfully"}), 200

