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
@form_bp.route('/budget-left-data', methods=['GET'])
def budget_data():
    budget_data = get_budget_left_data()
    if "error" in budget_data:
        return jsonify(budget_data), budget_data.get("status_code", 500)
    return jsonify(budget_data), 200

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
@form_bp.route('/get-monthly-data', methods=['GET'])
def get_monthly_data():
    user_data = get_user_monthly_data()
    if "error" in user_data:
        return jsonify(user_data), user_data.get("status_code", 500)
    return jsonify(user_data), 200


