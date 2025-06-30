#!/usr/bin/env python3
"""
EDIFACT Constants Module
=======================

This module defines constants, enumerations, and configuration values
used throughout the EDIFACT parser.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, List, Set


class EDIFACTVersion(Enum):
    """EDIFACT version identifiers"""
    D93A = "D.93A"
    D96A = "D.96A"
    D96B = "D.96B"
    D97A = "D.97A"
    D97B = "D.97B"
    D98A = "D.98A"
    D98B = "D.98B"
    D99A = "D.99A"
    D99B = "D.99B"
    D00A = "D.00A"
    D00B = "D.00B"
    D01A = "D.01A"
    D01B = "D.01B"
    D01C = "D.01C"
    D02A = "D.02A"
    D02B = "D.02B"
    D03A = "D.03A"
    D03B = "D.03B"


class MessageType(Enum):
    """Common EDIFACT message types"""
    ORDERS = "ORDERS"      # Purchase order message
    ORDRSP = "ORDRSP"      # Purchase order response message
    DESADV = "DESADV"      # Despatch advice message
    RECADV = "RECADV"      # Receiving advice message
    INVOIC = "INVOIC"      # Invoice message
    REMADV = "REMADV"      # Remittance advice message
    PAYORD = "PAYORD"      # Payment order message
    PAYDUC = "PAYDUC"      # Payroll deductions advice message
    PRICAT = "PRICAT"      # Price/sales catalogue message
    INVRPT = "INVRPT"      # Inventory report message
    SLSFCT = "SLSFCT"      # Sales forecast message
    SLSRPT = "SLSRPT"      # Sales data report message
    QUOTES = "QUOTES"      # Quote message
    REQOTE = "REQOTE"      # Request for quote message


class SegmentGroup(Enum):
    """EDIFACT segment groups"""
    SERVICE = "service"        # UNA, UNB, UNH, UNT, UNZ
    HEADER = "header"          # BGM, DTM, RFF, NAD, etc.
    DETAIL = "detail"          # LIN, QTY, PRI, etc.
    SUMMARY = "summary"        # UNS, CNT, etc.


class ElementType(Enum):
    """EDIFACT element types"""
    SIMPLE = "simple"          # Simple data element
    COMPOSITE = "composite"    # Composite data element
    SEGMENT = "segment"        # Segment tag


class ValidationLevel(Enum):
    """Validation levels for EDIFACT parsing"""
    NONE = "none"              # No validation
    BASIC = "basic"            # Basic syntax validation
    STANDARD = "standard"      # Standard EDIFACT validation
    STRICT = "strict"          # Strict validation with all rules


# Default configuration values
DEFAULT_CONFIG = {
    'validation_level': ValidationLevel.STANDARD,
    'generate_empty_tags': True,
    'preserve_whitespace': False,
    'include_segment_attributes': True,
    'include_element_attributes': True,
    'xml_encoding': 'UTF-8',
    'xml_version': '1.0',
    'pretty_print': True,
    'indent_size': 2,
}

# Character encoding mappings
SYNTAX_ENCODINGS = {
    'UNOA': 'ASCII',
    'UNOB': 'ASCII',
    'UNOC': 'ISO-8859-1',
    'UNOD': 'ISO-8859-2',
    'UNOE': 'ISO-8859-5',
    'UNOF': 'ISO-8859-7',
    'UNOG': 'UTF-8',
    'UNOH': 'UTF-8',
    'UNOI': 'UTF-8',
    'UNOJ': 'UTF-8',
    'UNOK': 'UTF-8',
    'UNOL': 'UTF-8',
    'UNOM': 'UTF-8',
    'UNON': 'UTF-8',
    'UNOO': 'UTF-8',
    'UNOP': 'UTF-8',
}

# Service segment tags
SERVICE_SEGMENTS = {
    'UNA', 'UNB', 'UNH', 'UNT', 'UNZ', 'UNS', 'UNG', 'UNE'
}

# Mandatory segments for basic message structure
MANDATORY_SEGMENTS = {
    'UNB',  # Interchange header
    'UNH',  # Message header
    'UNT',  # Message trailer
    'UNZ',  # Interchange trailer
}

# Segment occurrence rules
SEGMENT_OCCURRENCE = {
    'UNA': {'min': 0, 'max': 1},    # Optional, max 1
    'UNB': {'min': 1, 'max': 1},    # Mandatory, exactly 1
    'UNH': {'min': 1, 'max': 1},    # Mandatory, exactly 1
    'BGM': {'min': 0, 'max': 1},    # Optional, max 1
    'DTM': {'min': 0, 'max': 99},   # Optional, max 99
    'RFF': {'min': 0, 'max': 99},   # Optional, max 99
    'NAD': {'min': 0, 'max': 99},   # Optional, max 99
    'LIN': {'min': 0, 'max': 9999}, # Optional, max 9999
    'UNT': {'min': 1, 'max': 1},    # Mandatory, exactly 1
    'UNZ': {'min': 1, 'max': 1},    # Mandatory, exactly 1
}

# XML namespace definitions
XML_NAMESPACES = {
    'edifact': 'http://www.edifact.org/schema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}

# Common date/time formats
DATE_TIME_FORMATS = {
    '102': 'CCYYMMDD',
    '103': 'YYMMDD',
    '203': 'CCYYMMDDHHSS',
    '204': 'CCYYMMDDHHMM',
    '210': 'YYMMDDHHMM',
    '401': 'HHMM',
    '501': 'HHMMSS',
    '600': 'CC',
    '601': 'YY',
    '602': 'MM',
    '603': 'WW',
    '604': 'DD',
    '605': 'DDD',
    '606': 'HH',
    '607': 'NN',
    '608': 'SS',
}

# Error codes and messages
ERROR_CODES = {
    'E001': 'Invalid segment tag',
    'E002': 'Missing mandatory segment',
    'E003': 'Invalid element format',
    'E004': 'Missing mandatory element',
    'E005': 'Invalid qualifier code',
    'E006': 'Invalid date format',
    'E007': 'Invalid time format',
    'E008': 'Invalid numeric value',
    'E009': 'Value exceeds maximum length',
    'E010': 'Value below minimum length',
    'E011': 'Invalid syntax characters',
    'E012': 'Segment occurs too many times',
    'E013': 'Invalid message structure',
    'E014': 'Invalid character encoding',
    'E015': 'Malformed composite element',
}

# Warning codes and messages
WARNING_CODES = {
    'W001': 'Optional segment missing',
    'W002': 'Optional element missing',
    'W003': 'Deprecated qualifier used',
    'W004': 'Non-standard segment order',
    'W005': 'Empty element value',
    'W006': 'Unusual character encoding',
    'W007': 'Large message size',
    'W008': 'Multiple UNA segments',
    'W009': 'Non-standard syntax characters',
    'W010': 'Potential data truncation',
}

# File extensions and MIME types
FILE_EXTENSIONS = {
    'edifact': ['.edi', '.txt', '.dat'],
    'xml': ['.xml'],
    'json': ['.json'],
    'csv': ['.csv'],
}

MIME_TYPES = {
    'edifact': 'application/edifact',
    'xml': 'application/xml',
    'json': 'application/json',
    'csv': 'text/csv',
}

# Performance limits
PERFORMANCE_LIMITS = {
    'max_file_size': 100 * 1024 * 1024,  # 100 MB
    'max_segments': 100000,               # 100K segments
    'max_elements_per_segment': 100,      # 100 elements per segment
    'max_components_per_element': 20,     # 20 components per element
    'max_nesting_depth': 10,              # 10 levels of nesting
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'edifact_parser.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'edifact_parser': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# Regular expressions for validation
VALIDATION_PATTERNS = {
    'segment_tag': r'^[A-Z]{3}$',
    'element_tag': r'^\d{4}$',
    'numeric': r'^\d+$',
    'alphanumeric': r'^[A-Za-z0-9]+$',
    'alphabetic': r'^[A-Za-z]+$',
    'date_yymmdd': r'^\d{6}$',
    'date_ccyymmdd': r'^\d{8}$',
    'time_hhmm': r'^\d{4}$',
    'time_hhmmss': r'^\d{6}$',
    'decimal': r'^\d+(\.\d+)?$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^\+?[\d\s\-\(\)]+$',
    'url': r'^https?://[^\s]+$',
}

# Message type to segment mapping
MESSAGE_SEGMENTS = {
    'ORDERS': {
        'mandatory': ['UNH', 'BGM', 'DTM', 'UNT'],
        'optional': ['RFF', 'NAD', 'CTA', 'COM', 'CUX', 'PAT', 'TDT', 'TOD', 'LIN', 'PIA', 'IMD', 'QTY', 'PRI', 'UNS', 'CNT'],
        'conditional': ['FTX', 'LOC', 'MOA', 'TAX', 'ALC']
    },
    'INVOIC': {
        'mandatory': ['UNH', 'BGM', 'DTM', 'UNT'],
        'optional': ['RFF', 'NAD', 'CTA', 'COM', 'CUX', 'PAT', 'TDT', 'TOD', 'LIN', 'PIA', 'IMD', 'QTY', 'MOA', 'PRI', 'TAX', 'UNS', 'CNT'],
        'conditional': ['FTX', 'LOC', 'ALC', 'RTE']
    },
    'DESADV': {
        'mandatory': ['UNH', 'BGM', 'DTM', 'UNT'],
        'optional': ['RFF', 'NAD', 'CTA', 'COM', 'TDT', 'LOC', 'LIN', 'PIA', 'IMD', 'QTY', 'UNS', 'CNT'],
        'conditional': ['FTX', 'MEA', 'PCI', 'GIN']
    }
}

# Default XML structure template
DEFAULT_XML_STRUCTURE = {
    'root_element': 'EDIFACTMessage',
    'envelope_element': 'Envelope',
    'header_element': 'Header',
    'body_element': 'Body',
    'trailer_element': 'Trailer',
    'segment_element': 'Segment',
    'element_element': 'Element',
    'component_element': 'Component',
}

# Supported output formats
OUTPUT_FORMATS = {
    'xml': {
        'extension': '.xml',
        'mime_type': 'application/xml',
        'description': 'XML format'
    },
    'json': {
        'extension': '.json',
        'mime_type': 'application/json',
        'description': 'JSON format'
    },
    'csv': {
        'extension': '.csv',
        'mime_type': 'text/csv',
        'description': 'CSV format'
    },
    'excel': {
        'extension': '.xlsx',
        'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'description': 'Excel format'
    }
}

# Character sets and their descriptions
CHARACTER_SETS = {
    'UNOA': {
        'name': 'ASCII',
        'description': 'ASCII character set (7-bit)',
        'characters': 'A-Z, 0-9, space, and selected special characters'
    },
    'UNOB': {
        'name': 'ASCII',
        'description': 'ASCII character set (7-bit) with lowercase',
        'characters': 'A-Z, a-z, 0-9, space, and selected special characters'
    },
    'UNOC': {
        'name': 'ISO 8859-1',
        'description': 'Latin-1 character set',
        'characters': 'Extended ASCII with Western European characters'
    },
    'UNOD': {
        'name': 'ISO 8859-2',
        'description': 'Latin-2 character set',
        'characters': 'Extended ASCII with Central European characters'
    },
    'UNOE': {
        'name': 'ISO 8859-5',
        'description': 'Cyrillic character set',
        'characters': 'Extended ASCII with Cyrillic characters'
    },
    'UNOF': {
        'name': 'ISO 8859-7',
        'description': 'Greek character set',
        'characters': 'Extended ASCII with Greek characters'
    },
}

# Status codes for processing results
STATUS_CODES = {
    'SUCCESS': 0,
    'WARNING': 1,
    'ERROR': 2,
    'FATAL_ERROR': 3,
}

# Processing statistics keys
STATISTICS_KEYS = [
    'total_segments',
    'total_elements',
    'total_components',
    'processing_time',
    'file_size',
    'validation_errors',
    'validation_warnings',
    'segments_by_type',
    'elements_by_type',
]

