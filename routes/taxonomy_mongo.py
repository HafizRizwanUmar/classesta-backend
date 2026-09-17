import json
from flask import Blueprint, request, jsonify
from auth import role_required, token_required
from database import get_db

taxonomy_bp = Blueprint('taxonomy_mongo', __name__)

@taxonomy_bp.route('/share', methods=['POST'])
@role_required('Teacher')
def share_presentation():
    try:
        data = request.json
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO presentations (teacher_id, filename, pdfUrl, slides, sharedAt)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            request.user_id,
            data.get('filename'),
            data.get('pdfUrl'),
            json.dumps(data.get('slides')),
            data.get('sharedAt')
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Shared successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@taxonomy_bp.route('/shared', methods=['GET'])
@token_required
def get_shared_presentations():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM presentations ORDER BY id DESC LIMIT 10')
        rows = c.fetchall()
        conn.close()
        
        presentations = []
        for row in rows:
            doc = dict(row)
            doc['_id'] = str(doc['id'])
            doc['slides'] = json.loads(doc['slides']) if doc['slides'] else []
            presentations.append(doc)
            
        return jsonify(presentations)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
