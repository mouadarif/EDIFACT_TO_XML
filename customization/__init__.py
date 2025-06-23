#!/usr/bin/env python3
"""
EDI Customization Layer
======================

This module provides a customization layer for EDI data processing,
enabling customer-specific and document-specific XML generation.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from .data_readers import (
    XMLDataReader,
    CSVDataReader, 
    JSONDataReader,
    DataReaderFactory
)

from .rule_engine import (
    RuleEngine,
    DocumentTypeFilter,
    CustomerGLNFilter,
    FieldExtractor
)

from .mapping_engine import (
    MappingEngine,
    FieldMapper,
    DataTransformer
)

from .xml_customizer import (
    CustomXMLGenerator,
    TemplateProcessor,
    XMLStructureValidator
)

from .configuration_manager import (
    ConfigurationManager,
    DocumentTypeConfig,
    CustomerConfig,
    MappingConfig,
    create_orders_document_config,
    create_invoice_document_config,
    create_sample_customer_config
)

from .customization_processor import (
    CustomizationProcessor,
    BatchProcessor
)

__all__ = [
    # Data Readers
    'XMLDataReader',
    'CSVDataReader', 
    'JSONDataReader',
    'DataReaderFactory',
    
    # Rule Engine
    'RuleEngine',
    'DocumentTypeFilter',
    'CustomerGLNFilter',
    'FieldExtractor',
    
    # Mapping Engine
    'MappingEngine',
    'FieldMapper',
    'DataTransformer',
    
    # XML Customizer
    'CustomXMLGenerator',
    'TemplateProcessor',
    'XMLStructureValidator',
    
    # Configuration
    'ConfigurationManager',
    'DocumentTypeConfig',
    'CustomerConfig',
    'MappingConfig',
    'create_orders_document_config',
    'create_invoice_document_config',
    'create_sample_customer_config',
    
    # Main Processor
    'CustomizationProcessor',
    'BatchProcessor'
]

__version__ = "1.0.0"

