# EDI Customization Layer Integration Guide

## Overview

This guide provides detailed instructions for integrating the EDI Customization Layer with your existing EDIFACT Parser application and other systems.

## Table of Contents

1. [Integration Architecture](#integration-architecture)
2. [Step-by-Step Integration](#step-by-step-integration)
3. [Configuration Setup](#configuration-setup)
4. [API Integration](#api-integration)
5. [Workflow Integration](#workflow-integration)
6. [Testing Integration](#testing-integration)
7. [Production Deployment](#production-deployment)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Integration Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Web API   │    │  Batch Job  │    │   Service   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                Integration Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │            EDIFACT Parser Core                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │          Customization Layer                           │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ File System │    │  Database   │    │   Message   │     │
│  │             │    │             │    │    Queue    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

1. **Direct Integration**: Call customization layer directly from your application
2. **Service Integration**: Expose customization as a microservice
3. **Batch Integration**: Integrate with existing batch processing workflows
4. **Event-Driven Integration**: Use message queues for asynchronous processing

## Step-by-Step Integration

### Step 1: Environment Setup

1. **Install Dependencies**:
   ```bash
   # Ensure Python 3.7+ is installed
   pip install -r requirements.txt
   ```

2. **Add to Python Path**:
   ```python
   import sys
   sys.path.append('/path/to/edifact_parser')
   ```

3. **Verify Installation**:
   ```python
   from customization import CustomizationProcessor
   processor = CustomizationProcessor()
   print("Customization layer loaded successfully")
   ```

### Step 2: Basic Integration

#### Option A: Direct Integration

```python
from customization import CustomizationProcessor, ConfigurationManager

class EDIProcessor:
    def __init__(self, config_path=None):
        self.config_manager = ConfigurationManager(config_path)
        self.customization_processor = CustomizationProcessor(self.config_manager)
    
    def process_edi_file(self, file_path, document_type, customer_gln=None):
        """Process EDI file and return customized XML"""
        try:
            result = self.customization_processor.process_file(
                file_path, document_type, customer_gln
            )
            
            if result.success:
                return {
                    'success': True,
                    'xml_output': result.output_xml,
                    'metadata': result.metadata
                }
            else:
                return {
                    'success': False,
                    'errors': result.errors,
                    'warnings': result.warnings
                }
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)]
            }

# Usage
processor = EDIProcessor('/path/to/config')
result = processor.process_edi_file('input.xml', 'ORDERS', '1234567890123')
```

#### Option B: Service Integration

```python
from flask import Flask, request, jsonify
from customization import CustomizationProcessor
import tempfile
import os

app = Flask(__name__)
processor = CustomizationProcessor()

@app.route('/process-edi', methods=['POST'])
def process_edi():
    try:
        # Get parameters
        document_type = request.form.get('document_type')
        customer_gln = request.form.get('customer_gln')
        
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            
            # Process file
            result = processor.process_file(
                temp_file.name, document_type, customer_gln
            )
            
            # Clean up
            os.unlink(temp_file.name)
            
            if result.success:
                return jsonify({
                    'success': True,
                    'xml_output': result.output_xml,
                    'processing_stats': result.processing_stats
                })
            else:
                return jsonify({
                    'success': False,
                    'errors': result.errors
                }), 400
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Step 3: Advanced Integration Patterns

#### Batch Processing Integration

```python
import schedule
import time
from pathlib import Path
from customization.customization_processor import BatchProcessor

class EDIBatchProcessor:
    def __init__(self, input_dir, output_dir, config_manager):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.batch_processor = BatchProcessor()
        self.config_manager = config_manager
    
    def process_daily_files(self):
        """Process all files received today"""
        today_dir = self.input_dir / datetime.now().strftime('%Y-%m-%d')
        
        if today_dir.exists():
            # Process ORDERS files
            orders_results = self.batch_processor.process_directory(
                today_dir / 'orders',
                self.output_dir / 'orders',
                document_type='ORDERS',
                file_pattern='*.xml'
            )
            
            # Process INVOIC files
            invoice_results = self.batch_processor.process_directory(
                today_dir / 'invoices',
                self.output_dir / 'invoices',
                document_type='INVOIC',
                file_pattern='*.xml'
            )
            
            # Log results
            self.log_batch_results(orders_results, 'ORDERS')
            self.log_batch_results(invoice_results, 'INVOIC')
    
    def log_batch_results(self, results, doc_type):
        """Log batch processing results"""
        print(f"{doc_type} Processing Results:")
        print(f"  Total: {results['total_files']}")
        print(f"  Success: {results['successful_files']}")
        print(f"  Failed: {results['failed_files']}")
        print(f"  Success Rate: {results['summary']['success_rate']:.2%}")

# Schedule batch processing
batch_processor = EDIBatchProcessor('/data/input', '/data/output', config_manager)
schedule.every().day.at("02:00").do(batch_processor.process_daily_files)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

#### Message Queue Integration

```python
import pika
import json
from customization import CustomizationProcessor

class EDIMessageProcessor:
    def __init__(self, rabbitmq_url, config_manager):
        self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        self.channel = self.connection.channel()
        self.processor = CustomizationProcessor(config_manager)
        
        # Declare queues
        self.channel.queue_declare(queue='edi_input', durable=True)
        self.channel.queue_declare(queue='edi_output', durable=True)
        self.channel.queue_declare(queue='edi_errors', durable=True)
    
    def process_message(self, ch, method, properties, body):
        """Process EDI message from queue"""
        try:
            # Parse message
            message = json.loads(body)
            file_path = message['file_path']
            document_type = message['document_type']
            customer_gln = message.get('customer_gln')
            
            # Process file
            result = self.processor.process_file(file_path, document_type, customer_gln)
            
            if result.success:
                # Send to output queue
                output_message = {
                    'original_message': message,
                    'xml_output': result.output_xml,
                    'processing_stats': result.processing_stats
                }
                
                self.channel.basic_publish(
                    exchange='',
                    routing_key='edi_output',
                    body=json.dumps(output_message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            else:
                # Send to error queue
                error_message = {
                    'original_message': message,
                    'errors': result.errors,
                    'warnings': result.warnings
                }
                
                self.channel.basic_publish(
                    exchange='',
                    routing_key='edi_errors',
                    body=json.dumps(error_message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing message: {e}")
            # Reject message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        """Start consuming messages"""
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='edi_input',
            on_message_callback=self.process_message
        )
        
        print("Starting EDI message processing...")
        self.channel.start_consuming()

# Usage
processor = EDIMessageProcessor('amqp://localhost', config_manager)
processor.start_consuming()
```

## Configuration Setup

### Configuration File Structure

Create a configuration directory structure:

```
config/
├── document_types/
│   ├── ORDERS.json
│   ├── INVOIC.json
│   └── DESADV.json
├── customers/
│   ├── 1234567890123.json
│   ├── 9876543210987.json
│   └── default.json
├── mappings/
│   ├── ORDERS_1234567890123.json
│   ├── INVOIC_1234567890123.json
│   └── default_mappings.json
└── templates/
    ├── purchase_order.xml
    ├── invoice.xml
    └── custom_templates.xml
```

### Environment-Specific Configuration

```python
import os
from customization import ConfigurationManager

def create_config_manager():
    """Create configuration manager based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    
    config_paths = {
        'development': './config/dev',
        'testing': './config/test',
        'production': './config/prod'
    }
    
    config_path = config_paths.get(env, './config/dev')
    return ConfigurationManager(config_path)

# Usage
config_manager = create_config_manager()
```

### Dynamic Configuration Loading

```python
class DynamicConfigManager:
    def __init__(self, database_connection):
        self.db = database_connection
        self.config_manager = ConfigurationManager()
        self.load_configurations_from_database()
    
    def load_configurations_from_database(self):
        """Load configurations from database"""
        # Load document types
        doc_types = self.db.execute("SELECT * FROM document_types").fetchall()
        for doc_type in doc_types:
            config = DocumentTypeConfig(**doc_type)
            self.config_manager.add_document_type_config(config)
        
        # Load customers
        customers = self.db.execute("SELECT * FROM customers").fetchall()
        for customer in customers:
            config = CustomerConfig(**customer)
            self.config_manager.add_customer_config(config)
        
        # Load mappings
        mappings = self.db.execute("SELECT * FROM field_mappings").fetchall()
        for mapping in mappings:
            config = MappingConfig(**mapping)
            self.config_manager.add_mapping_config(config)
    
    def refresh_configurations(self):
        """Refresh configurations from database"""
        self.config_manager = ConfigurationManager()
        self.load_configurations_from_database()
```

## API Integration

### RESTful API Design

```python
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from customization import CustomizationProcessor

app = Flask(__name__)
api = Api(app)

class EDIProcessingResource(Resource):
    def __init__(self):
        self.processor = CustomizationProcessor()
    
    def post(self):
        """Process EDI data"""
        try:
            data = request.get_json()
            
            result = self.processor.process_data(
                data['edi_data'],
                data['document_type'],
                data.get('customer_gln'),
                data.get('output_template'),
                data.get('validation_level', 'standard')
            )
            
            return {
                'success': result.success,
                'xml_output': result.output_xml if result.success else None,
                'errors': result.errors,
                'warnings': result.warnings,
                'processing_stats': result.processing_stats
            }
            
        except Exception as e:
            return {'error': str(e)}, 500

class ConfigurationResource(Resource):
    def __init__(self):
        self.config_manager = ConfigurationManager()
    
    def get(self, config_type=None):
        """Get configurations"""
        if config_type == 'document-types':
            return {'document_types': self.config_manager.list_document_types()}
        elif config_type == 'customers':
            return {'customers': self.config_manager.list_customers()}
        elif config_type == 'mappings':
            return {'mappings': self.config_manager.list_mapping_configs()}
        else:
            return {
                'document_types': self.config_manager.list_document_types(),
                'customers': self.config_manager.list_customers(),
                'mappings': self.config_manager.list_mapping_configs()
            }

# Register resources
api.add_resource(EDIProcessingResource, '/api/process')
api.add_resource(ConfigurationResource, '/api/config', '/api/config/<string:config_type>')

if __name__ == '__main__':
    app.run(debug=True)
```

### GraphQL API Integration

```python
import graphene
from customization import CustomizationProcessor, ConfigurationManager

class ProcessingResult(graphene.ObjectType):
    success = graphene.Boolean()
    xml_output = graphene.String()
    errors = graphene.List(graphene.String)
    warnings = graphene.List(graphene.String)
    processing_stats = graphene.JSONString()

class ProcessEDI(graphene.Mutation):
    class Arguments:
        edi_data = graphene.JSONString(required=True)
        document_type = graphene.String(required=True)
        customer_gln = graphene.String()
        output_template = graphene.String()
        validation_level = graphene.String()
    
    Output = ProcessingResult
    
    def mutate(self, info, edi_data, document_type, customer_gln=None, 
               output_template=None, validation_level='standard'):
        processor = CustomizationProcessor()
        
        result = processor.process_data(
            edi_data, document_type, customer_gln, 
            output_template, validation_level
        )
        
        return ProcessingResult(
            success=result.success,
            xml_output=result.output_xml,
            errors=result.errors,
            warnings=result.warnings,
            processing_stats=result.processing_stats
        )

class Query(graphene.ObjectType):
    available_document_types = graphene.List(graphene.String)
    available_customers = graphene.List(graphene.String)
    
    def resolve_available_document_types(self, info):
        config_manager = ConfigurationManager()
        return config_manager.list_document_types()
    
    def resolve_available_customers(self, info):
        config_manager = ConfigurationManager()
        return config_manager.list_customers()

class Mutations(graphene.ObjectType):
    process_edi = ProcessEDI.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
```

## Workflow Integration

### Integration with Apache Airflow

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from customization.customization_processor import BatchProcessor

def process_edi_files(**context):
    """Airflow task to process EDI files"""
    batch_processor = BatchProcessor()
    
    # Get execution date
    execution_date = context['execution_date']
    input_dir = f"/data/input/{execution_date.strftime('%Y-%m-%d')}"
    output_dir = f"/data/output/{execution_date.strftime('%Y-%m-%d')}"
    
    # Process files
    results = batch_processor.process_directory(
        input_dir, output_dir, 
        document_type=context['params']['document_type'],
        customer_gln=context['params'].get('customer_gln')
    )
    
    # Return results for downstream tasks
    return results

# Define DAG
dag = DAG(
    'edi_processing',
    default_args={
        'owner': 'edi-team',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='EDI file processing workflow',
    schedule_interval='@daily',
    catchup=False
)

# Define tasks
process_orders = PythonOperator(
    task_id='process_orders',
    python_callable=process_edi_files,
    params={'document_type': 'ORDERS'},
    dag=dag
)

process_invoices = PythonOperator(
    task_id='process_invoices',
    python_callable=process_edi_files,
    params={'document_type': 'INVOIC'},
    dag=dag
)

# Set dependencies
process_orders >> process_invoices
```

### Integration with Celery

```python
from celery import Celery
from customization import CustomizationProcessor

# Create Celery app
app = Celery('edi_processor', broker='redis://localhost:6379')

@app.task
def process_edi_file(file_path, document_type, customer_gln=None):
    """Celery task to process EDI file"""
    processor = CustomizationProcessor()
    
    result = processor.process_file(file_path, document_type, customer_gln)
    
    return {
        'success': result.success,
        'xml_output': result.output_xml if result.success else None,
        'errors': result.errors,
        'processing_stats': result.processing_stats
    }

@app.task
def process_edi_batch(file_list, document_type, customer_gln=None):
    """Celery task to process multiple EDI files"""
    from customization.customization_processor import BatchProcessor
    
    batch_processor = BatchProcessor()
    
    results = batch_processor.process_file_list(
        file_list, '/tmp/output', document_type, customer_gln
    )
    
    return results

# Usage
if __name__ == '__main__':
    # Start worker
    app.start()
```

## Testing Integration

### Unit Testing

```python
import unittest
from unittest.mock import Mock, patch
from customization import CustomizationProcessor

class TestCustomizationIntegration(unittest.TestCase):
    
    def setUp(self):
        self.processor = CustomizationProcessor()
        self.sample_data = {
            'message_info': {'type': 'ORDERS'},
            'business_data': {
                'references': {'ON': 'ORDER-001'},
                'dates': {'137': '20240315'},
                'parties': {'BY': {'id': '1234567890123'}}
            }
        }
    
    def test_process_data_success(self):
        """Test successful data processing"""
        result = self.processor.process_data(
            self.sample_data, 'ORDERS', '1234567890123'
        )
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output_xml)
        self.assertEqual(len(result.errors), 0)
    
    def test_process_data_validation_error(self):
        """Test processing with validation errors"""
        # Remove required field
        del self.sample_data['business_data']['references']['ON']
        
        result = self.processor.process_data(
            self.sample_data, 'ORDERS', '1234567890123', 
            validation_level='strict'
        )
        
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
    
    @patch('customization.data_readers.DataReaderFactory.read_data')
    def test_process_file_integration(self, mock_read_data):
        """Test file processing integration"""
        mock_read_data.return_value = self.sample_data
        
        result = self.processor.process_file(
            'test_file.xml', 'ORDERS', '1234567890123'
        )
        
        self.assertTrue(result.success)
        mock_read_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
import pytest
import tempfile
import json
from pathlib import Path
from customization import CustomizationProcessor, ConfigurationManager

@pytest.fixture
def temp_config_dir():
    """Create temporary configuration directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir)
        
        # Create sample configurations
        (config_dir / 'document_types').mkdir()
        (config_dir / 'customers').mkdir()
        (config_dir / 'mappings').mkdir()
        
        # Add sample document type config
        doc_config = {
            'document_type': 'ORDERS',
            'document_code': '850',
            'description': 'Test Orders'
        }
        
        with open(config_dir / 'document_types' / 'ORDERS.json', 'w') as f:
            json.dump(doc_config, f)
        
        yield config_dir

@pytest.fixture
def processor_with_config(temp_config_dir):
    """Create processor with test configuration"""
    config_manager = ConfigurationManager(temp_config_dir)
    return CustomizationProcessor(config_manager)

def test_end_to_end_processing(processor_with_config):
    """Test complete end-to-end processing"""
    sample_data = {
        'message_info': {'type': 'ORDERS'},
        'business_data': {
            'references': {'ON': 'TEST-ORDER-001'},
            'dates': {'137': '20240315'}
        }
    }
    
    result = processor_with_config.process_data(sample_data, 'ORDERS')
    
    assert result.success
    assert 'TEST-ORDER-001' in result.output_xml
    assert len(result.errors) == 0

def test_batch_processing_integration():
    """Test batch processing integration"""
    from customization.customization_processor import BatchProcessor
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = Path(temp_dir) / 'input'
        output_dir = Path(temp_dir) / 'output'
        input_dir.mkdir()
        
        # Create sample files
        for i in range(3):
            sample_file = input_dir / f'order_{i}.json'
            sample_data = {
                'message_info': {'type': 'ORDERS'},
                'business_data': {'references': {'ON': f'ORDER-{i}'}}
            }
            
            with open(sample_file, 'w') as f:
                json.dump(sample_data, f)
        
        # Process batch
        batch_processor = BatchProcessor()
        results = batch_processor.process_directory(
            input_dir, output_dir, 'ORDERS', file_pattern='*.json'
        )
        
        assert results['total_files'] == 3
        assert results['successful_files'] >= 0
        assert results['summary']['processing_completed']
```

## Production Deployment

### Docker Integration

```dockerfile
# Dockerfile for EDI Customization Service
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY edifact_parser/ ./edifact_parser/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  edi-processor:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://user:pass@db:5432/edi
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: edi
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    
volumes:
  postgres_data:
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edi-customization-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: edi-customization
  template:
    metadata:
      labels:
        app: edi-customization
    spec:
      containers:
      - name: edi-processor
        image: edi-customization:latest
        ports:
        - containerPort: 5000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: edi-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: edi-customization-service
spec:
  selector:
    app: edi-customization
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

## Monitoring and Maintenance

### Logging Configuration

```python
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'edi_customization.log',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        'customization': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
```

### Metrics and Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
PROCESSING_REQUESTS = Counter('edi_processing_requests_total', 
                             'Total EDI processing requests', 
                             ['document_type', 'customer_gln', 'status'])

PROCESSING_DURATION = Histogram('edi_processing_duration_seconds',
                               'Time spent processing EDI files',
                               ['document_type'])

ACTIVE_PROCESSORS = Gauge('edi_active_processors',
                         'Number of active EDI processors')

class MonitoredCustomizationProcessor(CustomizationProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ACTIVE_PROCESSORS.inc()
    
    def process_file(self, input_file, document_type, customer_gln=None, **kwargs):
        """Process file with monitoring"""
        start_time = time.time()
        
        try:
            result = super().process_file(input_file, document_type, customer_gln, **kwargs)
            
            # Record metrics
            status = 'success' if result.success else 'failure'
            PROCESSING_REQUESTS.labels(
                document_type=document_type,
                customer_gln=customer_gln or 'default',
                status=status
            ).inc()
            
            PROCESSING_DURATION.labels(document_type=document_type).observe(
                time.time() - start_time
            )
            
            return result
            
        except Exception as e:
            PROCESSING_REQUESTS.labels(
                document_type=document_type,
                customer_gln=customer_gln or 'default',
                status='error'
            ).inc()
            raise

# Start metrics server
start_http_server(8000)
```

### Health Checks

```python
from flask import Flask, jsonify
from customization import CustomizationProcessor, ConfigurationManager

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Basic health check"""
    try:
        # Test processor creation
        processor = CustomizationProcessor()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/ready')
def readiness_check():
    """Readiness check"""
    try:
        # Test configuration loading
        config_manager = ConfigurationManager()
        doc_types = config_manager.list_document_types()
        
        # Test processing capability
        processor = CustomizationProcessor(config_manager)
        
        return jsonify({
            'status': 'ready',
            'document_types': len(doc_types),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

This integration guide provides comprehensive instructions for integrating the EDI Customization Layer into various environments and workflows. Choose the integration patterns that best fit your architecture and requirements.

