from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return '''
        <!DOCTYPE html>
        <html><head><title>EDI Customization Layer</title></head>
        <body style="font-family:Arial;margin:40px;background:#f5f5f5">
        <div style="max-width:800px;margin:0 auto;background:white;padding:40px;border-radius:8px">
        <h1>EDI Customization Layer</h1>
        <p>Backend server is running successfully!</p>
        <p><a href="/api/health">Check API Health</a></p>
        </div></body></html>'''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'message': 'EDI Customization Layer is running'
    })

@app.route('/api/edi/document-types')
def document_types():
    return jsonify({
        'success': True,
        'data': [
            {'document_type': 'ORDERS', 'document_code': '220', 'description': 'Purchase order messages'},
            {'document_type': 'INVOIC', 'document_code': '380', 'description': 'Invoice messages'},
            {'document_type': 'DESADV', 'document_code': '351', 'description': 'Dispatch advice messages'}
        ]
    })

# Placeholder routes for frontend API calls not yet implemented
@app.route('/api/system/info', methods=['GET'])
def system_info_stub():
    return jsonify({'message': 'Endpoint /api/system/info not yet implemented'}), 501

@app.route('/api/statistics', methods=['GET'])
def statistics_stub():
    return jsonify({'message': 'Endpoint /api/statistics not yet implemented'}), 501

@app.route('/api/edi/customers', methods=['GET', 'POST'])
def customers_stub():
    return jsonify({'message': 'Endpoint /api/edi/customers not yet implemented'}), 501

@app.route('/api/processing/upload', methods=['POST'])
def upload_stub():
    return jsonify({'message': 'Endpoint /api/processing/upload not yet implemented'}), 501

@app.route('/api/processing/jobs', methods=['GET'])
def jobs_stub():
    return jsonify({'message': 'Endpoint /api/processing/jobs not yet implemented'}), 501

if __name__ == '__main__':
    print('🚀 Starting EDI Customization Layer Backend...')
    print('🌐 Server available at: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)