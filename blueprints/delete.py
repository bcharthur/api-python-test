from flask import Blueprint, jsonify
from python.delete import delete_item

delete_bp = Blueprint('delete_bp', __name__)

@delete_bp.route('/api/item/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    try:
        delete_item(item_id)
        return jsonify({'status': 'success', 'message': 'Item supprimé avec succès'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
