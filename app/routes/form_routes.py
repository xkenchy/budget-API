from flask import Blueprint, request, jsonify
from services.budget_service import insert_purchase, get_month_to_date_purchases, get_purchase_categories

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
