#!/usr/bin/env python3
"""
Configuration Manager for EDI Customization Layer
=================================================

This module manages configurations for document types, customers,
and mapping rules in the EDI customization system.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfigFormat(Enum):
    """Configuration file formats"""
    JSON = "json"
    YAML = "yaml"
    XML = "xml"


@dataclass
class DocumentTypeConfig:
    """Configuration for a specific document type"""
    document_type: str
    document_code: str
    description: str = ""
    required_segments: List[str] = field(default_factory=list)
    optional_segments: List[str] = field(default_factory=list)
    business_rules: Dict[str, Any] = field(default_factory=dict)
    default_mappings: Dict[str, str] = field(default_factory=dict)
    validation_rules: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CustomerConfig:
    """Configuration for a specific customer"""
    customer_gln: str
    customer_name: str = ""
    contact_info: Dict[str, str] = field(default_factory=dict)
    document_preferences: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    field_mappings: Dict[str, Dict[str, str]] = field(default_factory=dict)
    transformation_rules: Dict[str, Any] = field(default_factory=dict)
    output_formats: List[str] = field(default_factory=list)
    special_requirements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MappingConfig:
    """Configuration for field mappings"""
    config_name: str
    document_type: str
    customer_gln: Optional[str] = None
    target_format: str = "xml"
    field_mappings: List[Dict[str, Any]] = field(default_factory=list)
    transformation_rules: Dict[str, Any] = field(default_factory=dict)
    output_template: str = ""
    validation_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConfigurationManager:
    """Main configuration manager"""
    
    def __init__(self, config_directory: Optional[Union[str, Path]] = None):
        self.config_directory = Path(config_directory) if config_directory else Path("./config")
        self.config_directory.mkdir(exist_ok=True)
        
        self.document_configs: Dict[str, DocumentTypeConfig] = {}
        self.customer_configs: Dict[str, CustomerConfig] = {}
        self.mapping_configs: Dict[str, MappingConfig] = {}
        
        self.logger = logging.getLogger(f"{__name__}.ConfigurationManager")
        
        # Load existing configurations
        self._load_all_configurations()
    
    # Document Type Configuration Management
    def add_document_type_config(self, config: DocumentTypeConfig):
        """Add or update document type configuration"""
        self.document_configs[config.document_type] = config
        self._save_document_config(config)
        self.logger.info(f"Added document type config: {config.document_type}")
    
    def get_document_type_config(self, document_type: str) -> Optional[DocumentTypeConfig]:
        """Get document type configuration"""
        return self.document_configs.get(document_type)
    
    def remove_document_type_config(self, document_type: str):
        """Remove document type configuration"""
        if document_type in self.document_configs:
            del self.document_configs[document_type]
            config_file = self.config_directory / "document_types" / f"{document_type}.json"
            if config_file.exists():
                config_file.unlink()
            self.logger.info(f"Removed document type config: {document_type}")
    
    def list_document_types(self) -> List[str]:
        """List all configured document types"""
        return list(self.document_configs.keys())
    
    # Customer Configuration Management
    def add_customer_config(self, config: CustomerConfig):
        """Add or update customer configuration"""
        self.customer_configs[config.customer_gln] = config
        self._save_customer_config(config)
        self.logger.info(f"Added customer config: {config.customer_gln}")
    
    def get_customer_config(self, customer_gln: str) -> Optional[CustomerConfig]:
        """Get customer configuration"""
        return self.customer_configs.get(customer_gln)
    
    def remove_customer_config(self, customer_gln: str):
        """Remove customer configuration"""
        if customer_gln in self.customer_configs:
            del self.customer_configs[customer_gln]
            config_file = self.config_directory / "customers" / f"{customer_gln}.json"
            if config_file.exists():
                config_file.unlink()
            self.logger.info(f"Removed customer config: {customer_gln}")
    
    def list_customers(self) -> List[str]:
        """List all configured customers"""
        return list(self.customer_configs.keys())
    
    # Mapping Configuration Management
    def add_mapping_config(self, config: MappingConfig):
        """Add or update mapping configuration"""
        config_key = self._get_mapping_key(config.document_type, config.customer_gln)
        self.mapping_configs[config_key] = config
        self._save_mapping_config(config)
        self.logger.info(f"Added mapping config: {config_key}")
    
    def get_mapping_config(self, document_type: str, customer_gln: Optional[str] = None) -> Optional[MappingConfig]:
        """Get mapping configuration"""
        # Try specific customer mapping first
        if customer_gln:
            config_key = self._get_mapping_key(document_type, customer_gln)
            if config_key in self.mapping_configs:
                return self.mapping_configs[config_key]
        
        # Fall back to general document type mapping
        config_key = self._get_mapping_key(document_type, None)
        return self.mapping_configs.get(config_key)
    
    def remove_mapping_config(self, document_type: str, customer_gln: Optional[str] = None):
        """Remove mapping configuration"""
        config_key = self._get_mapping_key(document_type, customer_gln)
        if config_key in self.mapping_configs:
            del self.mapping_configs[config_key]
            config_file = self.config_directory / "mappings" / f"{config_key}.json"
            if config_file.exists():
                config_file.unlink()
            self.logger.info(f"Removed mapping config: {config_key}")
    
    def list_mapping_configs(self) -> List[str]:
        """List all mapping configurations"""
        return list(self.mapping_configs.keys())
    
    # Configuration File Management
    def export_configuration(self, output_file: Union[str, Path], format_type: ConfigFormat = ConfigFormat.JSON):
        """Export all configurations to a file"""
        try:
            export_data = {
                'document_types': {k: asdict(v) for k, v in self.document_configs.items()},
                'customers': {k: asdict(v) for k, v in self.customer_configs.items()},
                'mappings': {k: asdict(v) for k, v in self.mapping_configs.items()},
                'metadata': {
                    'export_timestamp': str(Path().cwd()),
                    'version': '1.0.0'
                }
            }
            
            output_path = Path(output_file)
            
            if format_type == ConfigFormat.JSON:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            elif format_type == ConfigFormat.YAML:
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"Exported configuration to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {e}")
            raise
    
    def import_configuration(self, input_file: Union[str, Path], format_type: Optional[ConfigFormat] = None):
        """Import configurations from a file"""
        try:
            input_path = Path(input_file)
            
            if format_type is None:
                # Auto-detect format from extension
                if input_path.suffix.lower() == '.yaml' or input_path.suffix.lower() == '.yml':
                    format_type = ConfigFormat.YAML
                else:
                    format_type = ConfigFormat.JSON
            
            # Load data
            if format_type == ConfigFormat.JSON:
                with open(input_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
            elif format_type == ConfigFormat.YAML:
                with open(input_path, 'r', encoding='utf-8') as f:
                    import_data = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            # Import document types
            if 'document_types' in import_data:
                for doc_type, config_data in import_data['document_types'].items():
                    config = DocumentTypeConfig(**config_data)
                    self.add_document_type_config(config)
            
            # Import customers
            if 'customers' in import_data:
                for gln, config_data in import_data['customers'].items():
                    config = CustomerConfig(**config_data)
                    self.add_customer_config(config)
            
            # Import mappings
            if 'mappings' in import_data:
                for mapping_key, config_data in import_data['mappings'].items():
                    config = MappingConfig(**config_data)
                    self.add_mapping_config(config)
            
            self.logger.info(f"Imported configuration from {input_path}")
            
        except Exception as e:
            self.logger.error(f"Error importing configuration: {e}")
            raise
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate all configurations"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'document_types': {},
            'customers': {},
            'mappings': {}
        }
        
        # Validate document type configurations
        for doc_type, config in self.document_configs.items():
            doc_validation = self._validate_document_config(config)
            validation_result['document_types'][doc_type] = doc_validation
            if not doc_validation['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(doc_validation['errors'])
        
        # Validate customer configurations
        for gln, config in self.customer_configs.items():
            customer_validation = self._validate_customer_config(config)
            validation_result['customers'][gln] = customer_validation
            if not customer_validation['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(customer_validation['errors'])
        
        # Validate mapping configurations
        for mapping_key, config in self.mapping_configs.items():
            mapping_validation = self._validate_mapping_config(config)
            validation_result['mappings'][mapping_key] = mapping_validation
            if not mapping_validation['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(mapping_validation['errors'])
        
        return validation_result
    
    # Private helper methods
    def _get_mapping_key(self, document_type: str, customer_gln: Optional[str]) -> str:
        """Generate mapping configuration key"""
        return f"{document_type}:{customer_gln or 'default'}"
    
    def _load_all_configurations(self):
        """Load all existing configurations from files"""
        try:
            # Load document type configurations
            doc_types_dir = self.config_directory / "document_types"
            if doc_types_dir.exists():
                for config_file in doc_types_dir.glob("*.json"):
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config_data = json.load(f)
                        config = DocumentTypeConfig(**config_data)
                        self.document_configs[config.document_type] = config
                    except Exception as e:
                        self.logger.error(f"Error loading document config {config_file}: {e}")
            
            # Load customer configurations
            customers_dir = self.config_directory / "customers"
            if customers_dir.exists():
                for config_file in customers_dir.glob("*.json"):
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config_data = json.load(f)
                        config = CustomerConfig(**config_data)
                        self.customer_configs[config.customer_gln] = config
                    except Exception as e:
                        self.logger.error(f"Error loading customer config {config_file}: {e}")
            
            # Load mapping configurations
            mappings_dir = self.config_directory / "mappings"
            if mappings_dir.exists():
                for config_file in mappings_dir.glob("*.json"):
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config_data = json.load(f)
                        config = MappingConfig(**config_data)
                        config_key = self._get_mapping_key(config.document_type, config.customer_gln)
                        self.mapping_configs[config_key] = config
                    except Exception as e:
                        self.logger.error(f"Error loading mapping config {config_file}: {e}")
            
        except Exception as e:
            self.logger.error(f"Error loading configurations: {e}")
    
    def _save_document_config(self, config: DocumentTypeConfig):
        """Save document type configuration to file"""
        try:
            doc_types_dir = self.config_directory / "document_types"
            doc_types_dir.mkdir(exist_ok=True)
            
            config_file = doc_types_dir / f"{config.document_type}.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving document config: {e}")
    
    def _save_customer_config(self, config: CustomerConfig):
        """Save customer configuration to file"""
        try:
            customers_dir = self.config_directory / "customers"
            customers_dir.mkdir(exist_ok=True)
            
            config_file = customers_dir / f"{config.customer_gln}.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving customer config: {e}")
    
    def _save_mapping_config(self, config: MappingConfig):
        """Save mapping configuration to file"""
        try:
            mappings_dir = self.config_directory / "mappings"
            mappings_dir.mkdir(exist_ok=True)
            
            config_key = self._get_mapping_key(config.document_type, config.customer_gln)
            config_file = mappings_dir / f"{config_key}.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving mapping config: {e}")
    
    def _validate_document_config(self, config: DocumentTypeConfig) -> Dict[str, Any]:
        """Validate document type configuration"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not config.document_type:
            validation_result['errors'].append("Document type is required")
            validation_result['is_valid'] = False
        
        if not config.document_code:
            validation_result['errors'].append("Document code is required")
            validation_result['is_valid'] = False
        
        return validation_result
    
    def _validate_customer_config(self, config: CustomerConfig) -> Dict[str, Any]:
        """Validate customer configuration"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not config.customer_gln:
            validation_result['errors'].append("Customer GLN is required")
            validation_result['is_valid'] = False
        
        # Validate GLN format (13 digits)
        if config.customer_gln and (len(config.customer_gln) != 13 or not config.customer_gln.isdigit()):
            validation_result['warnings'].append("GLN should be 13 digits")
        
        return validation_result
    
    def _validate_mapping_config(self, config: MappingConfig) -> Dict[str, Any]:
        """Validate mapping configuration"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not config.config_name:
            validation_result['errors'].append("Configuration name is required")
            validation_result['is_valid'] = False
        
        if not config.document_type:
            validation_result['errors'].append("Document type is required")
            validation_result['is_valid'] = False
        
        return validation_result


# Convenience functions for creating common configurations
def create_orders_document_config() -> DocumentTypeConfig:
    """Create configuration for ORDERS document type"""
    return DocumentTypeConfig(
        document_type="ORDERS",
        document_code="850",
        description="Purchase Order",
        required_segments=["UNB", "UNH", "BGM", "DTM", "NAD", "LIN", "UNT", "UNZ"],
        optional_segments=["RFF", "CUX", "PAT", "TDT", "LOC", "QTY", "PRI", "MOA"],
        business_rules={
            "min_line_items": 1,
            "max_line_items": 9999,
            "currency_required": True
        },
        default_mappings={
            "order_number": "business_data.references.ON",
            "order_date": "business_data.dates.137",
            "buyer": "business_data.parties.BY",
            "supplier": "business_data.parties.SU"
        }
    )


def create_invoice_document_config() -> DocumentTypeConfig:
    """Create configuration for INVOIC document type"""
    return DocumentTypeConfig(
        document_type="INVOIC",
        document_code="810",
        description="Invoice",
        required_segments=["UNB", "UNH", "BGM", "DTM", "NAD", "LIN", "MOA", "UNT", "UNZ"],
        optional_segments=["RFF", "CUX", "PAT", "TDT", "LOC", "QTY", "PRI", "TAX"],
        business_rules={
            "min_line_items": 1,
            "total_amount_required": True,
            "tax_calculation_required": True
        },
        default_mappings={
            "invoice_number": "business_data.references.IV",
            "invoice_date": "business_data.dates.137",
            "supplier": "business_data.parties.SU",
            "customer": "business_data.parties.BY"
        }
    )


def create_sample_customer_config(gln: str, name: str) -> CustomerConfig:
    """Create a sample customer configuration"""
    return CustomerConfig(
        customer_gln=gln,
        customer_name=name,
        document_preferences={
            "ORDERS": {
                "require_delivery_date": True,
                "max_line_items": 100,
                "currency": "EUR"
            },
            "INVOIC": {
                "require_tax_breakdown": True,
                "payment_terms_required": True
            }
        },
        output_formats=["xml", "json"],
        special_requirements=[
            "Include all empty fields",
            "Use customer-specific item codes"
        ]
    )

