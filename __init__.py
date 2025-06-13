#!/usr/bin/env python3
"""
EDIFACT Parser Package
=====================

A comprehensive, modular EDIFACT to XML parser with professional-grade
validation, semantic mapping, and structured output generation.

This package provides:
- Complete EDIFACT syntax parsing
- Comprehensive validation at multiple levels
- Semantic mapping to meaningful XML element names
- Support for all standard EDIFACT segments and elements
- Multiple output formats (XML, JSON, CSV)
- Batch processing capabilities
- Extensible architecture for custom mappings

Author: EDIFACT Parser Team
Version: 1.0.0
License: MIT
"""

# Core parsing and conversion functionality
from .edifact_parser import EDIFACTParser, ParsedMessage, ParsedSegment, ParsedElement, ParsedComponent
from .xml_generator import XMLGenerator, XMLGeneratorConfig
from .edifact_validators import EDIFACTValidator, ValidationResult, ValidationLevel

# Main interface
from .__main__ import (
    EDIFACTToXMLConverter,
    convert_edifact_to_xml,
    convert_edifact_file_to_xml,
    parse_edifact_message,
    validate_edifact_message,
    get_supported_output_formats,
    setup_parser_logging
)

# Utilities and helpers
from .edifact_utils import EDIFACTUtils, DataExtractor, FileProcessor
from .edifact_syntax import EDIFACTSyntax, EDIFACTSyntaxChars
from .edifact_mappings import EDIFACTMappings, MappingContext

# Constants and definitions
from .edifact_constants import (
    ValidationLevel,
    MessageType,
    SegmentGroup,
    OUTPUT_FORMATS,
    ERROR_CODES,
    WARNING_CODES
)

# Version information
__version__ = "1.0.0"
__author__ = "EDIFACT Parser Team"
__description__ = "Professional EDIFACT to XML parser with comprehensive validation and semantic mapping"
__license__ = "MIT"

# Package metadata
__all__ = [
    # Main classes
    'EDIFACTToXMLConverter',
    'EDIFACTParser',
    'XMLGenerator',
    'EDIFACTValidator',
    
    # Configuration classes
    'XMLGeneratorConfig',
    'ValidationLevel',
    
    # Data structures
    'ParsedMessage',
    'ParsedSegment', 
    'ParsedElement',
    'ParsedComponent',
    'ValidationResult',
    
    # Convenience functions
    'convert_edifact_to_xml',
    'convert_edifact_file_to_xml',
    'parse_edifact_message',
    'validate_edifact_message',
    'get_supported_output_formats',
    'setup_parser_logging',
    
    # Utility classes
    'EDIFACTUtils',
    'DataExtractor',
    'FileProcessor',
    'EDIFACTSyntax',
    'EDIFACTMappings',
    
    # Constants and enums
    'MessageType',
    'SegmentGroup',
    'MappingContext',
    'OUTPUT_FORMATS',
    'ERROR_CODES',
    'WARNING_CODES'
]

# Package-level configuration
DEFAULT_CONFIG = {
    'validation_level': ValidationLevel.STANDARD,
    'generate_empty_tags': True,
    'use_semantic_names': True,
    'pretty_print': True,
    'include_statistics': True,
    'include_validation_info': True
}


def get_version() -> str:
    """Get package version"""
    return __version__


def get_package_info() -> dict:
    """Get package information"""
    return {
        'name': 'edifact_parser',
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'license': __license__
    }


def create_converter(**kwargs) -> EDIFACTToXMLConverter:
    """
    Create EDIFACT to XML converter with default configuration.
    
    Args:
        **kwargs: Configuration overrides
        
    Returns:
        Configured EDIFACTToXMLConverter instance
    """
    config = DEFAULT_CONFIG.copy()
    config.update(kwargs)
    return EDIFACTToXMLConverter(**config)


def quick_convert(edifact_content: str, output_format: str = 'xml') -> str:
    """
    Quick conversion function with default settings.
    
    Args:
        edifact_content: Raw EDIFACT message content
        output_format: Output format ('xml', 'json', 'csv')
        
    Returns:
        Converted content as string
    """
    converter = create_converter()
    return converter.convert_to_format(edifact_content, output_format)


def quick_validate(edifact_content: str) -> bool:
    """
    Quick validation function.
    
    Args:
        edifact_content: Raw EDIFACT message content
        
    Returns:
        True if valid, False otherwise
    """
    result = validate_edifact_message(edifact_content)
    return result.get('is_valid', False)


# Initialize logging with default configuration
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

