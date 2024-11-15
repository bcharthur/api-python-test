from flask import Blueprint, jsonify
from python.list import list_items

list_bp = Blueprint('list_bp', __name__)

@list_bp.route('/api/items', methods=['GET'])
def list_all():
    try:
        items = list_items()
        return jsonify({'status': 'success', 'items': items}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
