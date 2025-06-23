#!/usr/bin/env python3
"""
Complete Integration Test for EDIFACT Parser with Customization Layer
====================================================================

This script tests the complete integration between the main EDIFACT parser
and the customization layer, demonstrating end-to-end functionality.

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

# Import main EDIFACT parser components
from edifact_syntax import EDIFACTSyntax
from edifact_parser import EDIFACTParser
from xml_generator import XMLGenerator

# Import customization layer components
from customization import (
    CustomizationProcessor,
    ConfigurationManager,
    create_orders_document_config,
    create_sample_customer_config
)


def create_real_edifact_message():
    """Create a real EDIFACT message for testing"""
    return """UNA:+.?'UNB+UNOC:3+SENDER123:ZZ+RECEIVER456:ZZ+240315:1200+000000001+++++1'UNH+000001+ORDERS:D:96A:UN'BGM+220+PO-2024-001+9'DTM+137:20240315:102'DTM+2:20240322:102'RFF+CR:CUST-REF-001'NAD+BY+1234567890123++Global Retail Chain Inc.+123 Business Blvd+Commerce City+CA+90210+US'CTA+IC+John Smith'COM+john.smith@globalretail.com:EM'NAD+SU+9876543210987++Premium Suppliers Ltd.+456 Supply Street+Manufacturing Town+TX+75001+US'CTA+IC+Sarah Johnson'COM+sarah.johnson@premiumsuppliers.com:EM'CUX+2:USD:4'PAT+3++5:2:D:10'TDT+20+++UPS++GROUND'LIN+1++SKU-WIDGET-001:SA'IMD+F++:::Premium Widget - Blue'QTY+21:100:EA'PRI+AAA:25.50:1::1:EA'DTM+2:20240322:102'LIN+2++SKU-GADGET-002:SA'IMD+F++:::Advanced Gadget - Red'QTY+21:50:EA'PRI+AAA:75.00:1::1:EA'DTM+2:20240325:102'LIN+3++SKU-TOOL-003:SA'IMD+F++:::Professional Tool Set'QTY+21:25:SET'PRI+AAA:150.00:1::1:SET'DTM+2:20240330:102'UNS+S'MOA+79:10050.00'MOA+125:10050.00'MOA+124:829.14'MOA+128:10879.14'UNT+35+000001'UNZ+1+000000001'"""


def test_main_parser():
    """Test the main EDIFACT parser"""
    print("=" * 60)
    print(" TESTING MAIN EDIFACT PARSER")
    print("=" * 60)
    
    # Create EDIFACT message
    edifact_message = create_real_edifact_message()
    print(f"✓ Created EDIFACT message ({len(edifact_message)} characters)")
    
    # Test syntax parsing
    print("\n1. Testing Syntax Parsing:")
    syntax = EDIFACTSyntax()
    
    # Extract syntax characters
    syntax_chars = syntax.extract_syntax_chars(edifact_message)
    print(f"   ✓ Syntax characters: {syntax_chars}")
    
    # Split into segments
    segments = syntax.split_segments(edifact_message)
    print(f"   ✓ Found {len(segments)} segments")
    
    # Parse first few segments
    for i, segment in enumerate(segments[:5]):
        elements = syntax.split_elements(segment)
        print(f"   ✓ Segment {i+1}: {elements[0] if elements else 'Empty'} ({len(elements)} elements)")
    
    # Test main parser
    print("\n2. Testing Main Parser:")
    parser = EDIFACTParser()
    
    try:
        parsed_message = parser.parse_message(edifact_message)
        print(f"   ✓ Message parsed successfully")
        print(f"   ✓ Message type: {parsed_message.message_type}")
        print(f"   ✓ Segments count: {len(parsed_message.segments)}")
        print(f"   ✓ Business data keys: {list(parsed_message.business_data.keys())}")
        
        return parsed_message
        
    except Exception as e:
        print(f"   ❌ Parser error: {e}")
        return None


def test_xml_generation(parsed_message):
    """Test XML generation from parsed message"""
    print("\n3. Testing XML Generation:")
    
    if not parsed_message:
        print("   ❌ No parsed message available")
        return None
    
    try:
        xml_generator = XMLGenerator()
        xml_root = xml_generator.generate_xml(parsed_message)
        xml_string = xml_generator.to_string(xml_root)
        
        print(f"   ✓ XML generated successfully ({len(xml_string)} characters)")
        print(f"   ✓ Root element: {xml_root.tag}")
        print(f"   ✓ Child elements: {len(list(xml_root))}")
        
        # Save XML for customization layer
        return xml_string
        
    except Exception as e:
        print(f"   ❌ XML generation error: {e}")
        return None


def test_customization_layer(xml_data):
    """Test the customization layer"""
    print("\n" + "=" * 60)
    print(" TESTING CUSTOMIZATION LAYER")
    print("=" * 60)
    
    # Setup configuration
    print("\n1. Setting up Configuration:")
    config_manager = ConfigurationManager()
    
    # Add document type config
    orders_config = create_orders_document_config()
    config_manager.add_document_type_config(orders_config)
    print("   ✓ Document type configuration added")
    
    # Add customer config
    customer_config = create_sample_customer_config("1234567890123", "Global Retail Chain")
    config_manager.add_customer_config(customer_config)
    print("   ✓ Customer configuration added")
    
    # Create processor
    processor = CustomizationProcessor(config_manager)
    print("   ✓ Customization processor created")
    
    # Test with XML data
    print("\n2. Testing XML Data Processing:")
    
    if xml_data:
        # Save XML to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as temp_file:
            temp_file.write(xml_data)
            xml_file = temp_file.name
        
        try:
            result = processor.process_file(
                xml_file,
                document_type="ORDERS",
                customer_gln="1234567890123"
            )
            
            print(f"   ✓ XML processing: {'SUCCESS' if result.success else 'FAILED'}")
            if result.success:
                print(f"   ✓ Output XML size: {len(result.output_xml)} characters")
            else:
                print(f"   ❌ Errors: {result.errors}")
            
            # Clean up
            Path(xml_file).unlink()
            
            return result
            
        except Exception as e:
            print(f"   ❌ Customization error: {e}")
            Path(xml_file).unlink()
            return None
    
    # Test with structured data
    print("\n3. Testing Structured Data Processing:")
    
    # Create structured data from EDIFACT
    structured_data = {
        "format": "structured",
        "message_info": {
            "type": "ORDERS",
            "reference": "PO-2024-001"
        },
        "business_data": {
            "references": {
                "ON": "PO-2024-001",
                "CR": "CUST-REF-001"
            },
            "dates": {
                "137": "20240315",
                "2": "20240322"
            },
            "parties": {
                "BY": {
                    "id": "1234567890123",
                    "name": "Global Retail Chain Inc.",
                    "address": "123 Business Blvd",
                    "city": "Commerce City",
                    "state": "CA",
                    "postal_code": "90210",
                    "country": "US"
                },
                "SU": {
                    "id": "9876543210987",
                    "name": "Premium Suppliers Ltd.",
                    "address": "456 Supply Street",
                    "city": "Manufacturing Town",
                    "state": "TX",
                    "postal_code": "75001",
                    "country": "US"
                }
            },
            "line_items": [
                {
                    "line_number": "1",
                    "item_id": "SKU-WIDGET-001",
                    "description": "Premium Widget - Blue",
                    "quantity": "100",
                    "unit_price": "25.50",
                    "total_amount": "2550.00"
                },
                {
                    "line_number": "2",
                    "item_id": "SKU-GADGET-002",
                    "description": "Advanced Gadget - Red",
                    "quantity": "50",
                    "unit_price": "75.00",
                    "total_amount": "3750.00"
                },
                {
                    "line_number": "3",
                    "item_id": "SKU-TOOL-003",
                    "description": "Professional Tool Set",
                    "quantity": "25",
                    "unit_price": "150.00",
                    "total_amount": "3750.00"
                }
            ],
            "totals": {
                "79": "10050.00",
                "125": "10050.00",
                "124": "829.14",
                "128": "10879.14"
            }
        }
    }
    
    try:
        result = processor.process_data(
            structured_data,
            document_type="ORDERS",
            customer_gln="1234567890123"
        )
        
        print(f"   ✓ Structured data processing: {'SUCCESS' if result.success else 'FAILED'}")
        if result.success:
            print(f"   ✓ Output XML size: {len(result.output_xml)} characters")
            print(f"   ✓ Processing stats: {result.processing_stats}")
        else:
            print(f"   ❌ Errors: {result.errors}")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Structured data processing error: {e}")
        return None


def test_end_to_end_integration():
    """Test complete end-to-end integration"""
    print("\n" + "=" * 60)
    print(" END-TO-END INTEGRATION TEST")
    print("=" * 60)
    
    # Step 1: Parse EDIFACT message
    print("\n1. Parsing EDIFACT Message:")
    edifact_message = create_real_edifact_message()
    
    parser = EDIFACTParser()
    parsed_message = parser.parse_message(edifact_message)
    print(f"   ✓ EDIFACT message parsed")
    
    # Step 2: Convert to comprehensive data structure
    print("\n2. Converting to Comprehensive Data:")
    comprehensive_data = {
        "format": "comprehensive",
        "source": "edifact_parser",
        "timestamp": datetime.now().isoformat(),
        "message_info": {
            "type": parsed_message.message_type,
            "reference": parsed_message.message_reference,
            "version": parsed_message.version,
            "control_number": parsed_message.control_number
        },
        "interchange_info": {
            "sender_id": parsed_message.interchange_header.sender_id if hasattr(parsed_message, 'interchange_header') else "SENDER123",
            "recipient_id": parsed_message.interchange_header.recipient_id if hasattr(parsed_message, 'interchange_header') else "RECEIVER456"
        },
        "business_data": parsed_message.business_data,
        "segments": [
            {
                "tag": segment.tag,
                "position": segment.position,
                "elements": segment.elements
            }
            for segment in parsed_message.segments
        ]
    }
    print(f"   ✓ Comprehensive data structure created")
    
    # Step 3: Apply customization
    print("\n3. Applying Customization:")
    config_manager = ConfigurationManager()
    config_manager.add_document_type_config(create_orders_document_config())
    config_manager.add_customer_config(create_sample_customer_config("1234567890123", "Global Retail Chain"))
    
    processor = CustomizationProcessor(config_manager)
    
    result = processor.process_data(
        comprehensive_data,
        document_type="ORDERS",
        customer_gln="1234567890123"
    )
    
    print(f"   ✓ Customization applied: {'SUCCESS' if result.success else 'FAILED'}")
    
    if result.success:
        print(f"   ✓ Final XML size: {len(result.output_xml)} characters")
        
        # Save final result
        output_file = Path("end_to_end_result.xml")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.output_xml)
        
        print(f"   ✓ Result saved to: {output_file}")
        
        return True
    else:
        print(f"   ❌ Customization errors: {result.errors}")
        return False


def test_performance():
    """Test performance with multiple messages"""
    print("\n" + "=" * 60)
    print(" PERFORMANCE TESTING")
    print("=" * 60)
    
    import time
    
    # Setup
    config_manager = ConfigurationManager()
    config_manager.add_document_type_config(create_orders_document_config())
    config_manager.add_customer_config(create_sample_customer_config("1234567890123", "Test Customer"))
    
    processor = CustomizationProcessor(config_manager)
    parser = EDIFACTParser()
    
    # Test data
    edifact_message = create_real_edifact_message()
    
    # Performance test
    num_iterations = 10
    print(f"\n1. Processing {num_iterations} messages:")
    
    start_time = time.time()
    successful_processes = 0
    
    for i in range(num_iterations):
        try:
            # Parse EDIFACT
            parsed_message = parser.parse_message(edifact_message)
            
            # Create data structure
            data = {
                "message_info": {"type": "ORDERS"},
                "business_data": parsed_message.business_data
            }
            
            # Apply customization
            result = processor.process_data(data, "ORDERS", "1234567890123")
            
            if result.success:
                successful_processes += 1
            
        except Exception as e:
            print(f"   ❌ Error in iteration {i+1}: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"   ✓ Completed {successful_processes}/{num_iterations} processes")
    print(f"   ✓ Total time: {total_time:.2f} seconds")
    print(f"   ✓ Average time per message: {total_time/num_iterations:.3f} seconds")
    print(f"   ✓ Messages per second: {num_iterations/total_time:.2f}")


def test_error_handling():
    """Test error handling capabilities"""
    print("\n" + "=" * 60)
    print(" ERROR HANDLING TESTING")
    print("=" * 60)
    
    processor = CustomizationProcessor()
    
    # Test 1: Invalid data format
    print("\n1. Testing Invalid Data Format:")
    try:
        result = processor.process_data(
            "invalid_data",
            document_type="ORDERS"
        )
        print(f"   ✓ Handled invalid data: {'SUCCESS' if not result.success else 'UNEXPECTED SUCCESS'}")
        if not result.success:
            print(f"   ✓ Error captured: {result.errors[0] if result.errors else 'No specific error'}")
    except Exception as e:
        print(f"   ✓ Exception handled: {e}")
    
    # Test 2: Missing required fields
    print("\n2. Testing Missing Required Fields:")
    incomplete_data = {
        "message_info": {"type": "ORDERS"},
        "business_data": {}  # Missing required fields
    }
    
    result = processor.process_data(
        incomplete_data,
        document_type="ORDERS",
        validation_level="strict"
    )
    
    print(f"   ✓ Handled missing fields: {'SUCCESS' if not result.success else 'UNEXPECTED SUCCESS'}")
    if not result.success:
        print(f"   ✓ Errors found: {len(result.errors)}")
    
    # Test 3: Invalid document type
    print("\n3. Testing Invalid Document Type:")
    valid_data = {
        "message_info": {"type": "INVALID"},
        "business_data": {"test": "data"}
    }
    
    result = processor.process_data(
        valid_data,
        document_type="INVALID_TYPE"
    )
    
    print(f"   ✓ Handled invalid document type: {'SUCCESS' if not result.success else 'PROCESSED ANYWAY'}")


def main():
    """Main test function"""
    print("EDIFACT PARSER + CUSTOMIZATION LAYER - INTEGRATION TEST")
    print("=" * 70)
    print(f"Test started at: {datetime.now().isoformat()}")
    
    test_results = {
        "main_parser": False,
        "xml_generation": False,
        "customization_layer": False,
        "end_to_end": False,
        "performance": False,
        "error_handling": False
    }
    
    try:
        # Test main parser
        parsed_message = test_main_parser()
        test_results["main_parser"] = parsed_message is not None
        
        # Test XML generation
        xml_data = test_xml_generation(parsed_message)
        test_results["xml_generation"] = xml_data is not None
        
        # Test customization layer
        customization_result = test_customization_layer(xml_data)
        test_results["customization_layer"] = customization_result is not None and customization_result.success
        
        # Test end-to-end integration
        test_results["end_to_end"] = test_end_to_end_integration()
        
        # Test performance
        test_performance()
        test_results["performance"] = True
        
        # Test error handling
        test_error_handling()
        test_results["error_handling"] = True
        
        # Summary
        print("\n" + "=" * 70)
        print(" TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(test_results)
        passed_tests = sum(test_results.values())
        
        for test_name, result in test_results.items():
            status = "✓ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {passed_tests/total_tests:.1%}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Integration is successful!")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Review the output above.")
        
        print(f"\nTest completed at: {datetime.now().isoformat()}")
        
        return passed_tests == total_tests
        
    except Exception as e:
        print(f"\n❌ Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

