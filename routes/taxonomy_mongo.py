import os
from flask import Blueprint, request, jsonify
from auth import role_required, token_required
from mongo import get_mongo_db

taxonomy_bp = Blueprint('taxonomy_mongo', __name__)

@taxonomy_bp.route('/share', methods=['POST'])
@role_required('Teacher')
def share_presentation():
    try:
        db = get_mongo_db()
        if db is None:
            return jsonify({'message': 'MongoDB not configured on server'}), 500
        data = request.json
        
        db.presentations.insert_one({
            'teacher_id': request.user_id,
            'filename': data.get('filename'),
            'pdfUrl': data.get('pdfUrl'),
            'slides': data.get('slides'),
            'sharedAt': data.get('sharedAt')
        })
        return jsonify({'message': 'Shared successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@taxonomy_bp.route('/shared', methods=['GET'])
@token_required
def get_shared_presentations():
    try:
        db = get_mongo_db()
        if db is None:
            return jsonify({'message': 'MongoDB not configured on server'}), 500
        cursor = db.presentations.find().sort('_id', -1).limit(10)
        presentations = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            presentations.append(doc)
        return jsonify(presentations)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
