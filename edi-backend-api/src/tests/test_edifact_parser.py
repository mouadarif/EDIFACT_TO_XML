#!/usr/bin/env python3
"""
Test Suite for EDIFACT Parser
=============================

Comprehensive test suite for the EDIFACT parser package.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
# sys.path.insert(0, str(Path(__file__).parent.parent)) # No longer needed

from src.__main__ import (
    EDIFACTToXMLConverter,
    convert_edifact_to_xml,
    parse_edifact_message,
    validate_edifact_message
)
from src.edifact_parser import EDIFACTParser # This is the core parser class
from src.edifact_syntax import EDIFACTSyntax
from src.xml_generator import XMLGenerator
from src.edifact_utils import EDIFACTUtils
from src.edifact_validators import ValidationLevel # ValidationLevel enum


class TestEDIFACTSyntax(unittest.TestCase):
    """Test EDIFACT syntax parsing"""
    
    def setUp(self):
        self.syntax = EDIFACTSyntax() # self.syntax is an EDIFACTSyntax object
    
    def test_default_syntax_characters(self):
        """Test default syntax characters"""
        self.assertEqual(self.syntax.syntax.component_separator, ':')
        self.assertEqual(self.syntax.syntax.element_separator, '+')
        self.assertEqual(self.syntax.syntax.segment_terminator, "'")
        self.assertEqual(self.syntax.syntax.escape_character, '?')
        self.assertEqual(self.syntax.syntax.decimal_point, '.')
    
    def test_una_segment_parsing(self):
        """Test UNA segment parsing"""
        # Standard UNA: UNA<comp><elem><dec><esc><reserved><term>
        # Example: "UNA:+.? '" (Here, reserved is space, terminator is apostrophe)
        una_segment = "UNA:+.? '" # Corrected to include a space for 'reserved'
        parsed_syntax_obj = EDIFACTSyntax.from_una_segment(una_segment) # This is an EDIFACTSyntax object
        
        self.assertEqual(parsed_syntax_obj.syntax.component_separator, ':')
        self.assertEqual(parsed_syntax_obj.syntax.element_separator, '+')
        self.assertEqual(parsed_syntax_obj.syntax.decimal_point, '.')
        self.assertEqual(parsed_syntax_obj.syntax.escape_character, '?')
        self.assertEqual(parsed_syntax_obj.syntax.reserved, ' ')
        self.assertEqual(parsed_syntax_obj.syntax.segment_terminator, "'")
    
    def test_segment_splitting(self):
        """Test segment splitting"""
        content = "UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'"
        segments = self.syntax.split_segments(content)
        
        self.assertEqual(len(segments), 3)
        self.assertTrue(segments[0].startswith("UNB"))
        self.assertTrue(segments[1].startswith("UNH"))
        self.assertTrue(segments[2].startswith("BGM"))
    
    def test_element_splitting(self):
        """Test element splitting"""
        segment = "UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1"
        elements = self.syntax.split_elements(segment)
        
        self.assertEqual(len(elements), 6)
        self.assertEqual(elements[0], "UNB")
        self.assertEqual(elements[1], "UNOC:3")
        self.assertEqual(elements[2], "SENDER")
    
    def test_component_splitting(self):
        """Test component splitting"""
        element = "UNOC:3"
        components = self.syntax.split_components(element)
        
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0], "UNOC")
        self.assertEqual(components[1], "3")


class TestEDIFACTParser(unittest.TestCase):
    """Test EDIFACT parser functionality"""
    
    def setUp(self):
        self.parser = EDIFACTParser()
        self.sample_edifact = """UNA:+.? 'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'DTM+137:20231201:102'NAD+BY+BUYER123++BUYER COMPANY'LIN+1++PRODUCT123:EN'QTY+21:100:PCE'PRI+AAA:10.50:EUR'UNT+8+1'UNZ+1+1'"""
    
    def test_parse_message(self):
        """Test message parsing"""
        parsed_message = self.parser.parse_message(self.sample_edifact)
        
        self.assertIsNotNone(parsed_message)
        self.assertEqual(parsed_message.message_type, "ORDERS")
        self.assertEqual(parsed_message.sender_id, "SENDER")
        self.assertEqual(parsed_message.recipient_id, "RECEIVER")
        self.assertTrue(len(parsed_message.segments) > 0)
    
    def test_segment_parsing(self):
        """Test individual segment parsing"""
        parsed_message = self.parser.parse_message(self.sample_edifact)
        
        # Find BGM segment
        bgm_segment = None
        for segment in parsed_message.segments:
            if segment.tag == "BGM":
                bgm_segment = segment
                break
        
        self.assertIsNotNone(bgm_segment)
        self.assertEqual(bgm_segment.tag, "BGM")
        self.assertTrue(len(bgm_segment.elements) >= 3)
    
    def test_business_data_extraction(self):
        """Test business data extraction"""
        parsed_message = self.parser.parse_message(self.sample_edifact)
        business_data = self.parser.extract_business_data(parsed_message)
        
        self.assertIn('message_info', business_data)
        self.assertIn('parties', business_data)
        self.assertIn('dates', business_data)
        self.assertEqual(business_data['message_info']['type'], "ORDERS")


class TestXMLGenerator(unittest.TestCase):
    """Test XML generation functionality"""
    
    def setUp(self):
        self.parser = EDIFACTParser()
        self.xml_generator = XMLGenerator()
        self.sample_edifact = """UNA:+.? 'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""
    
    def test_xml_generation(self):
        """Test XML generation from parsed message"""
        parsed_message = self.parser.parse_message(self.sample_edifact)
        xml_root = self.xml_generator.generate_xml(parsed_message)
        
        self.assertIsNotNone(xml_root)
        self.assertEqual(xml_root.tag, "PurchaseOrderMessage") # Changed from ORDERSMessage
    
    def test_xml_string_output(self):
        """Test XML string output"""
        parsed_message = self.parser.parse_message(self.sample_edifact)
        xml_root = self.xml_generator.generate_xml(parsed_message)
        xml_string = self.xml_generator.to_string(xml_root)
        
        self.assertIsInstance(xml_string, str)
        self.assertIn("<?xml", xml_string)
        self.assertIn("PurchaseOrderMessage", xml_string) # Changed from ORDERSMessage


class TestEDIFACTToXMLConverter(unittest.TestCase):
    """Test main converter functionality"""
    
    def setUp(self):
        self.converter = EDIFACTToXMLConverter()
        self.sample_edifact = """UNA:+.? 'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'DTM+137:20231201:102'UNT+5+1'UNZ+1+1'"""
    
    def test_convert_string(self):
        """Test string conversion"""
        xml_result = self.converter.convert_string(self.sample_edifact)
        
        self.assertIsInstance(xml_result, str)
        self.assertIn("PurchaseOrderMessage", xml_result) # Changed from ORDERSMessage
        self.assertIn("UNB", xml_result)
        self.assertIn("BGM", xml_result)
    
    def test_parse_and_extract(self):
        """Test parsing and data extraction"""
        data = self.converter.parse_and_extract(self.sample_edifact)
        
        self.assertIsInstance(data, dict)
        self.assertIn('message_info', data)
        self.assertIn('segments', data)
        self.assertEqual(data['message_info']['type'], "ORDERS")
    
    def test_validate_message(self):
        """Test message validation"""
        validation_result = self.converter.validate_message(self.sample_edifact)
        
        self.assertIsInstance(validation_result, dict)
        self.assertIn('is_valid', validation_result)
        self.assertIn('error_count', validation_result)
        self.assertIn('warning_count', validation_result)
    
    def test_get_message_info(self):
        """Test message info extraction"""
        info = self.converter.get_message_info(self.sample_edifact)
        
        self.assertIsInstance(info, dict)
        self.assertEqual(info['message_type'], "ORDERS")
        self.assertEqual(info['sender_id'], "SENDER")
        self.assertEqual(info['recipient_id'], "RECEIVER")


class TestEDIFACTUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_format_date(self):
        """Test date formatting"""
        # Test YYMMDD format
        formatted_date = EDIFACTUtils.format_date("231201", "103", "iso")
        self.assertEqual(formatted_date, "2023-12-01")
        
        # Test CCYYMMDD format
        formatted_date = EDIFACTUtils.format_date("20231201", "102", "iso")
        self.assertEqual(formatted_date, "2023-12-01")
    
    def test_format_time(self):
        """Test time formatting"""
        formatted_time = EDIFACTUtils.format_time("1230", "401")
        self.assertEqual(formatted_time, "12:30:00")
        
        formatted_time = EDIFACTUtils.format_time("123045", "401")
        self.assertEqual(formatted_time, "12:30:45")
    
    def test_clean_edifact_value(self):
        """Test EDIFACT value cleaning"""
        cleaned = EDIFACTUtils.clean_edifact_value("TEST?:VALUE")
        self.assertEqual(cleaned, "TEST:VALUE")
        
        cleaned = EDIFACTUtils.clean_edifact_value("TEST?+VALUE")
        self.assertEqual(cleaned, "TEST+VALUE")
    
    def test_extract_message_type(self):
        """Test message type extraction"""
        content = "UNH+1+ORDERS:D:03B:UN:EAN008'"
        message_type = EDIFACTUtils.extract_message_type(content)
        self.assertEqual(message_type, "ORDERS")


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def setUp(self):
        self.sample_edifact = """UNA:+.? 'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""
    
    def test_convert_edifact_to_xml(self):
        """Test convenience conversion function"""
        xml_result = convert_edifact_to_xml(self.sample_edifact)
        
        self.assertIsInstance(xml_result, str)
        self.assertIn("PurchaseOrderMessage", xml_result) # Changed from ORDERSMessage
    
    def test_parse_edifact_message(self):
        """Test convenience parsing function"""
        data = parse_edifact_message(self.sample_edifact)
        
        self.assertIsInstance(data, dict)
        self.assertIn('message_info', data)
        self.assertEqual(data['message_info']['type'], "ORDERS")
    
    def test_validate_edifact_message(self):
        """Test convenience validation function"""
        validation_result = validate_edifact_message(self.sample_edifact)
        
        self.assertIsInstance(validation_result, dict)
        self.assertIn('is_valid', validation_result)


class TestValidationLevels(unittest.TestCase):
    """Test different validation levels"""
    
    def setUp(self):
        self.sample_edifact = """UNA:+.? 'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""
    
    def test_no_validation(self):
        """Test with no validation"""
        converter = EDIFACTToXMLConverter(validation_level=ValidationLevel.NONE)
        result = converter.validate_message(self.sample_edifact)
        
        # Should still return a result structure
        self.assertIsInstance(result, dict)
    
    def test_basic_validation(self):
        """Test with basic validation"""
        converter = EDIFACTToXMLConverter(validation_level=ValidationLevel.BASIC)
        result = converter.validate_message(self.sample_edifact)
        
        self.assertIsInstance(result, dict)
        self.assertIn('is_valid', result)
    
    def test_standard_validation(self):
        """Test with standard validation"""
        converter = EDIFACTToXMLConverter(validation_level=ValidationLevel.STANDARD)
        result = converter.validate_message(self.sample_edifact)
        
        self.assertIsInstance(result, dict)
        self.assertIn('is_valid', result)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_empty_content(self):
        """Test handling of empty content"""
        converter = EDIFACTToXMLConverter()
        
        # Should not raise exception
        result = converter.validate_message("")
        self.assertFalse(result['is_valid'])
    
    def test_invalid_edifact(self):
        """Test handling of invalid EDIFACT"""
        converter = EDIFACTToXMLConverter()
        invalid_content = "This is not EDIFACT content"
        
        # Should not raise exception
        result = converter.validate_message(invalid_content)
        self.assertFalse(result['is_valid'])
    
    def test_malformed_segments(self):
        """Test handling of malformed segments"""
        converter = EDIFACTToXMLConverter()
        malformed_content = "UNB+INCOMPLETE"
        
        # Should not raise exception
        result = converter.validate_message(malformed_content)
        self.assertIsInstance(result, dict)


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestEDIFACTSyntax,
        TestEDIFACTParser,
        TestXMLGenerator,
        TestEDIFACTToXMLConverter,
        TestEDIFACTUtils,
        TestConvenienceFunctions,
        TestValidationLevels,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

