#!/usr/bin/env python3
"""
EDIFACT Parser Main Module
==========================

This is the main interface module for the EDIFACT parser.
Provides a simple API for parsing EDIFACT messages and generating XML output.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union
import logging
from pathlib import Path
from .edifact_parser import EDIFACTParser, ParsedMessage
from .xml_generator import XMLGenerator, XMLGeneratorConfig
from .edifact_validators import ValidationLevel
from .edifact_utils import EDIFACTUtils, DataExtractor, FileProcessor, setup_logging
from .edifact_constants import OUTPUT_FORMATS


class EDIFACTToXMLConverter:
    """
    Main EDIFACT to XML converter class.
    
    Provides a high-level interface for converting EDIFACT messages to XML
    with comprehensive parsing, validation, and output options.
    """
    
    def __init__(self,
                 validation_level: ValidationLevel = ValidationLevel.STANDARD,
                 generate_empty_tags: bool = True,
                 use_semantic_names: bool = True,
                 pretty_print: bool = True,
                 include_statistics: bool = True,
                 include_validation_info: bool = True):
        """
        Initialize EDIFACT to XML converter.
        
        Args:
            validation_level: Level of validation to perform
            generate_empty_tags: Generate empty XML tags for missing elements
            use_semantic_names: Use semantic element names instead of generic ones
            pretty_print: Format XML with indentation
            include_statistics: Include parsing statistics in XML
            include_validation_info: Include validation results in XML
        """
        # Initialize parser
        self.parser = EDIFACTParser(
            validation_level=validation_level,
            generate_empty_elements=generate_empty_tags
        )
        
        # Initialize XML generator
        xml_config = XMLGeneratorConfig(
            generate_empty_tags=generate_empty_tags,
            use_semantic_names=use_semantic_names,
            pretty_print=pretty_print,
            include_statistics=include_statistics,
            include_validation_info=include_validation_info
        )
        self.xml_generator = XMLGenerator(xml_config)
        
        # Initialize utilities
        self.data_extractor = DataExtractor()
        self.file_processor = FileProcessor()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def convert_string(self, edifact_content: str) -> str:
        """
        Convert EDIFACT string to XML string.
        
        Args:
            edifact_content: Raw EDIFACT message content
            
        Returns:
            XML string representation
        """
        try:
            # Parse EDIFACT content
            parsed_message = self.parser.parse_message(edifact_content)
            
            # Generate XML
            xml_root = self.xml_generator.generate_xml(parsed_message)
            xml_string = self.xml_generator.to_string(xml_root)
            
            self.logger.info("Successfully converted EDIFACT string to XML")
            return xml_string
            
        except Exception as e:
            self.logger.error(f"Error converting EDIFACT string: {e}")
            raise
    
    def convert_file(self, input_file: str, output_file: str, 
                    encoding: str = 'utf-8') -> bool:
        """
        Convert EDIFACT file to XML file.
        
        Args:
            input_file: Path to input EDIFACT file
            output_file: Path to output XML file
            encoding: File encoding
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate input file
            if not EDIFACTUtils.validate_file_path(input_file, must_exist=True):
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            # Parse EDIFACT file
            parsed_message = self.parser.parse_file(input_file, encoding)
            
            # Generate XML
            xml_root = self.xml_generator.generate_xml(parsed_message)
            
            # Save XML file
            self.xml_generator.save_to_file(xml_root, output_file)
            
            self.logger.info(f"Successfully converted {input_file} to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting file {input_file}: {e}")
            return False
    
    def parse_and_extract(self, edifact_content: str) -> Dict[str, Any]:
        """
        Parse EDIFACT content and extract structured data.
        
        Args:
            edifact_content: Raw EDIFACT message content
            
        Returns:
            Dictionary with parsed data and metadata
        """
        try:
            # Parse EDIFACT content
            parsed_message = self.parser.parse_message(edifact_content)
            
            # Extract to dictionary
            data = self.data_extractor.extract_to_dict(parsed_message)
            
            # Add business data extraction
            business_data = self.parser.extract_business_data(parsed_message)
            data['business_data'] = business_data
            
            # Add segment summary
            segment_summary = self.parser.get_segment_summary(parsed_message)
            data['segment_summary'] = segment_summary
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error parsing and extracting EDIFACT content: {e}")
            raise
    
    def validate_message(self, edifact_content: str) -> Dict[str, Any]:
        """
        Validate EDIFACT message and return validation results.
        
        Args:
            edifact_content: Raw EDIFACT message content
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse with validation
            parsed_message = self.parser.parse_message(edifact_content)
            
            validation_result = {
                'is_valid': True,
                'error_count': 0,
                'warning_count': 0,
                'info_count': 0,
                'messages': [],
                'summary': 'No validation performed'
            }
            
            if parsed_message.validation_result:
                vr = parsed_message.validation_result
                validation_result = {
                    'is_valid': vr.is_valid,
                    'error_count': vr.error_count,
                    'warning_count': vr.warning_count,
                    'info_count': vr.info_count,
                    'messages': [str(msg) for msg in vr.messages],
                    'summary': vr.get_summary()
                }
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error validating EDIFACT message: {e}")
            return {
                'is_valid': False,
                'error_count': 1,
                'warning_count': 0,
                'info_count': 0,
                'messages': [f"Validation failed: {e}"],
                'summary': 'Validation failed due to parsing error'
            }
    
    def convert_to_format(self, edifact_content: str, output_format: str) -> str:
        """
        Convert EDIFACT content to specified format.
        
        Args:
            edifact_content: Raw EDIFACT message content
            output_format: Output format ('xml', 'json', 'csv')
            
        Returns:
            Converted content as string
        """
        if output_format.lower() == 'xml':
            return self.convert_string(edifact_content)
        
        # Parse EDIFACT content
        parsed_message = self.parser.parse_message(edifact_content)
        
        if output_format.lower() == 'json':
            import json
            data = self.data_extractor.extract_to_dict(parsed_message)
            return json.dumps(data, indent=2, ensure_ascii=False)
        
        elif output_format.lower() == 'csv':
            # For CSV, we'll return a simple representation
            # In practice, you'd want to save to a file
            import io
            import csv
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['SegmentTag', 'Position', 'ElementCount', 'SemanticName'])
            
            # Write data
            for segment in parsed_message.segments:
                writer.writerow([
                    segment.tag,
                    segment.position,
                    len(segment.elements),
                    segment.semantic_name or ''
                ])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def batch_convert_directory(self, input_dir: str, output_dir: str,
                              output_format: str = 'xml',
                              file_pattern: str = '*.edi') -> Dict[str, Any]:
        """
        Convert all EDIFACT files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            output_format: Output format ('xml', 'json', 'csv')
            file_pattern: File pattern to match
            
        Returns:
            Processing results summary
        """
        return self.file_processor.process_directory(
            input_dir, output_dir, output_format, file_pattern
        )
    
    def get_message_info(self, edifact_content: str) -> Dict[str, Any]:
        """
        Get basic message information without full parsing.
        
        Args:
            edifact_content: Raw EDIFACT message content
            
        Returns:
            Dictionary with message information
        """
        try:
            # Quick extraction of message type
            message_type = EDIFACTUtils.extract_message_type(edifact_content)
            
            # Parse for full information
            parsed_message = self.parser.parse_message(edifact_content)
            
            return {
                'message_type': parsed_message.message_type or message_type,
                'message_version': parsed_message.message_version,
                'message_release': parsed_message.message_release,
                'message_reference': parsed_message.message_reference,
                'interchange_reference': parsed_message.interchange_reference,
                'sender_id': parsed_message.sender_id,
                'recipient_id': parsed_message.recipient_id,
                'preparation_date': parsed_message.preparation_date,
                'preparation_time': parsed_message.preparation_time,
                'segment_count': len(parsed_message.segments),
                'file_size': len(edifact_content)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting message info: {e}")
            return {
                'error': str(e),
                'message_type': EDIFACTUtils.extract_message_type(edifact_content),
                'file_size': len(edifact_content)
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current parsing statistics"""
        return self.parser.get_statistics()


# Convenience functions for direct usage
def convert_edifact_to_xml(edifact_content: str, **kwargs) -> str:
    """
    Convert EDIFACT content to XML string.
    
    Args:
        edifact_content: Raw EDIFACT message content
        **kwargs: Additional configuration options
        
    Returns:
        XML string representation
    """
    converter = EDIFACTToXMLConverter(**kwargs)
    return converter.convert_string(edifact_content)


def convert_edifact_file_to_xml(input_file: str, output_file: str, **kwargs) -> bool:
    """
    Convert EDIFACT file to XML file.
    
    Args:
        input_file: Path to input EDIFACT file
        output_file: Path to output XML file
        **kwargs: Additional configuration options
        
    Returns:
        True if successful, False otherwise
    """
    converter = EDIFACTToXMLConverter(**kwargs)
    return converter.convert_file(input_file, output_file)


def parse_edifact_message(edifact_content: str, **kwargs) -> Dict[str, Any]:
    """
    Parse EDIFACT message and return structured data.
    
    Args:
        edifact_content: Raw EDIFACT message content
        **kwargs: Additional configuration options
        
    Returns:
        Dictionary with parsed data
    """
    converter = EDIFACTToXMLConverter(**kwargs)
    return converter.parse_and_extract(edifact_content)


def validate_edifact_message(edifact_content: str, **kwargs) -> Dict[str, Any]:
    """
    Validate EDIFACT message.
    
    Args:
        edifact_content: Raw EDIFACT message content
        **kwargs: Additional configuration options
        
    Returns:
        Dictionary with validation results
    """
    converter = EDIFACTToXMLConverter(**kwargs)
    return converter.validate_message(edifact_content)


def get_supported_output_formats() -> Dict[str, str]:
    """Get supported output formats"""
    return OUTPUT_FORMATS.copy()


def setup_parser_logging(level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup logging for the EDIFACT parser.
    
    Args:
        level: Logging level
        log_file: Optional log file path
    """
    setup_logging(level, log_file)


# Version information
__version__ = "1.0.0"
__author__ = "EDIFACT Parser Team"
__description__ = "Professional EDIFACT to XML parser with comprehensive validation and semantic mapping"

if __name__ == "__main__":
    # Ensure cli.py can find its modules if __main__ is the entry point of the package
    import sys
    from pathlib import Path
    # Add the package directory itself to sys.path to help resolve imports if needed,
    # though -m should handle this. cli.py also does this.
    # sys.path.insert(0, str(Path(__file__).parent))

    from .cli import main as cli_main # Use relative import for cli
    sys.exit(cli_main())
