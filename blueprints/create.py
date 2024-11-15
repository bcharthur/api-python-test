from flask import Blueprint, request, jsonify
from python.create import create_item

create_bp = Blueprint('create_bp', __name__)

@create_bp.route('/api/item', methods=['POST'])
def create():
    data = request.get_json()
    nom = data.get('nom')

    if not nom:
        return jsonify({'status': 'error', 'message': 'Nom requis'}), 400

    try:
        create_item(nom)
        return jsonify({'status': 'success', 'message': 'Item créé avec succès'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
