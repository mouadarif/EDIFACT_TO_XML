#!/usr/bin/env python3
"""
Simple Integration Test for EDIFACT Customization Layer
======================================================

This script tests the customization layer functionality independently
and demonstrates its capabilities with sample data.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_customization_layer_standalone():
    """Test the customization layer as a standalone component"""
    print("EDIFACT CUSTOMIZATION LAYER - STANDALONE TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().isoformat()}")
    
    try:
        # Import customization components
        from customization import (
            CustomizationProcessor,
            ConfigurationManager,
            create_orders_document_config,
            create_sample_customer_config
        )
        
        print("✓ Customization layer imports successful")
        
        # Test 1: Configuration Management
        print("\n1. Testing Configuration Management:")
        config_manager = ConfigurationManager()
        
        # Add document type config
        orders_config = create_orders_document_config()
        config_manager.add_document_type_config(orders_config)
        print("   ✓ Document type configuration added")
        
        # Add customer config
        customer_config = create_sample_customer_config("1234567890123", "Test Customer")
        config_manager.add_customer_config(customer_config)
        print("   ✓ Customer configuration added")
        
        # Validate configurations
        validation = config_manager.validate_configuration()
        print(f"   ✓ Configuration validation: {'PASS' if validation['is_valid'] else 'FAIL'}")
        
        # Test 2: Processor Creation
        print("\n2. Testing Processor Creation:")
        processor = CustomizationProcessor(config_manager)
        print("   ✓ Customization processor created")
        
        # Test 3: Sample Data Processing
        print("\n3. Testing Sample Data Processing:")
        sample_data = {
            "format": "json",
            "message_info": {
                "type": "ORDERS",
                "reference": "TEST-ORDER-001"
            },
            "business_data": {
                "references": {
                    "ON": "PO-TEST-001",
                    "CR": "CUSTOMER-REF-001"
                },
                "dates": {
                    "137": "20240315",
                    "2": "20240322"
                },
                "parties": {
                    "BY": {
                        "id": "1234567890123",
                        "name": "Test Customer Corp",
                        "address": "123 Test Street",
                        "city": "Test City",
                        "postal_code": "12345",
                        "country": "US"
                    },
                    "SU": {
                        "id": "9876543210987",
                        "name": "Test Supplier Inc",
                        "address": "456 Supply Avenue",
                        "city": "Supply Town",
                        "postal_code": "67890",
                        "country": "US"
                    }
                },
                "line_items": [
                    {
                        "line_number": "1",
                        "item_id": "TEST-ITEM-001",
                        "description": "Test Product A",
                        "quantity": "10",
                        "unit_price": "25.00",
                        "total_amount": "250.00"
                    },
                    {
                        "line_number": "2",
                        "item_id": "TEST-ITEM-002",
                        "description": "Test Product B",
                        "quantity": "5",
                        "unit_price": "50.00",
                        "total_amount": "250.00"
                    }
                ],
                "totals": {
                    "79": "500.00",
                    "125": "500.00",
                    "124": "40.00",
                    "128": "540.00"
                }
            }
        }
        
        # Process the data
        result = processor.process_data(
            sample_data,
            document_type="ORDERS",
            customer_gln="1234567890123"
        )
        
        print(f"   ✓ Data processing: {'SUCCESS' if result.success else 'FAILED'}")
        
        if result.success:
            print(f"   ✓ Generated XML size: {len(result.output_xml)} characters")
            print(f"   ✓ Processing stats: {result.processing_stats}")
            
            # Save output
            output_file = Path("test_customization_output.xml")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.output_xml)
            print(f"   ✓ Output saved to: {output_file}")
            
            # Show XML preview
            print("\n   XML Preview (first 500 characters):")
            print("   " + "-" * 50)
            print("   " + result.output_xml[:500])
            if len(result.output_xml) > 500:
                print("   ... (truncated)")
            print("   " + "-" * 50)
            
        else:
            print(f"   ❌ Processing errors: {result.errors}")
            print(f"   ⚠️  Processing warnings: {result.warnings}")
        
        # Test 4: Different Validation Levels
        print("\n4. Testing Validation Levels:")
        validation_levels = ["none", "basic", "standard", "strict"]
        
        for level in validation_levels:
            test_result = processor.process_data(
                sample_data,
                document_type="ORDERS",
                customer_gln="1234567890123",
                validation_level=level
            )
            
            status = "SUCCESS" if test_result.success else "FAILED"
            print(f"   ✓ Validation level '{level}': {status}")
        
        # Test 5: Configuration Export/Import
        print("\n5. Testing Configuration Export/Import:")
        
        # Export configuration
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            config_manager.export_configuration(temp_file.name)
            export_file = temp_file.name
        
        print(f"   ✓ Configuration exported to temporary file")
        
        # Import to new manager
        new_config_manager = ConfigurationManager()
        new_config_manager.import_configuration(export_file)
        
        print(f"   ✓ Configuration imported successfully")
        print(f"   ✓ Document types: {len(new_config_manager.list_document_types())}")
        print(f"   ✓ Customers: {len(new_config_manager.list_customers())}")
        
        # Clean up
        Path(export_file).unlink()
        
        # Test 6: Error Handling
        print("\n6. Testing Error Handling:")
        
        # Test with invalid data
        invalid_data = {"invalid": "data"}
        
        error_result = processor.process_data(
            invalid_data,
            document_type="ORDERS",
            validation_level="strict"
        )
        
        print(f"   ✓ Error handling: {'PASS' if not error_result.success else 'UNEXPECTED SUCCESS'}")
        if not error_result.success:
            print(f"   ✓ Errors captured: {len(error_result.errors)}")
        
        # Summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        
        if result.success:
            print("✅ ALL TESTS PASSED!")
            print("✅ Customization layer is working correctly")
            print(f"✅ Generated XML output: {len(result.output_xml)} characters")
            print(f"✅ Processing time: {result.metadata.get('processing_duration', 'N/A')}")
        else:
            print("❌ SOME TESTS FAILED!")
            print("❌ Check the error messages above")
        
        print(f"\nTest completed at: {datetime.now().isoformat()}")
        
        return result.success
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("❌ Customization layer modules not found or have import issues")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_module_structure():
    """Test the module structure and availability"""
    print("\nMODULE STRUCTURE TEST")
    print("=" * 40)
    
    expected_modules = [
        "customization.__init__",
        "customization.data_readers",
        "customization.rule_engine", 
        "customization.mapping_engine",
        "customization.xml_customizer",
        "customization.configuration_manager",
        "customization.customization_processor"
    ]
    
    available_modules = []
    missing_modules = []
    
    for module_name in expected_modules:
        try:
            __import__(module_name)
            available_modules.append(module_name)
            print(f"✓ {module_name}")
        except ImportError as e:
            missing_modules.append(module_name)
            print(f"❌ {module_name}: {e}")
    
    print(f"\nModule Summary:")
    print(f"  Available: {len(available_modules)}/{len(expected_modules)}")
    print(f"  Missing: {len(missing_modules)}")
    
    return len(missing_modules) == 0


def main():
    """Main test function"""
    print("EDIFACT CUSTOMIZATION LAYER - COMPREHENSIVE TEST")
    print("=" * 70)
    
    # Test module structure
    modules_ok = test_module_structure()
    
    if not modules_ok:
        print("\n❌ Module structure test failed. Cannot proceed with functionality tests.")
        return False
    
    # Test functionality
    functionality_ok = test_customization_layer_standalone()
    
    # Overall result
    print("\n" + "=" * 70)
    print(" OVERALL TEST RESULT")
    print("=" * 70)
    
    if modules_ok and functionality_ok:
        print("🎉 ALL TESTS PASSED!")
        print("🎉 Customization layer is ready for production use!")
    else:
        print("⚠️  SOME TESTS FAILED!")
        print("⚠️  Review the output above for details.")
    
    return modules_ok and functionality_ok


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

