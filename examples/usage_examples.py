#!/usr/bin/env python3
"""
EDIFACT Parser Examples
======================

This module contains practical examples of using the EDIFACT parser
for various common scenarios and message types.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from edifact_parser import (
    EDIFACTToXMLConverter,
    convert_edifact_to_xml,
    parse_edifact_message,
    validate_edifact_message,
    ValidationLevel,
    setup_parser_logging
)


# Sample EDIFACT messages for testing
SAMPLE_ORDERS_MESSAGE = """UNA:+.?'UNB+UNOC:3+SENDER123+RECEIVER456+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123456+9'DTM+137:20231201:102'RFF+ON:PO123456'NAD+BY+BUYER123++BUYER COMPANY+BUYER STREET 1+BUYER CITY++12345+FR'NAD+SU+SUPPLIER456++SUPPLIER COMPANY+SUPPLIER STREET 1+SUPPLIER CITY++67890+DE'CTA+IC+:JOHN DOE'COM+TE+33123456789'CUX+2:EUR:4'LIN+1++PRODUCT123:EN'PIA+1+GTIN123456789:GTIN'IMD+F++:::PRODUCT DESCRIPTION'QTY+21:100:PCE'PRI+AAA:10.50:EUR'MOA+203:1050.00:EUR'LIN+2++PRODUCT456:EN'PIA+1+GTIN987654321:GTIN'IMD+F++:::ANOTHER PRODUCT'QTY+21:50:PCE'PRI+AAA:25.00:EUR'MOA+203:1250.00:EUR'UNS+S'CNT+2:2'MOA+79:2300.00:EUR'UNT+21+1'UNZ+1+1'"""

SAMPLE_INVOICE_MESSAGE = """UNA:+.?'UNB+UNOC:3+SUPPLIER456+BUYER123+20231205:1400+2'UNH+2+INVOIC:D:03B:UN:EAN008'BGM+380+INV123456+9'DTM+137:20231205:102'DTM+35:20231210:102'RFF+ON:PO123456'RFF+DQ:DN789'NAD+SU+SUPPLIER456++SUPPLIER COMPANY+SUPPLIER STREET 1+SUPPLIER CITY++67890+DE'NAD+BY+BUYER123++BUYER COMPANY+BUYER STREET 1+BUYER CITY++12345+FR'CUX+2:EUR:4'LIN+1++PRODUCT123:EN'QTY+47:100:PCE'PRI+AAA:10.50:EUR'MOA+203:1050.00:EUR'TAX+7+VAT+++:::20.00:210.00'LIN+2++PRODUCT456:EN'QTY+47:50:PCE'PRI+AAA:25.00:EUR'MOA+203:1250.00:EUR'TAX+7+VAT+++:::20.00:250.00'UNS+S'CNT+2:2'MOA+125:2300.00:EUR'MOA+124:460.00:EUR'MOA+128:2760.00:EUR'UNT+19+2'UNZ+1+2'"""

SAMPLE_DESADV_MESSAGE = """UNA:+.?'UNB+UNOC:3+SUPPLIER456+BUYER123+20231203:1000+3'UNH+3+DESADV:D:03B:UN:EAN008'BGM+351+DN789+9'DTM+137:20231203:102'DTM+11:20231204:102'RFF+ON:PO123456'NAD+SU+SUPPLIER456++SUPPLIER COMPANY'NAD+BY+BUYER123++BUYER COMPANY'NAD+DP+WAREHOUSE789++DELIVERY WAREHOUSE+WAREHOUSE STREET 1+WAREHOUSE CITY++54321+FR'TDT+20++:TRUCK'LOC+7+WAREHOUSE789'LIN+1++PRODUCT123:EN'QTY+12:100:PCE'QTY+46:100:PCE'PCI+33E'GIN+BX+BATCH123'LIN+2++PRODUCT456:EN'QTY+12:50:PCE'QTY+46:50:PCE'PCI+33E'GIN+BX+BATCH456'UNS+S'CNT+2:2'UNT+16+3'UNZ+1+3'"""


def example_basic_conversion():
    """Example 1: Basic EDIFACT to XML conversion"""
    print("=== Example 1: Basic EDIFACT to XML Conversion ===")
    
    # Simple conversion using convenience function
    xml_result = convert_edifact_to_xml(SAMPLE_ORDERS_MESSAGE)
    
    print("EDIFACT Input (first 100 chars):")
    print(SAMPLE_ORDERS_MESSAGE[:100] + "...")
    print("\nXML Output (first 500 chars):")
    print(xml_result[:500] + "...")
    print("\n" + "="*60 + "\n")


def example_detailed_parsing():
    """Example 2: Detailed parsing with data extraction"""
    print("=== Example 2: Detailed Parsing with Data Extraction ===")
    
    # Parse message and extract structured data
    data = parse_edifact_message(SAMPLE_ORDERS_MESSAGE)
    
    print("Message Information:")
    print(f"  Type: {data['message_info']['type']}")
    print(f"  Version: {data['message_info']['version']}")
    print(f"  Reference: {data['message_info']['reference']}")
    
    print("\nInterchange Information:")
    print(f"  Sender: {data['interchange_info']['sender_id']}")
    print(f"  Recipient: {data['interchange_info']['recipient_id']}")
    print(f"  Date: {data['interchange_info']['preparation_date']}")
    
    print("\nBusiness Data:")
    business_data = data.get('business_data', {})
    if 'parties' in business_data:
        print("  Parties:")
        for qualifier, party in business_data['parties'].items():
            print(f"    {qualifier}: {party.get('name', 'N/A')}")
    
    if 'line_items' in business_data:
        print(f"  Line Items: {len(business_data['line_items'])}")
    
    print("\nSegment Summary:")
    segment_summary = data.get('segment_summary', {})
    print(f"  Total Segments: {segment_summary.get('total_segments', 0)}")
    print(f"  Segment Types: {list(segment_summary.get('segment_types', {}).keys())}")
    
    print("\n" + "="*60 + "\n")


def example_validation():
    """Example 3: Message validation"""
    print("=== Example 3: Message Validation ===")
    
    # Validate a correct message
    print("Validating correct ORDERS message:")
    validation_result = validate_edifact_message(SAMPLE_ORDERS_MESSAGE)
    
    print(f"  Valid: {validation_result['is_valid']}")
    print(f"  Errors: {validation_result['error_count']}")
    print(f"  Warnings: {validation_result['warning_count']}")
    print(f"  Summary: {validation_result['summary']}")
    
    # Validate an invalid message
    print("\nValidating invalid message:")
    invalid_message = "UNB+INCOMPLETE+MESSAGE"
    validation_result = validate_edifact_message(invalid_message)
    
    print(f"  Valid: {validation_result['is_valid']}")
    print(f"  Errors: {validation_result['error_count']}")
    print(f"  Summary: {validation_result['summary']}")
    
    if validation_result['messages']:
        print("  First few validation messages:")
        for msg in validation_result['messages'][:3]:
            print(f"    - {msg}")
    
    print("\n" + "="*60 + "\n")


def example_different_message_types():
    """Example 4: Processing different message types"""
    print("=== Example 4: Processing Different Message Types ===")
    
    messages = {
        "ORDERS (Purchase Order)": SAMPLE_ORDERS_MESSAGE,
        "INVOIC (Invoice)": SAMPLE_INVOICE_MESSAGE,
        "DESADV (Despatch Advice)": SAMPLE_DESADV_MESSAGE
    }
    
    for msg_type, content in messages.items():
        print(f"Processing {msg_type}:")
        
        data = parse_edifact_message(content)
        
        print(f"  Message Type: {data['message_info']['type']}")
        print(f"  Segments: {data['segment_summary']['total_segments']}")
        
        # Extract specific business data
        business_data = data.get('business_data', {})
        
        if 'document_info' in business_data:
            doc_info = business_data['document_info']
            print(f"  Document Number: {doc_info.get('number', 'N/A')}")
        
        if 'parties' in business_data:
            party_count = len(business_data['parties'])
            print(f"  Parties: {party_count}")
        
        if 'line_items' in business_data:
            item_count = len(business_data['line_items'])
            print(f"  Line Items: {item_count}")
        
        print()
    
    print("="*60 + "\n")


def example_custom_configuration():
    """Example 5: Using custom configuration"""
    print("=== Example 5: Custom Configuration ===")
    
    # Create converter with custom settings
    converter = EDIFACTToXMLConverter(
        validation_level=ValidationLevel.STRICT,
        generate_empty_tags=True,
        use_semantic_names=True,
        pretty_print=True,
        include_statistics=True,
        include_validation_info=True
    )
    
    print("Converting with strict validation and full options:")
    
    # Convert message
    xml_result = converter.convert_string(SAMPLE_ORDERS_MESSAGE)
    
    # Get statistics
    stats = converter.get_statistics()
    
    print(f"  Processing time: {stats.get('processing_time', 0):.3f} seconds")
    print(f"  Total segments: {stats.get('total_segments', 0)}")
    print(f"  Total elements: {stats.get('total_elements', 0)}")
    print(f"  File size: {stats.get('file_size', 0)} bytes")
    
    # Show XML structure info
    print(f"  XML length: {len(xml_result)} characters")
    print(f"  Contains statistics: {'ParsingStatistics' in xml_result}")
    print(f"  Contains validation: {'ValidationInfo' in xml_result}")
    
    print("\n" + "="*60 + "\n")


def example_multiple_output_formats():
    """Example 6: Multiple output formats"""
    print("=== Example 6: Multiple Output Formats ===")
    
    converter = EDIFACTToXMLConverter()
    
    formats = ['xml', 'json', 'csv']
    
    for fmt in formats:
        print(f"Converting to {fmt.upper()}:")
        
        try:
            result = converter.convert_to_format(SAMPLE_ORDERS_MESSAGE, fmt)
            
            print(f"  Output length: {len(result)} characters")
            print(f"  First 200 chars: {result[:200]}...")
            
            if fmt == 'json':
                import json
                # Validate JSON
                json.loads(result)
                print("  ✓ Valid JSON format")
            elif fmt == 'csv':
                lines = result.split('\n')
                print(f"  CSV lines: {len(lines)}")
            elif fmt == 'xml':
                print("  ✓ XML format generated")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    print("="*60 + "\n")


def example_error_handling():
    """Example 7: Error handling"""
    print("=== Example 7: Error Handling ===")
    
    converter = EDIFACTToXMLConverter()
    
    # Test various error conditions
    test_cases = [
        ("Empty content", ""),
        ("Invalid content", "This is not EDIFACT"),
        ("Incomplete UNB", "UNB+INCOMPLETE"),
        ("Missing segments", "UNA:+.?'UNB+UNOC:3+A+B+20231201:1200+1'"),
        ("Malformed elements", "UNB+UNOC:3+SENDER++RECEIVER+20231201:1200+1'")
    ]
    
    for test_name, content in test_cases:
        print(f"Testing {test_name}:")
        
        try:
            # Try to get message info (should not crash)
            info = converter.get_message_info(content)
            
            if 'error' in info:
                print(f"  ✓ Handled gracefully: {info['error'][:50]}...")
            else:
                print(f"  ✓ Processed successfully: {info.get('message_type', 'Unknown')}")
            
            # Try validation
            validation = converter.validate_message(content)
            print(f"  Validation: {'PASS' if validation['is_valid'] else 'FAIL'} "
                  f"({validation['error_count']} errors)")
            
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
        
        print()
    
    print("="*60 + "\n")


def example_file_processing():
    """Example 8: File processing (simulated)"""
    print("=== Example 8: File Processing (Simulated) ===")
    
    # Simulate file processing without actual files
    print("Simulating batch file processing:")
    
    # Create sample file data
    sample_files = {
        "order_001.edi": SAMPLE_ORDERS_MESSAGE,
        "invoice_002.edi": SAMPLE_INVOICE_MESSAGE,
        "despatch_003.edi": SAMPLE_DESADV_MESSAGE
    }
    
    converter = EDIFACTToXMLConverter()
    
    results = {
        'total_files': len(sample_files),
        'processed_files': 0,
        'failed_files': 0,
        'errors': []
    }
    
    for filename, content in sample_files.items():
        print(f"  Processing {filename}:")
        
        try:
            # Get message info
            info = converter.get_message_info(content)
            
            if 'error' not in info:
                # Convert to XML
                xml_result = converter.convert_string(content)
                
                print(f"    ✓ Type: {info['message_type']}")
                print(f"    ✓ Segments: {info['segment_count']}")
                print(f"    ✓ XML size: {len(xml_result)} chars")
                
                results['processed_files'] += 1
            else:
                print(f"    ✗ Error: {info['error']}")
                results['failed_files'] += 1
                results['errors'].append(f"{filename}: {info['error']}")
                
        except Exception as e:
            print(f"    ✗ Exception: {e}")
            results['failed_files'] += 1
            results['errors'].append(f"{filename}: {str(e)}")
    
    print(f"\nBatch processing summary:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Processed: {results['processed_files']}")
    print(f"  Failed: {results['failed_files']}")
    
    if results['errors']:
        print(f"  Errors: {results['errors']}")
    
    print("\n" + "="*60 + "\n")


def run_all_examples():
    """Run all examples"""
    print("EDIFACT Parser - Comprehensive Examples")
    print("=" * 60)
    print()
    
    # Setup logging for examples
    setup_parser_logging("INFO")
    
    examples = [
        example_basic_conversion,
        example_detailed_parsing,
        example_validation,
        example_different_message_types,
        example_custom_configuration,
        example_multiple_output_formats,
        example_error_handling,
        example_file_processing
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"Error in example {i}: {e}")
            print("="*60 + "\n")
    
    print("All examples completed!")


if __name__ == '__main__':
    run_all_examples()

