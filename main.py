from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import json
import uuid
import sqlite3
import threading

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE = 'edi_customization.db'

# Thread-local storage for database connections
local = threading.local()

def get_db():
    if not hasattr(local, 'connection'):
        local.connection = sqlite3.connect(DATABASE)
        local.connection.row_factory = sqlite3.Row
    return local.connection

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gln TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            preferences TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processing_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            document_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            progress INTEGER DEFAULT 0,
            output_format TEXT DEFAULT 'xml',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT
        )
    ''')
    
    # Add sample data if empty
    cursor.execute('SELECT COUNT(*) FROM document_types')
    if cursor.fetchone()[0] == 0:
        sample_docs = [
            ('ORDERS', '220', 'Purchase Orders', 'EDIFACT purchase order messages'),
            ('INVOIC', '380', 'Invoices', 'EDIFACT invoice messages'),
            ('DESADV', '351', 'Dispatch Advice', 'EDIFACT dispatch advice messages')
        ]
        cursor.executemany(
            'INSERT INTO document_types (type, code, name, description) VALUES (?, ?, ?, ?)',
            sample_docs
        )
    
    cursor.execute('SELECT COUNT(*) FROM customers')
    if cursor.fetchone()[0] == 0:
        sample_customers = [
            ('ACME Corporation', '3700123456789', 'orders@acme.com', '', '{"defaultOutputFormat": "xml", "enableNotifications": true}'),
            ('TechCorp Industries', '3700987654321', 'edi@techcorp.com', '', '{"defaultOutputFormat": "json", "enableNotifications": false}')
        ]
        cursor.executemany(
            'INSERT INTO customers (name, gln, email, phone, preferences) VALUES (?, ?, ?, ?, ?)',
            sample_customers
        )
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'message': 'EDI Customization Layer API is running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/system/info')
def system_info():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM document_types')
    doc_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM customers')
    customer_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM processing_jobs')
    job_count = cursor.fetchone()[0]
    
    return jsonify({
        'status': 'operational',
        'components': {
            'database': 'connected',
            'edifact_parser': 'available',
            'xml_generator': 'available'
        },
        'statistics': {
            'document_types': doc_count,
            'customers': customer_count,
            'processing_jobs': job_count
        }
    })

@app.route('/api/edi/document-types', methods=['GET'])
def get_document_types():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM document_types ORDER BY created_at DESC')
    docs = cursor.fetchall()
    
    return jsonify([{
        'id': doc['id'],
        'type': doc['type'],
        'code': doc['code'],
        'name': doc['name'],
        'description': doc['description'],
        'createdAt': doc['created_at']
    } for doc in docs])

@app.route('/api/edi/document-types', methods=['POST'])
def create_document_type():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO document_types (type, code, name, description) VALUES (?, ?, ?, ?)',
        (data['type'], data['code'], data['name'], data.get('description', ''))
    )
    conn.commit()
    
    doc_id = cursor.lastrowid
    cursor.execute('SELECT * FROM document_types WHERE id = ?', (doc_id,))
    doc = cursor.fetchone()
    
    return jsonify({
        'id': doc['id'],
        'type': doc['type'],
        'code': doc['code'],
        'name': doc['name'],
        'description': doc['description'],
        'createdAt': doc['created_at']
    }), 201

@app.route('/api/edi/customers', methods=['GET'])
def get_customers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers ORDER BY created_at DESC')
    customers = cursor.fetchall()
    
    return jsonify([{
        'id': customer['id'],
        'name': customer['name'],
        'gln': customer['gln'],
        'email': customer['email'],
        'phone': customer['phone'],
        'preferences': json.loads(customer['preferences']) if customer['preferences'] else {},
        'createdAt': customer['created_at']
    } for customer in customers])

@app.route('/api/edi/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO customers (name, gln, email, phone, preferences) VALUES (?, ?, ?, ?, ?)',
        (
            data['name'],
            data['gln'],
            data.get('email', ''),
            data.get('phone', ''),
            json.dumps(data.get('preferences', {}))
        )
    )
    conn.commit()
    
    customer_id = cursor.lastrowid
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    
    return jsonify({
        'id': customer['id'],
        'name': customer['name'],
        'gln': customer['gln'],
        'email': customer['email'],
        'phone': customer['phone'],
        'preferences': json.loads(customer['preferences']) if customer['preferences'] else {},
        'createdAt': customer['created_at']
    }), 201

@app.route('/api/processing/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    document_type = request.form.get('documentType', 'ORDERS')
    output_format = request.form.get('outputFormat', 'xml')
    
    conn = get_db()
    cursor = conn.cursor()
    jobs = []
    
    for file in files:
        if file.filename:
            cursor.execute(
                'INSERT INTO processing_jobs (filename, document_type, output_format, status) VALUES (?, ?, ?, ?)',
                (file.filename, document_type, output_format, 'processing')
            )
            job_id = cursor.lastrowid
            
            cursor.execute('SELECT * FROM processing_jobs WHERE id = ?', (job_id,))
            job = cursor.fetchone()
            
            jobs.append({
                'id': job['id'],
                'filename': job['filename'],
                'documentType': job['document_type'],
                'status': job['status'],
                'progress': job['progress'],
                'createdAt': job['created_at']
            })
    
    conn.commit()
    
    return jsonify({
        'success': True,
        'jobs': jobs,
        'message': f'{len(jobs)} files uploaded and processing started'
    })

@app.route('/api/processing/jobs', methods=['GET'])
def get_processing_jobs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM processing_jobs ORDER BY created_at DESC')
    jobs = cursor.fetchall()
    
    return jsonify([{
        'id': job['id'],
        'filename': job['filename'],
        'documentType': job['document_type'],
        'status': job['status'],
        'progress': job['progress'],
        'outputFormat': job['output_format'],
        'createdAt': job['created_at'],
        'completedAt': job['completed_at']
    } for job in jobs])

@app.route('/api/statistics')
def get_statistics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM processing_jobs')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM processing_jobs WHERE status = ?', ('completed',))
    completed = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM processing_jobs WHERE status = ?', ('processing',))
    processing = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM processing_jobs WHERE status = ?', ('error',))
    errors = cursor.fetchone()[0]
    
    return jsonify({
        'totalProcessed': total,
        'successfulProcessed': completed,
        'processingCount': processing,
        'errorCount': errors,
        'successRate': (completed / total * 100) if total > 0 else 0
    })

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    print('🚀 Starting EDI Customization Layer Backend...')
    print('🌐 Server available at: http://localhost:5000')
    print('📊 API Health: http://localhost:5000/api/health')
    app.run(debug=True, host='0.0.0.0', port=5000)