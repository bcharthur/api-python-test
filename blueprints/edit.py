from flask import Blueprint, request, jsonify
from python.edit import edit_item

edit_bp = Blueprint('edit_bp', __name__)

@edit_bp.route('/api/item/<int:item_id>', methods=['PUT'])
def edit(item_id):
    data = request.get_json()
    nom = data.get('nom')

    if not nom:
        return jsonify({'status': 'error', 'message': 'Nom requis'}), 400

    try:
        edit_item(item_id, nom)
        return jsonify({'status': 'success', 'message': 'Item modifié avec succès'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
