from flask import Blueprint, request, jsonify

form_bp = Blueprint('form_bp', __name__)

@form_bp.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    # Process form data here
    print(data)
    response = {
        "message": "Form submitted successfully",
        "data": data
    }
    return jsonify(response), 200

