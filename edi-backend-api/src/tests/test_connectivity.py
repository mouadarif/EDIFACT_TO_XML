import unittest
import json
# import sys # No longer needed for this path manipulation
# import os # No longer needed for this path manipulation

# Assuming 'src' is importable after 'pip install -e .' from edi-backend-api
from src.main import app

class ConnectivityTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['message'], 'EDI Customization Layer is running')

    def test_document_types_endpoint(self):
        response = self.app.get('/api/edi/document-types')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)
        # Check for expected keys in one of the document types
        if len(data['data']) > 0:
            self.assertIn('document_type', data['data'][0])
            self.assertIn('document_code', data['data'][0])
            self.assertIn('description', data['data'][0])

    def test_root_path_serves_html(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        # Check for a common HTML tag
        self.assertIn(b'<html', response.data.lower())
        # Check if it's serving the actual index.html or the fallback
        # For now, just ensuring it's HTML is good.
        # A more specific check might look for content from edi-backend-api/src/static/index.html
        # For example, if we know a specific title or element ID from that file.
        # Based on ls output, 'edi-backend-api/src/static/index.html' exists.
        # The fallback HTML also contains "EDI Customization Layer"
        self.assertTrue(b"edi customization layer" in response.data.lower() or \
                        b"<!doctype html>" in response.data.lower()) # A common marker for React/Vite builds

    def test_stub_system_info_endpoint(self):
        response = self.app.get('/api/system/info')
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

    def test_stub_statistics_endpoint(self):
        response = self.app.get('/api/statistics')
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

    def test_stub_customers_get_endpoint(self):
        response = self.app.get('/api/edi/customers')
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

    def test_stub_customers_post_endpoint(self):
        response = self.app.post('/api/edi/customers', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

    def test_stub_processing_upload_post_endpoint(self):
        # Minimal POST data, actual content doesn't matter for a stub
        response = self.app.post('/api/processing/upload', data={'file': (None, '')})
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

    def test_stub_processing_jobs_get_endpoint(self):
        response = self.app.get('/api/processing/jobs')
        self.assertEqual(response.status_code, 501)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not yet implemented', data['message'])

if __name__ == '__main__':
    unittest.main()
