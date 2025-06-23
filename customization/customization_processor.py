#!/usr/bin/env python3
"""
Customization Processor for EDI Customization Layer
===================================================

This module provides the main processing engine that coordinates
all customization components to transform EDI data into customer-specific XML.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import logging
from datetime import datetime

from .data_readers import DataReaderFactory
from .rule_engine import RuleEngine, DocumentTypeFilter, CustomerGLNFilter, FieldExtractor
from .mapping_engine import MappingEngine, FieldMapping, MappingConfiguration, TransformationType
from .xml_customizer import CustomXMLGenerator, TemplateProcessor, XMLTemplate
from .configuration_manager import ConfigurationManager, DocumentTypeConfig, CustomerConfig, MappingConfig

logger = logging.getLogger(__name__)


class ProcessingResult:
    """Result of customization processing"""
    
    def __init__(self):
        self.success = False
        self.output_data = {}
        self.output_xml = ""
        self.errors = []
        self.warnings = []
        self.processing_stats = {}
        self.metadata = {}
    
    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str):
        """Add a warning message"""
        self.warnings.append(warning)
    
    def set_success(self, output_data: Dict[str, Any], output_xml: str):
        """Set successful result"""
        self.success = True
        self.output_data = output_data
        self.output_xml = output_xml
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            'success': self.success,
            'output_data': self.output_data,
            'output_xml': self.output_xml,
            'errors': self.errors,
            'warnings': self.warnings,
            'processing_stats': self.processing_stats,
            'metadata': self.metadata
        }


class CustomizationProcessor:
    """Main processor for EDI customization"""
    
    def __init__(self, config_manager: Optional[ConfigurationManager] = None):
        self.config_manager = config_manager or ConfigurationManager()
        self.rule_engine = RuleEngine()
        self.mapping_engine = MappingEngine()
        self.xml_generator = CustomXMLGenerator()
        self.data_reader_factory = DataReaderFactory()
        
        self.logger = logging.getLogger(f"{__name__}.CustomizationProcessor")
        
        # Initialize with default filters
        self._setup_default_filters()
        self._load_configurations()
    
    def process_file(self, input_file: Union[str, Path], document_type: str, 
                    customer_gln: Optional[str] = None, output_template: Optional[str] = None,
                    validation_level: str = "standard") -> ProcessingResult:
        """Process a single EDI file"""
        result = ProcessingResult()
        
        try:
            # Record processing start
            start_time = datetime.now()
            result.metadata['processing_start'] = start_time.isoformat()
            result.metadata['input_file'] = str(input_file)
            result.metadata['document_type'] = document_type
            result.metadata['customer_gln'] = customer_gln
            
            # Step 1: Read input data
            self.logger.info(f"Reading input file: {input_file}")
            try:
                input_data = self.data_reader_factory.read_data(input_file)
                result.processing_stats['input_segments'] = len(input_data.get('segments', []))
            except Exception as e:
                result.add_error(f"Error reading input file: {str(e)}")
                return result
            
            # Step 2: Apply rule-based filtering
            self.logger.info("Applying rule-based filtering")
            try:
                filtered_data = self.rule_engine.apply_all_filters(input_data)
                if not filtered_data:
                    result.add_error("Data was filtered out by rules")
                    return result
                result.processing_stats['filtered_segments'] = len(filtered_data.get('segments', []))
            except Exception as e:
                result.add_error(f"Error in rule filtering: {str(e)}")
                return result
            
            # Step 3: Apply field mapping and transformation
            self.logger.info("Applying field mapping and transformation")
            try:
                mapped_data = self.mapping_engine.apply_mapping(filtered_data, document_type, customer_gln)
                result.processing_stats['mapped_fields'] = len(mapped_data)
            except Exception as e:
                result.add_error(f"Error in field mapping: {str(e)}")
                return result
            
            # Step 4: Generate custom XML
            self.logger.info("Generating custom XML")
            try:
                if output_template:
                    xml_output = self.xml_generator.generate_xml(mapped_data, output_template)
                else:
                    # Use default structure generation
                    root_name = self._get_root_element_name(document_type)
                    xml_output = self.xml_generator.generate_xml_from_structure(mapped_data, root_name)
                
                result.processing_stats['xml_size'] = len(xml_output)
            except Exception as e:
                result.add_error(f"Error generating XML: {str(e)}")
                return result
            
            # Step 5: Validation (if enabled)
            if validation_level != "none":
                self.logger.info("Validating output")
                try:
                    validation_result = self._validate_output(mapped_data, document_type, customer_gln)
                    if not validation_result['is_valid']:
                        for error in validation_result['errors']:
                            result.add_error(f"Validation error: {error}")
                        if validation_level == "strict":
                            return result
                    
                    for warning in validation_result['warnings']:
                        result.add_warning(f"Validation warning: {warning}")
                        
                except Exception as e:
                    result.add_warning(f"Error in validation: {str(e)}")
            
            # Success
            end_time = datetime.now()
            result.metadata['processing_end'] = end_time.isoformat()
            result.metadata['processing_duration'] = str(end_time - start_time)
            
            result.set_success(mapped_data, xml_output)
            self.logger.info(f"Successfully processed {input_file}")
            
        except Exception as e:
            result.add_error(f"Unexpected error in processing: {str(e)}")
            self.logger.error(f"Error processing file {input_file}: {e}")
        
        return result
    
    def process_data(self, input_data: Dict[str, Any], document_type: str,
                    customer_gln: Optional[str] = None, output_template: Optional[str] = None,
                    validation_level: str = "standard") -> ProcessingResult:
        """Process EDI data directly (without file reading)"""
        result = ProcessingResult()
        
        try:
            # Record processing start
            start_time = datetime.now()
            result.metadata['processing_start'] = start_time.isoformat()
            result.metadata['document_type'] = document_type
            result.metadata['customer_gln'] = customer_gln
            
            # Step 1: Apply rule-based filtering
            self.logger.info("Applying rule-based filtering")
            filtered_data = self.rule_engine.apply_all_filters(input_data)
            if not filtered_data:
                result.add_error("Data was filtered out by rules")
                return result
            
            # Step 2: Apply field mapping and transformation
            self.logger.info("Applying field mapping and transformation")
            mapped_data = self.mapping_engine.apply_mapping(filtered_data, document_type, customer_gln)
            
            # Step 3: Generate custom XML
            self.logger.info("Generating custom XML")
            if output_template:
                xml_output = self.xml_generator.generate_xml(mapped_data, output_template)
            else:
                root_name = self._get_root_element_name(document_type)
                xml_output = self.xml_generator.generate_xml_from_structure(mapped_data, root_name)
            
            # Step 4: Validation (if enabled)
            if validation_level != "none":
                validation_result = self._validate_output(mapped_data, document_type, customer_gln)
                if not validation_result['is_valid']:
                    for error in validation_result['errors']:
                        result.add_error(f"Validation error: {error}")
                    if validation_level == "strict":
                        return result
                
                for warning in validation_result['warnings']:
                    result.add_warning(f"Validation warning: {warning}")
            
            # Success
            end_time = datetime.now()
            result.metadata['processing_end'] = end_time.isoformat()
            result.metadata['processing_duration'] = str(end_time - start_time)
            
            result.set_success(mapped_data, xml_output)
            self.logger.info("Successfully processed data")
            
        except Exception as e:
            result.add_error(f"Error in processing: {str(e)}")
            self.logger.error(f"Error processing data: {e}")
        
        return result
    
    def add_custom_template(self, template: XMLTemplate):
        """Add a custom XML template"""
        self.xml_generator.template_processor.load_template(template)
        self.logger.info(f"Added custom template: {template.name}")
    
    def add_custom_mapping(self, mapping_config: MappingConfiguration):
        """Add a custom mapping configuration"""
        self.mapping_engine.add_configuration(mapping_config)
        self.logger.info(f"Added custom mapping: {mapping_config.document_type}/{mapping_config.customer_gln}")
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'available_document_types': self.config_manager.list_document_types(),
            'available_customers': self.config_manager.list_customers(),
            'available_mappings': self.mapping_engine.get_available_configurations(),
            'available_templates': list(self.xml_generator.template_processor.templates.keys())
        }
    
    def _setup_default_filters(self):
        """Setup default filters in the rule engine"""
        # Add document type filter
        doc_filter = DocumentTypeFilter()
        self.rule_engine.add_filter(doc_filter)
        
        # Add customer GLN filter
        gln_filter = CustomerGLNFilter()
        self.rule_engine.add_filter(gln_filter)
        
        # Add field extractor
        field_extractor = FieldExtractor()
        self.rule_engine.add_filter(field_extractor)
    
    def _load_configurations(self):
        """Load configurations into engines"""
        # Load mapping configurations into mapping engine
        for mapping_key in self.config_manager.list_mapping_configs():
            parts = mapping_key.split(':')
            document_type = parts[0]
            customer_gln = parts[1] if parts[1] != 'default' else None
            
            mapping_config = self.config_manager.get_mapping_config(document_type, customer_gln)
            if mapping_config:
                # Convert to MappingConfiguration format
                field_mappings = []
                for mapping_data in mapping_config.field_mappings:
                    field_mapping = FieldMapping(
                        source_path=mapping_data.get('source_path', ''),
                        target_path=mapping_data.get('target_path', ''),
                        transformation_type=TransformationType(mapping_data.get('transformation_type', 'copy')),
                        transformation_config=mapping_data.get('transformation_config', {}),
                        required=mapping_data.get('required', False),
                        default_value=mapping_data.get('default_value'),
                        description=mapping_data.get('description', '')
                    )
                    field_mappings.append(field_mapping)
                
                mapping_configuration = MappingConfiguration(
                    document_type=mapping_config.document_type,
                    customer_gln=mapping_config.customer_gln,
                    target_structure=mapping_config.target_format,
                    field_mappings=field_mappings,
                    global_transformations=mapping_config.transformation_rules,
                    metadata=mapping_config.metadata
                )
                
                self.mapping_engine.add_configuration(mapping_configuration)
    
    def _get_root_element_name(self, document_type: str) -> str:
        """Get root element name for document type"""
        root_names = {
            'ORDERS': 'PurchaseOrder',
            'INVOIC': 'Invoice',
            'DESADV': 'DeliveryNotification',
            'ORDRSP': 'OrderResponse',
            'REMADV': 'PaymentAdvice'
        }
        return root_names.get(document_type, 'EDIDocument')
    
    def _validate_output(self, data: Dict[str, Any], document_type: str, 
                        customer_gln: Optional[str]) -> Dict[str, Any]:
        """Validate output data"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Basic validation
        if not data:
            validation_result['errors'].append("Output data is empty")
            validation_result['is_valid'] = False
        
        # Document type specific validation
        doc_config = self.config_manager.get_document_type_config(document_type)
        if doc_config:
            # Check for required business data
            if document_type == 'ORDERS':
                if 'order_number' not in data:
                    validation_result['warnings'].append("Order number not found")
                if 'buyer' not in data:
                    validation_result['warnings'].append("Buyer information not found")
            elif document_type == 'INVOIC':
                if 'invoice_number' not in data:
                    validation_result['warnings'].append("Invoice number not found")
                if 'total_amount' not in data:
                    validation_result['warnings'].append("Total amount not found")
        
        return validation_result


class BatchProcessor:
    """Batch processor for multiple files"""
    
    def __init__(self, customization_processor: Optional[CustomizationProcessor] = None):
        self.processor = customization_processor or CustomizationProcessor()
        self.logger = logging.getLogger(f"{__name__}.BatchProcessor")
    
    def process_directory(self, input_directory: Union[str, Path], output_directory: Union[str, Path],
                         document_type: str, customer_gln: Optional[str] = None,
                         file_pattern: str = "*.xml", output_template: Optional[str] = None) -> Dict[str, Any]:
        """Process all files in a directory"""
        input_dir = Path(input_directory)
        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'total_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'file_results': {},
            'summary': {}
        }
        
        try:
            # Find all matching files
            files = list(input_dir.glob(file_pattern))
            results['total_files'] = len(files)
            
            self.logger.info(f"Processing {len(files)} files from {input_dir}")
            
            for file_path in files:
                try:
                    # Process file
                    result = self.processor.process_file(
                        file_path, document_type, customer_gln, output_template
                    )
                    
                    # Save result
                    if result.success:
                        output_file = output_dir / f"{file_path.stem}_customized.xml"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(result.output_xml)
                        
                        results['successful_files'] += 1
                        self.logger.info(f"Successfully processed: {file_path}")
                    else:
                        results['failed_files'] += 1
                        self.logger.error(f"Failed to process: {file_path}")
                    
                    results['file_results'][str(file_path)] = result.to_dict()
                    
                except Exception as e:
                    results['failed_files'] += 1
                    results['file_results'][str(file_path)] = {
                        'success': False,
                        'errors': [str(e)]
                    }
                    self.logger.error(f"Error processing {file_path}: {e}")
            
            # Generate summary
            results['summary'] = {
                'success_rate': results['successful_files'] / results['total_files'] if results['total_files'] > 0 else 0,
                'processing_completed': True
            }
            
        except Exception as e:
            results['summary'] = {
                'success_rate': 0,
                'processing_completed': False,
                'error': str(e)
            }
            self.logger.error(f"Error in batch processing: {e}")
        
        return results
    
    def process_file_list(self, file_list: List[Union[str, Path]], output_directory: Union[str, Path],
                         document_type: str, customer_gln: Optional[str] = None,
                         output_template: Optional[str] = None) -> Dict[str, Any]:
        """Process a list of specific files"""
        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'total_files': len(file_list),
            'successful_files': 0,
            'failed_files': 0,
            'file_results': {},
            'summary': {}
        }
        
        for file_path in file_list:
            try:
                file_path = Path(file_path)
                
                # Process file
                result = self.processor.process_file(
                    file_path, document_type, customer_gln, output_template
                )
                
                # Save result
                if result.success:
                    output_file = output_dir / f"{file_path.stem}_customized.xml"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.output_xml)
                    
                    results['successful_files'] += 1
                else:
                    results['failed_files'] += 1
                
                results['file_results'][str(file_path)] = result.to_dict()
                
            except Exception as e:
                results['failed_files'] += 1
                results['file_results'][str(file_path)] = {
                    'success': False,
                    'errors': [str(e)]
                }
        
        # Generate summary
        results['summary'] = {
            'success_rate': results['successful_files'] / results['total_files'] if results['total_files'] > 0 else 0,
            'processing_completed': True
        }
        
        return results


# Convenience functions
def process_single_file(input_file: Union[str, Path], output_file: Union[str, Path],
                       document_type: str, customer_gln: Optional[str] = None) -> bool:
    """Process a single file with default settings"""
    processor = CustomizationProcessor()
    result = processor.process_file(input_file, document_type, customer_gln)
    
    if result.success:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.output_xml)
        return True
    else:
        logger.error(f"Processing failed: {result.errors}")
        return False


def create_default_processor() -> CustomizationProcessor:
    """Create a processor with default configurations"""
    processor = CustomizationProcessor()
    
    # Add default templates
    from .xml_customizer import create_purchase_order_template, create_invoice_template
    
    processor.add_custom_template(create_purchase_order_template())
    processor.add_custom_template(create_invoice_template())
    
    return processor

