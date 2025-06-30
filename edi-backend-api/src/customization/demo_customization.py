#!/usr/bin/env python3
"""
EDI Customization Layer - Complete Demonstration
===============================================

This script demonstrates the complete functionality of the EDI Customization Layer
with real-world examples and comprehensive testing.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from customization import (
    CustomizationProcessor,
    ConfigurationManager,
    DocumentTypeConfig,
    CustomerConfig,
    MappingConfig,
    create_orders_document_config,
    create_invoice_document_config,
    create_sample_customer_config
)


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")


def create_comprehensive_sample_data():
    """Create comprehensive sample EDI data for testing"""
    return {
        "format": "json",
        "message_info": {
            "type": "ORDERS",
            "reference": "ORD-2024-001",
            "version": "D.96A",
            "control_number": "000001"
        },
        "interchange_info": {
            "sender_id": "SUPPLIER123",
            "sender_qualifier": "ZZ",
            "recipient_id": "BUYER456",
            "recipient_qualifier": "ZZ",
            "interchange_control_number": "000000001",
            "acknowledgment_requested": "0",
            "test_indicator": "P"
        },
        "business_data": {
            "references": {
                "ON": "PO-2024-001",
                "CR": "CUST-REF-001",
                "PJ": "PROJECT-A",
                "CC": "COST-CENTER-100"
            },
            "dates": {
                "137": "20240315",  # Order date
                "2": "20240322",    # Delivery date
                "64": "20240320"    # Requested date
            },
            "currencies": {
                "order_currency": "USD",
                "pricing_currency": "USD"
            },
            "parties": {
                "BY": {
                    "id": "1234567890123",
                    "name": "Global Retail Chain Inc.",
                    "address": "123 Business Boulevard",
                    "city": "Commerce City",
                    "state": "CA",
                    "postal_code": "90210",
                    "country": "US",
                    "contact": {
                        "name": "John Smith",
                        "phone": "+1-555-0123",
                        "email": "john.smith@globalretail.com"
                    }
                },
                "SU": {
                    "id": "9876543210987",
                    "name": "Premium Suppliers Ltd.",
                    "address": "456 Supply Street",
                    "city": "Manufacturing Town",
                    "state": "TX",
                    "postal_code": "75001",
                    "country": "US",
                    "contact": {
                        "name": "Sarah Johnson",
                        "phone": "+1-555-0456",
                        "email": "sarah.johnson@premiumsuppliers.com"
                    }
                },
                "DP": {
                    "id": "5555555555555",
                    "name": "Distribution Center West",
                    "address": "789 Warehouse Way",
                    "city": "Logistics City",
                    "state": "NV",
                    "postal_code": "89101",
                    "country": "US"
                }
            },
            "line_items": [
                {
                    "line_number": "1",
                    "item_id": "SKU-WIDGET-001",
                    "supplier_item_id": "SUP-WID-001",
                    "customer_item_id": "CUST-WID-001",
                    "description": "Premium Widget - Blue",
                    "category": "WIDGETS",
                    "quantity": "100",
                    "unit_of_measure": "EA",
                    "unit_price": "25.50",
                    "total_amount": "2550.00",
                    "tax_rate": "8.25",
                    "tax_amount": "210.38",
                    "delivery_date": "20240322",
                    "special_instructions": "Handle with care"
                },
                {
                    "line_number": "2",
                    "item_id": "SKU-GADGET-002",
                    "supplier_item_id": "SUP-GAD-002",
                    "customer_item_id": "CUST-GAD-002",
                    "description": "Advanced Gadget - Red",
                    "category": "GADGETS",
                    "quantity": "50",
                    "unit_of_measure": "EA",
                    "unit_price": "75.00",
                    "total_amount": "3750.00",
                    "tax_rate": "8.25",
                    "tax_amount": "309.38",
                    "delivery_date": "20240325",
                    "special_instructions": "Fragile - This side up"
                },
                {
                    "line_number": "3",
                    "item_id": "SKU-TOOL-003",
                    "supplier_item_id": "SUP-TOO-003",
                    "customer_item_id": "CUST-TOO-003",
                    "description": "Professional Tool Set",
                    "category": "TOOLS",
                    "quantity": "25",
                    "unit_of_measure": "SET",
                    "unit_price": "150.00",
                    "total_amount": "3750.00",
                    "tax_rate": "8.25",
                    "tax_amount": "309.38",
                    "delivery_date": "20240330",
                    "special_instructions": "Requires signature"
                }
            ],
            "totals": {
                "79": "10050.00",   # Total line items amount
                "125": "10050.00",  # Subtotal
                "124": "829.14",    # Total tax
                "128": "10879.14"   # Total payable amount
            },
            "payment_terms": {
                "terms": "NET30",
                "discount_percent": "2.0",
                "discount_days": "10",
                "net_days": "30"
            },
            "shipping_info": {
                "method": "GROUND",
                "carrier": "UPS",
                "service_level": "STANDARD",
                "special_instructions": "Deliver to loading dock"
            },
            "free_text": {
                "DEL": "Please coordinate delivery with receiving department",
                "GEN": "This is a priority order for Q2 launch",
                "PAC": "Use eco-friendly packaging when possible"
            }
        },
        "segments": [
            {"tag": "UNB", "position": 1, "elements": ["UNOC", "3", "SUPPLIER123", "ZZ", "BUYER456", "ZZ"]},
            {"tag": "UNH", "position": 2, "elements": ["000001", "ORDERS", "D", "96A", "UN"]},
            {"tag": "BGM", "position": 3, "elements": ["220", "PO-2024-001", "9"]},
            {"tag": "DTM", "position": 4, "elements": ["137", "20240315", "102"]},
            {"tag": "DTM", "position": 5, "elements": ["2", "20240322", "102"]},
            {"tag": "RFF", "position": 6, "elements": ["CR", "CUST-REF-001"]},
            {"tag": "NAD", "position": 7, "elements": ["BY", "1234567890123", "", "", "Global Retail Chain Inc."]},
            {"tag": "NAD", "position": 8, "elements": ["SU", "9876543210987", "", "", "Premium Suppliers Ltd."]},
            {"tag": "NAD", "position": 9, "elements": ["DP", "5555555555555", "", "", "Distribution Center West"]},
            {"tag": "CUX", "position": 10, "elements": ["2", "USD", "4"]},
            {"tag": "PAT", "position": 11, "elements": ["3", "", "", "5", "2", "D", "10"]},
            {"tag": "TDT", "position": 12, "elements": ["20", "", "", "", "UPS", "", "GROUND"]},
            {"tag": "LIN", "position": 13, "elements": ["1", "", "SKU-WIDGET-001", "SA"]},
            {"tag": "QTY", "position": 14, "elements": ["21", "100", "EA"]},
            {"tag": "PRI", "position": 15, "elements": ["AAA", "25.50", "1", "", "1", "EA"]},
            {"tag": "LIN", "position": 16, "elements": ["2", "", "SKU-GADGET-002", "SA"]},
            {"tag": "QTY", "position": 17, "elements": ["21", "50", "EA"]},
            {"tag": "PRI", "position": 18, "elements": ["AAA", "75.00", "1", "", "1", "EA"]},
            {"tag": "LIN", "position": 19, "elements": ["3", "", "SKU-TOOL-003", "SA"]},
            {"tag": "QTY", "position": 20, "elements": ["21", "25", "SET"]},
            {"tag": "PRI", "position": 21, "elements": ["AAA", "150.00", "1", "", "1", "SET"]},
            {"tag": "UNS", "position": 22, "elements": ["S"]},
            {"tag": "MOA", "position": 23, "elements": ["79", "10050.00"]},
            {"tag": "MOA", "position": 24, "elements": ["125", "10050.00"]},
            {"tag": "MOA", "position": 25, "elements": ["124", "829.14"]},
            {"tag": "MOA", "position": 26, "elements": ["128", "10879.14"]},
            {"tag": "UNT", "position": 27, "elements": ["26", "000001"]},
            {"tag": "UNZ", "position": 28, "elements": ["1", "000000001"]}
        ]
    }


def demo_basic_functionality():
    """Demonstrate basic customization functionality"""
    print_section("BASIC FUNCTIONALITY DEMONSTRATION")
    
    # Step 1: Create configuration manager
    print_subsection("1. Configuration Setup")
    config_manager = ConfigurationManager()
    print("✓ Configuration manager created")
    
    # Step 2: Add document type configurations
    print_subsection("2. Document Type Configuration")
    orders_config = create_orders_document_config()
    config_manager.add_document_type_config(orders_config)
    print(f"✓ Added ORDERS document configuration")
    
    invoice_config = create_invoice_document_config()
    config_manager.add_document_type_config(invoice_config)
    print(f"✓ Added INVOIC document configuration")
    
    # Step 3: Add customer configurations
    print_subsection("3. Customer Configuration")
    customer1 = create_sample_customer_config("1234567890123", "Global Retail Chain")
    config_manager.add_customer_config(customer1)
    print(f"✓ Added customer: {customer1.customer_name}")
    
    customer2 = create_sample_customer_config("9876543210987", "Manufacturing Corp")
    config_manager.add_customer_config(customer2)
    print(f"✓ Added customer: {customer2.customer_name}")
    
    # Step 4: Create comprehensive mapping
    print_subsection("4. Mapping Configuration")
    comprehensive_mapping = MappingConfig(
        config_name="comprehensive_orders_mapping",
        document_type="ORDERS",
        customer_gln="1234567890123",
        target_format="xml",
        field_mappings=[
            # Header information
            {
                "source_path": "business_data.references.ON",
                "target_path": "Header.OrderNumber",
                "transformation_type": "copy",
                "required": True,
                "description": "Purchase order number"
            },
            {
                "source_path": "business_data.dates.137",
                "target_path": "Header.OrderDate",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "date",
                    "input_format": "%Y%m%d",
                    "output_format": "%Y-%m-%d"
                },
                "required": True,
                "description": "Order date in ISO format"
            },
            {
                "source_path": "business_data.dates.2",
                "target_path": "Header.RequestedDeliveryDate",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "date",
                    "input_format": "%Y%m%d",
                    "output_format": "%Y-%m-%d"
                },
                "required": False,
                "default_value": "",
                "description": "Requested delivery date"
            },
            {
                "source_path": "business_data.references.CR",
                "target_path": "Header.CustomerReference",
                "transformation_type": "copy",
                "required": False,
                "default_value": "",
                "description": "Customer reference number"
            },
            {
                "source_path": "business_data.currencies.order_currency",
                "target_path": "Header.Currency",
                "transformation_type": "copy",
                "required": False,
                "default_value": "USD",
                "description": "Order currency"
            },
            # Party information
            {
                "source_path": "business_data.parties.BY",
                "target_path": "Parties.Buyer",
                "transformation_type": "copy",
                "required": True,
                "description": "Buyer party information"
            },
            {
                "source_path": "business_data.parties.SU",
                "target_path": "Parties.Supplier",
                "transformation_type": "copy",
                "required": True,
                "description": "Supplier party information"
            },
            {
                "source_path": "business_data.parties.DP",
                "target_path": "Parties.DeliveryPoint",
                "transformation_type": "copy",
                "required": False,
                "default_value": {},
                "description": "Delivery point information"
            },
            # Line items
            {
                "source_path": "business_data.line_items",
                "target_path": "LineItems.LineItem",
                "transformation_type": "copy",
                "required": True,
                "description": "Order line items"
            },
            # Totals
            {
                "source_path": "business_data.totals.125",
                "target_path": "Summary.SubTotal",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "number",
                    "decimal_places": 2
                },
                "required": False,
                "default_value": "0.00",
                "description": "Order subtotal"
            },
            {
                "source_path": "business_data.totals.124",
                "target_path": "Summary.TotalTax",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "number",
                    "decimal_places": 2
                },
                "required": False,
                "default_value": "0.00",
                "description": "Total tax amount"
            },
            {
                "source_path": "business_data.totals.128",
                "target_path": "Summary.TotalAmount",
                "transformation_type": "format",
                "transformation_config": {
                    "format_type": "number",
                    "decimal_places": 2
                },
                "required": True,
                "default_value": "0.00",
                "description": "Total payable amount"
            },
            # Additional information
            {
                "source_path": "business_data.payment_terms",
                "target_path": "PaymentTerms",
                "transformation_type": "copy",
                "required": False,
                "default_value": {},
                "description": "Payment terms information"
            },
            {
                "source_path": "business_data.shipping_info",
                "target_path": "ShippingInfo",
                "transformation_type": "copy",
                "required": False,
                "default_value": {},
                "description": "Shipping information"
            },
            {
                "source_path": "business_data.free_text",
                "target_path": "Notes",
                "transformation_type": "copy",
                "required": False,
                "default_value": {},
                "description": "Free text notes"
            }
        ],
        transformation_rules={
            "include_empty_elements": True,
            "date_format": "ISO",
            "number_format": "decimal_2",
            "preserve_structure": True
        },
        validation_enabled=True
    )
    
    config_manager.add_mapping_config(comprehensive_mapping)
    print("✓ Added comprehensive mapping configuration")
    
    # Step 5: Create processor
    print_subsection("5. Processor Creation")
    processor = CustomizationProcessor(config_manager)
    print("✓ Customization processor created")
    
    # Step 6: Process sample data
    print_subsection("6. Data Processing")
    sample_data = create_comprehensive_sample_data()
    
    result = processor.process_data(
        sample_data,
        document_type="ORDERS",
        customer_gln="1234567890123",
        validation_level="standard"
    )
    
    print(f"✓ Processing completed")
    print(f"  Success: {result.success}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")
    print(f"  XML Size: {len(result.output_xml)} characters")
    
    if result.errors:
        print("  Errors found:")
        for error in result.errors:
            print(f"    - {error}")
    
    if result.warnings:
        print("  Warnings found:")
        for warning in result.warnings:
            print(f"    - {warning}")
    
    # Step 7: Display processing statistics
    print_subsection("7. Processing Statistics")
    for key, value in result.processing_stats.items():
        print(f"  {key}: {value}")
    
    # Step 8: Show sample XML output
    print_subsection("8. Sample XML Output")
    if result.success and result.output_xml:
        # Show first 1000 characters of XML
        xml_preview = result.output_xml[:1000]
        if len(result.output_xml) > 1000:
            xml_preview += "\\n... (truncated)"
        
        print("Generated XML Preview:")
        print("-" * 40)
        print(xml_preview)
        print("-" * 40)
    
    return result


def demo_advanced_features():
    """Demonstrate advanced customization features"""
    print_section("ADVANCED FEATURES DEMONSTRATION")
    
    # Custom XML template
    print_subsection("1. Custom XML Template")
    from customization.xml_customizer import XMLTemplate
    
    custom_template = XMLTemplate(
        name="EnhancedPurchaseOrder",
        root_element="EnhancedOrder",
        namespace="http://example.com/enhanced-orders/v2",
        attributes={
            "version": "2.0",
            "xmlns": "http://example.com/enhanced-orders/v2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        },
        structure={
            "OrderHeader": {
                "OrderInfo": {
                    "Number": "string",
                    "Date": "string",
                    "Currency": "string",
                    "Priority": "string",
                    "Type": "string"
                },
                "References": {
                    "CustomerReference": "string",
                    "ProjectCode": "string",
                    "CostCenter": "string"
                },
                "Dates": {
                    "OrderDate": "string",
                    "RequestedDate": "string",
                    "PromisedDate": "string"
                }
            },
            "BusinessPartners": {
                "Buyer": {
                    "ID": "string",
                    "Name": "string",
                    "Address": {
                        "Street": "string",
                        "City": "string",
                        "State": "string",
                        "PostalCode": "string",
                        "Country": "string"
                    },
                    "Contact": {
                        "Name": "string",
                        "Phone": "string",
                        "Email": "string"
                    }
                },
                "Supplier": {
                    "ID": "string",
                    "Name": "string",
                    "Address": {
                        "Street": "string",
                        "City": "string",
                        "State": "string",
                        "PostalCode": "string",
                        "Country": "string"
                    },
                    "Contact": {
                        "Name": "string",
                        "Phone": "string",
                        "Email": "string"
                    }
                },
                "DeliveryPoint": {
                    "ID": "string",
                    "Name": "string",
                    "Address": {
                        "Street": "string",
                        "City": "string",
                        "State": "string",
                        "PostalCode": "string",
                        "Country": "string"
                    }
                }
            },
            "OrderDetails": {
                "LineItems": {
                    "LineItem": [{
                        "LineNumber": "string",
                        "ItemIdentification": {
                            "SupplierItemID": "string",
                            "CustomerItemID": "string",
                            "StandardItemID": "string"
                        },
                        "ItemDescription": {
                            "Description": "string",
                            "Category": "string",
                            "Specifications": "string"
                        },
                        "Quantity": {
                            "Ordered": "string",
                            "UnitOfMeasure": "string"
                        },
                        "Pricing": {
                            "UnitPrice": "string",
                            "ExtendedPrice": "string",
                            "Currency": "string"
                        },
                        "Tax": {
                            "Rate": "string",
                            "Amount": "string"
                        },
                        "Delivery": {
                            "RequestedDate": "string",
                            "PromisedDate": "string",
                            "Instructions": "string"
                        }
                    }]
                }
            },
            "OrderSummary": {
                "Totals": {
                    "LineItemsCount": "string",
                    "SubTotal": "string",
                    "TotalTax": "string",
                    "TotalAmount": "string",
                    "Currency": "string"
                },
                "Terms": {
                    "PaymentTerms": {
                        "Terms": "string",
                        "DiscountPercent": "string",
                        "DiscountDays": "string",
                        "NetDays": "string"
                    },
                    "ShippingTerms": {
                        "Method": "string",
                        "Carrier": "string",
                        "ServiceLevel": "string",
                        "Instructions": "string"
                    }
                }
            },
            "AdditionalInfo": {
                "Notes": {
                    "DeliveryNotes": "string",
                    "GeneralNotes": "string",
                    "PackagingNotes": "string"
                },
                "Metadata": {
                    "ProcessingTimestamp": "string",
                    "ProcessingVersion": "string",
                    "SourceSystem": "string"
                }
            }
        }
    )
    
    processor = CustomizationProcessor()
    processor.add_custom_template(custom_template)
    print("✓ Custom XML template added")
    
    # Process with custom template
    sample_data = create_comprehensive_sample_data()
    
    result = processor.process_data(
        sample_data,
        document_type="ORDERS",
        customer_gln="1234567890123",
        output_template="EnhancedPurchaseOrder"
    )
    
    print(f"✓ Processing with custom template completed")
    print(f"  Success: {result.success}")
    print(f"  XML Size: {len(result.output_xml)} characters")
    
    if result.success:
        print("\\nCustom XML Preview:")
        print("-" * 40)
        print(result.output_xml[:800] + "\\n... (truncated)")
        print("-" * 40)


def demo_batch_processing():
    """Demonstrate batch processing capabilities"""
    print_section("BATCH PROCESSING DEMONSTRATION")
    
    from customization.customization_processor import BatchProcessor
    
    # Create temporary directory with sample files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = Path(temp_dir) / "input"
        output_dir = Path(temp_dir) / "output"
        input_dir.mkdir()
        
        print_subsection("1. Creating Sample Files")
        
        # Create multiple sample files
        sample_files = []
        for i in range(5):
            sample_data = create_comprehensive_sample_data()
            # Modify data to make each file unique
            sample_data["business_data"]["references"]["ON"] = f"PO-2024-{i+1:03d}"
            sample_data["business_data"]["totals"]["128"] = f"{10000 + (i * 1000)}.00"
            
            sample_file = input_dir / f"order_{i+1}.json"
            with open(sample_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            
            sample_files.append(sample_file)
        
        print(f"✓ Created {len(sample_files)} sample files")
        
        print_subsection("2. Batch Processing")
        
        # Create batch processor
        batch_processor = BatchProcessor()
        
        # Process all files
        results = batch_processor.process_directory(
            input_dir,
            output_dir,
            document_type="ORDERS",
            customer_gln="1234567890123",
            file_pattern="*.json"
        )
        
        print(f"✓ Batch processing completed")
        print(f"  Total files: {results['total_files']}")
        print(f"  Successful: {results['successful_files']}")
        print(f"  Failed: {results['failed_files']}")
        print(f"  Success rate: {results['summary']['success_rate']:.2%}")
        
        # Show generated files
        if output_dir.exists():
            output_files = list(output_dir.glob("*.xml"))
            print(f"\\n✓ Generated {len(output_files)} XML files:")
            for file_path in output_files:
                file_size = file_path.stat().st_size
                print(f"  - {file_path.name} ({file_size:,} bytes)")


def demo_validation_levels():
    """Demonstrate different validation levels"""
    print_section("VALIDATION LEVELS DEMONSTRATION")
    
    processor = CustomizationProcessor()
    
    # Create data with intentional issues
    problematic_data = create_comprehensive_sample_data()
    # Remove required field
    del problematic_data["business_data"]["references"]["ON"]
    # Add invalid date
    problematic_data["business_data"]["dates"]["137"] = "INVALID-DATE"
    
    validation_levels = ["none", "basic", "standard", "strict"]
    
    for level in validation_levels:
        print_subsection(f"Validation Level: {level.upper()}")
        
        result = processor.process_data(
            problematic_data,
            document_type="ORDERS",
            customer_gln="1234567890123",
            validation_level=level
        )
        
        print(f"  Success: {result.success}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Warnings: {len(result.warnings)}")
        
        if result.errors:
            print("  Error details:")
            for error in result.errors[:3]:  # Show first 3 errors
                print(f"    - {error}")
        
        if result.warnings:
            print("  Warning details:")
            for warning in result.warnings[:3]:  # Show first 3 warnings
                print(f"    - {warning}")


def demo_configuration_management():
    """Demonstrate configuration management features"""
    print_section("CONFIGURATION MANAGEMENT DEMONSTRATION")
    
    print_subsection("1. Configuration Export/Import")
    
    config_manager = ConfigurationManager()
    
    # Add some configurations
    config_manager.add_document_type_config(create_orders_document_config())
    config_manager.add_customer_config(create_sample_customer_config("1234567890123", "Test Customer"))
    
    # Export configuration
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        config_manager.export_configuration(temp_file.name)
        export_file = temp_file.name
    
    print(f"✓ Configuration exported to {export_file}")
    
    # Create new config manager and import
    new_config_manager = ConfigurationManager()
    new_config_manager.import_configuration(export_file)
    
    print(f"✓ Configuration imported successfully")
    print(f"  Document types: {len(new_config_manager.list_document_types())}")
    print(f"  Customers: {len(new_config_manager.list_customers())}")
    
    # Clean up
    Path(export_file).unlink()
    
    print_subsection("2. Configuration Validation")
    
    validation_result = config_manager.validate_configuration()
    print(f"✓ Configuration validation completed")
    print(f"  Valid: {validation_result['is_valid']}")
    print(f"  Errors: {len(validation_result['errors'])}")
    print(f"  Warnings: {len(validation_result['warnings'])}")


def main():
    """Main demonstration function"""
    print("EDI CUSTOMIZATION LAYER - COMPLETE DEMONSTRATION")
    print("=" * 60)
    print(f"Demonstration started at: {datetime.now().isoformat()}")
    
    try:
        # Run all demonstrations
        basic_result = demo_basic_functionality()
        demo_advanced_features()
        demo_batch_processing()
        demo_validation_levels()
        demo_configuration_management()
        
        print_section("DEMONSTRATION SUMMARY")
        print("✓ All demonstrations completed successfully!")
        print(f"✓ Basic processing result: {'SUCCESS' if basic_result.success else 'FAILED'}")
        print(f"✓ Generated XML size: {len(basic_result.output_xml):,} characters")
        print(f"✓ Processing time: {basic_result.metadata.get('processing_duration', 'N/A')}")
        
        # Save sample output
        output_file = Path("sample_customized_output.xml")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(basic_result.output_xml)
        
        print(f"✓ Sample output saved to: {output_file}")
        
        print(f"\\nDemonstration completed at: {datetime.now().isoformat()}")
        
    except Exception as e:
        print(f"\\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

