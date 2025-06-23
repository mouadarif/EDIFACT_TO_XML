#!/usr/bin/env python3
"""
Basic Usage Example for EDI Customization Layer
===============================================

This example demonstrates the basic usage of the EDI customization layer
to transform comprehensive EDI data into customer-specific XML.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from customization import (
    CustomizationProcessor,
    ConfigurationManager,
    DocumentTypeConfig,
    CustomerConfig,
    MappingConfig,
    create_orders_document_config,
    create_sample_customer_config
)


def basic_usage_example():
    """Demonstrate basic usage of the customization layer"""
    print("EDI Customization Layer - Basic Usage Example")
    print("=" * 50)
    
    # Step 1: Create configuration manager
    print("\\n1. Setting up configuration manager...")
    config_manager = ConfigurationManager()
    
    # Step 2: Add document type configuration
    print("2. Adding document type configuration...")
    orders_config = create_orders_document_config()
    config_manager.add_document_type_config(orders_config)
    
    # Step 3: Add customer configuration
    print("3. Adding customer configuration...")
    customer_config = create_sample_customer_config("1234567890123", "Sample Customer Corp")
    config_manager.add_customer_config(customer_config)
    
    # Step 4: Create mapping configuration
    print("4. Creating mapping configuration...")
    mapping_config = MappingConfig(
        config_name="orders_sample_customer",
        document_type="ORDERS",
        customer_gln="1234567890123",
        target_format="xml",
        field_mappings=[
            {
                "source_path": "business_data.references.ON",
                "target_path": "Header.OrderNumber",
                "transformation_type": "copy",
                "required": True
            },
            {
                "source_path": "business_data.dates.137",
                "target_path": "Header.OrderDate",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "date",
                    "output_format": "%Y-%m-%d"
                }
            },
            {
                "source_path": "business_data.parties.BY",
                "target_path": "Parties.Buyer",
                "transformation_type": "copy"
            },
            {
                "source_path": "business_data.parties.SU",
                "target_path": "Parties.Supplier",
                "transformation_type": "copy"
            },
            {
                "source_path": "business_data.line_items",
                "target_path": "LineItems.LineItem",
                "transformation_type": "copy"
            }
        ]
    )
    config_manager.add_mapping_config(mapping_config)
    
    # Step 5: Create customization processor
    print("5. Creating customization processor...")
    processor = CustomizationProcessor(config_manager)
    
    # Step 6: Create sample EDI data
    print("6. Creating sample EDI data...")
    sample_data = {
        "format": "json",
        "message_info": {
            "type": "ORDERS",
            "reference": "ORD001"
        },
        "interchange_info": {
            "sender_id": "SUPPLIER123",
            "recipient_id": "BUYER456"
        },
        "business_data": {
            "references": {
                "ON": "PO-2024-001"
            },
            "dates": {
                "137": "20240315"
            },
            "parties": {
                "BY": {
                    "id": "1234567890123",
                    "name": "Sample Customer Corp",
                    "address": "123 Business St",
                    "city": "Business City",
                    "postal_code": "12345",
                    "country": "US"
                },
                "SU": {
                    "id": "9876543210987",
                    "name": "Supplier Inc",
                    "address": "456 Supply Ave",
                    "city": "Supply Town",
                    "postal_code": "67890",
                    "country": "US"
                }
            },
            "line_items": [
                {
                    "line_number": "1",
                    "item_id": "ITEM001",
                    "description": "Sample Product A",
                    "quantity": "10",
                    "unit_price": "25.00",
                    "total_amount": "250.00"
                },
                {
                    "line_number": "2",
                    "item_id": "ITEM002",
                    "description": "Sample Product B",
                    "quantity": "5",
                    "unit_price": "50.00",
                    "total_amount": "250.00"
                }
            ]
        },
        "segments": [
            {"tag": "UNB", "position": 1},
            {"tag": "UNH", "position": 2},
            {"tag": "BGM", "position": 3},
            {"tag": "DTM", "position": 4},
            {"tag": "NAD", "position": 5},
            {"tag": "LIN", "position": 6},
            {"tag": "UNT", "position": 7},
            {"tag": "UNZ", "position": 8}
        ]
    }
    
    # Step 7: Process the data
    print("7. Processing EDI data...")
    result = processor.process_data(
        sample_data,
        document_type="ORDERS",
        customer_gln="1234567890123"
    )
    
    # Step 8: Display results
    print("8. Processing Results:")
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Output XML length: {len(result.output_xml)} characters")
        print("\\n   Generated XML:")
        print("   " + "=" * 40)
        print(result.output_xml)
        print("   " + "=" * 40)
    else:
        print(f"   Errors: {result.errors}")
        print(f"   Warnings: {result.warnings}")
    
    print(f"\\n   Processing Stats: {result.processing_stats}")
    print(f"   Metadata: {result.metadata}")
    
    return result


def advanced_usage_example():
    """Demonstrate advanced usage with custom templates"""
    print("\\n\\nEDI Customization Layer - Advanced Usage Example")
    print("=" * 55)
    
    # Create processor
    processor = CustomizationProcessor()
    
    # Create custom XML template
    from customization.xml_customizer import XMLTemplate
    
    custom_template = XMLTemplate(
        name="CustomPurchaseOrder",
        root_element="CustomOrder",
        namespace="http://example.com/custom-orders",
        attributes={
            "version": "2.0",
            "xmlns": "http://example.com/custom-orders"
        },
        structure={
            "OrderInfo": {
                "Number": "string",
                "Date": "string",
                "Currency": "string"
            },
            "Customer": {
                "GLN": "string",
                "Name": "string",
                "ContactInfo": {
                    "Email": "string",
                    "Phone": "string"
                }
            },
            "Items": {
                "Item": [{
                    "SKU": "string",
                    "Name": "string",
                    "Qty": "string",
                    "Price": "string"
                }]
            },
            "Totals": {
                "ItemCount": "string",
                "SubTotal": "string",
                "Tax": "string",
                "Total": "string"
            }
        }
    )
    
    # Add custom template
    processor.add_custom_template(custom_template)
    
    # Create custom mapping
    from customization.mapping_engine import MappingConfiguration, FieldMapping, TransformationType
    
    custom_mappings = [
        FieldMapping(
            source_path="business_data.references.ON",
            target_path="OrderInfo.Number",
            transformation_type=TransformationType.COPY,
            required=True
        ),
        FieldMapping(
            source_path="business_data.dates.137",
            target_path="OrderInfo.Date",
            transformation_type=TransformationType.FORMAT,
            transformation_config={
                "format_type": "date",
                "input_format": "%Y%m%d",
                "output_format": "%Y-%m-%d"
            }
        ),
        FieldMapping(
            source_path="business_data.parties.BY.id",
            target_path="Customer.GLN",
            transformation_type=TransformationType.COPY
        ),
        FieldMapping(
            source_path="business_data.parties.BY.name",
            target_path="Customer.Name",
            transformation_type=TransformationType.COPY
        ),
        FieldMapping(
            source_path="business_data.line_items",
            target_path="Items.Item",
            transformation_type=TransformationType.COPY
        )
    ]
    
    custom_mapping_config = MappingConfiguration(
        document_type="ORDERS",
        customer_gln="CUSTOM123",
        target_structure="CustomPurchaseOrder",
        field_mappings=custom_mappings
    )
    
    processor.add_custom_mapping(custom_mapping_config)
    
    # Sample data for custom processing
    custom_data = {
        "business_data": {
            "references": {"ON": "CUSTOM-ORDER-001"},
            "dates": {"137": "20240320"},
            "parties": {
                "BY": {
                    "id": "CUSTOM123",
                    "name": "Custom Client Ltd"
                }
            },
            "line_items": [
                {
                    "item_id": "SKU001",
                    "description": "Custom Product",
                    "quantity": "3",
                    "unit_price": "99.99"
                }
            ]
        }
    }
    
    # Process with custom template
    result = processor.process_data(
        custom_data,
        document_type="ORDERS",
        customer_gln="CUSTOM123",
        output_template="CustomPurchaseOrder"
    )
    
    print("Advanced Processing Results:")
    if result.success:
        print("Custom XML Generated:")
        print("=" * 30)
        print(result.output_xml)
        print("=" * 30)
    else:
        print(f"Errors: {result.errors}")


def batch_processing_example():
    """Demonstrate batch processing capabilities"""
    print("\\n\\nEDI Customization Layer - Batch Processing Example")
    print("=" * 55)
    
    from customization.customization_processor import BatchProcessor
    
    # Create batch processor
    batch_processor = BatchProcessor()
    
    # Create sample files for batch processing
    sample_files_dir = Path("sample_batch_files")
    sample_files_dir.mkdir(exist_ok=True)
    
    # Create sample JSON files
    for i in range(3):
        sample_file = sample_files_dir / f"order_{i+1}.json"
        sample_data = {
            "message_info": {"type": "ORDERS"},
            "business_data": {
                "references": {"ON": f"ORDER-{i+1:03d}"},
                "dates": {"137": "20240320"},
                "parties": {
                    "BY": {"id": "1234567890123", "name": f"Customer {i+1}"}
                },
                "line_items": [
                    {
                        "line_number": "1",
                        "item_id": f"ITEM{i+1:03d}",
                        "description": f"Product {i+1}",
                        "quantity": str((i+1) * 2),
                        "unit_price": "10.00"
                    }
                ]
            }
        }
        
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
    
    print(f"Created {len(list(sample_files_dir.glob('*.json')))} sample files")
    
    # Process batch
    output_dir = Path("batch_output")
    results = batch_processor.process_directory(
        sample_files_dir,
        output_dir,
        document_type="ORDERS",
        customer_gln="1234567890123",
        file_pattern="*.json"
    )
    
    print("\\nBatch Processing Results:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful_files']}")
    print(f"Failed: {results['failed_files']}")
    print(f"Success rate: {results['summary']['success_rate']:.2%}")
    
    # Show generated files
    if output_dir.exists():
        output_files = list(output_dir.glob("*.xml"))
        print(f"\\nGenerated {len(output_files)} XML files:")
        for file_path in output_files:
            print(f"  - {file_path.name}")


if __name__ == "__main__":
    try:
        # Run basic example
        basic_result = basic_usage_example()
        
        # Run advanced example
        advanced_usage_example()
        
        # Run batch processing example
        batch_processing_example()
        
        print("\\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\\nError running examples: {e}")
        import traceback
        traceback.print_exc()

