#!/usr/bin/env python3
"""
Mapping Engine for EDI Customization Layer
==========================================

This module provides mapping and transformation capabilities for converting
EDI data to customer-specific XML structures.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Callable, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TransformationType(Enum):
    """Types of data transformations"""
    COPY = "copy"                    # Direct copy
    FORMAT = "format"                # Format transformation
    CALCULATE = "calculate"          # Calculated field
    LOOKUP = "lookup"               # Lookup table
    CONDITIONAL = "conditional"      # Conditional logic
    AGGREGATE = "aggregate"         # Aggregation
    SPLIT = "split"                 # Split field
    COMBINE = "combine"             # Combine fields


@dataclass
class FieldMapping:
    """Represents a field mapping configuration"""
    source_path: str                 # Source field path (dot notation)
    target_path: str                 # Target field path (dot notation)
    transformation_type: TransformationType = TransformationType.COPY
    transformation_config: Dict[str, Any] = field(default_factory=dict)
    required: bool = False
    default_value: Any = None
    validation_rules: List[str] = field(default_factory=list)
    description: str = ""
    
    def __post_init__(self):
        if not self.description:
            self.description = f"Map {self.source_path} to {self.target_path}"


@dataclass
class MappingConfiguration:
    """Complete mapping configuration for a document type/customer"""
    document_type: str
    customer_gln: Optional[str] = None
    target_structure: str = "default"
    field_mappings: List[FieldMapping] = field(default_factory=list)
    global_transformations: Dict[str, Any] = field(default_factory=dict)
    validation_rules: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataTransformer:
    """Handles data transformations"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DataTransformer")
        self._transformation_functions = {
            TransformationType.COPY: self._copy_transform,
            TransformationType.FORMAT: self._format_transform,
            TransformationType.CALCULATE: self._calculate_transform,
            TransformationType.LOOKUP: self._lookup_transform,
            TransformationType.CONDITIONAL: self._conditional_transform,
            TransformationType.AGGREGATE: self._aggregate_transform,
            TransformationType.SPLIT: self._split_transform,
            TransformationType.COMBINE: self._combine_transform
        }
    
    def transform_value(self, value: Any, transformation_type: TransformationType, 
                       config: Dict[str, Any], context: Dict[str, Any] = None) -> Any:
        """Transform a value according to the specified transformation"""
        try:
            if transformation_type in self._transformation_functions:
                return self._transformation_functions[transformation_type](value, config, context or {})
            else:
                self.logger.warning(f"Unknown transformation type: {transformation_type}")
                return value
                
        except Exception as e:
            self.logger.error(f"Error in transformation {transformation_type}: {e}")
            return value
    
    def _copy_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Direct copy transformation"""
        return value
    
    def _format_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Format transformation (dates, numbers, strings)"""
        format_type = config.get('format_type', 'string')
        format_pattern = config.get('pattern', '')
        
        if format_type == 'date':
            return self._format_date(value, format_pattern, config)
        elif format_type == 'number':
            return self._format_number(value, format_pattern, config)
        elif format_type == 'string':
            return self._format_string(value, format_pattern, config)
        else:
            return str(value)
    
    def _calculate_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Calculate transformation using expressions"""
        expression = config.get('expression', '')
        variables = config.get('variables', {})
        
        # Simple calculation support
        try:
            # Replace variables in expression
            calc_expression = expression
            for var_name, var_path in variables.items():
                var_value = self._get_context_value(context, var_path)
                calc_expression = calc_expression.replace(f'{{{var_name}}}', str(var_value or 0))
            
            # Evaluate simple mathematical expressions
            # Note: In production, use a safer expression evaluator
            if re.match(r'^[\d\s+\-*/().]+$', calc_expression):
                return eval(calc_expression)
            else:
                return value
                
        except Exception as e:
            self.logger.error(f"Error in calculation: {e}")
            return value
    
    def _lookup_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Lookup transformation using lookup tables"""
        lookup_table = config.get('lookup_table', {})
        default_value = config.get('default', value)
        
        return lookup_table.get(str(value), default_value)
    
    def _conditional_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Conditional transformation"""
        conditions = config.get('conditions', [])
        default_value = config.get('default', value)
        
        for condition in conditions:
            condition_expr = condition.get('condition', '')
            result_value = condition.get('value', value)
            
            if self._evaluate_condition(value, condition_expr, context):
                return result_value
        
        return default_value
    
    def _aggregate_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Aggregate transformation (sum, count, etc.)"""
        operation = config.get('operation', 'sum')
        source_array = config.get('source_array', [])
        
        if not isinstance(source_array, list):
            return value
        
        if operation == 'sum':
            return sum(float(x) for x in source_array if self._is_numeric(x))
        elif operation == 'count':
            return len(source_array)
        elif operation == 'avg':
            numeric_values = [float(x) for x in source_array if self._is_numeric(x)]
            return sum(numeric_values) / len(numeric_values) if numeric_values else 0
        else:
            return value
    
    def _split_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Split transformation"""
        delimiter = config.get('delimiter', ' ')
        index = config.get('index', 0)
        
        if isinstance(value, str):
            parts = value.split(delimiter)
            if 0 <= index < len(parts):
                return parts[index]
        
        return value
    
    def _combine_transform(self, value: Any, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Combine transformation"""
        fields = config.get('fields', [])
        separator = config.get('separator', ' ')
        
        combined_values = []
        for field_path in fields:
            field_value = self._get_context_value(context, field_path)
            if field_value:
                combined_values.append(str(field_value))
        
        return separator.join(combined_values)
    
    def _format_date(self, value: Any, pattern: str, config: Dict[str, Any]) -> str:
        """Format date value"""
        try:
            input_format = config.get('input_format', '%Y%m%d')
            output_format = config.get('output_format', '%Y-%m-%d')
            
            if isinstance(value, str) and value:
                # Parse input date
                if len(value) == 8 and value.isdigit():  # YYYYMMDD
                    date_obj = datetime.strptime(value, '%Y%m%d')
                elif len(value) == 6 and value.isdigit():  # YYMMDD
                    date_obj = datetime.strptime(value, '%y%m%d')
                else:
                    date_obj = datetime.strptime(value, input_format)
                
                return date_obj.strftime(output_format)
            
            return str(value)
            
        except Exception as e:
            self.logger.error(f"Error formatting date {value}: {e}")
            return str(value)
    
    def _format_number(self, value: Any, pattern: str, config: Dict[str, Any]) -> str:
        """Format number value"""
        try:
            decimal_places = config.get('decimal_places', 2)
            thousands_separator = config.get('thousands_separator', '')
            
            if self._is_numeric(value):
                num_value = float(value)
                formatted = f"{num_value:.{decimal_places}f}"
                
                if thousands_separator:
                    # Add thousands separator
                    parts = formatted.split('.')
                    parts[0] = f"{int(parts[0]):,}".replace(',', thousands_separator)
                    formatted = '.'.join(parts)
                
                return formatted
            
            return str(value)
            
        except Exception as e:
            self.logger.error(f"Error formatting number {value}: {e}")
            return str(value)
    
    def _format_string(self, value: Any, pattern: str, config: Dict[str, Any]) -> str:
        """Format string value"""
        try:
            case_transform = config.get('case', 'none')
            max_length = config.get('max_length', 0)
            padding = config.get('padding', '')
            
            str_value = str(value)
            
            # Apply case transformation
            if case_transform == 'upper':
                str_value = str_value.upper()
            elif case_transform == 'lower':
                str_value = str_value.lower()
            elif case_transform == 'title':
                str_value = str_value.title()
            
            # Apply length limit
            if max_length > 0:
                str_value = str_value[:max_length]
            
            # Apply padding
            if padding:
                pad_length = config.get('pad_length', 10)
                pad_direction = config.get('pad_direction', 'left')
                
                if pad_direction == 'left':
                    str_value = str_value.rjust(pad_length, padding)
                else:
                    str_value = str_value.ljust(pad_length, padding)
            
            return str_value
            
        except Exception as e:
            self.logger.error(f"Error formatting string {value}: {e}")
            return str(value)
    
    def _evaluate_condition(self, value: Any, condition_expr: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple condition expression"""
        try:
            # Simple condition evaluation
            # Format: "value operator expected_value"
            # e.g., "== 'test'", "> 100", "in ['A', 'B']"
            
            if condition_expr.startswith('=='):
                expected = condition_expr[2:].strip().strip("'\"")
                return str(value) == expected
            elif condition_expr.startswith('!='):
                expected = condition_expr[2:].strip().strip("'\"")
                return str(value) != expected
            elif condition_expr.startswith('>='):
                expected = float(condition_expr[2:].strip())
                return float(value) >= expected
            elif condition_expr.startswith('<='):
                expected = float(condition_expr[2:].strip())
                return float(value) <= expected
            elif condition_expr.startswith('>'):
                expected = float(condition_expr[1:].strip())
                return float(value) > expected
            elif condition_expr.startswith('<'):
                expected = float(condition_expr[1:].strip())
                return float(value) < expected
            elif condition_expr.startswith('in'):
                # Simple list membership check
                return str(value) in condition_expr
            
            return False
            
        except Exception:
            return False
    
    def _get_context_value(self, context: Dict[str, Any], path: str) -> Any:
        """Get value from context using dot notation path"""
        try:
            keys = path.split('.')
            value = context
            
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return None
                
                if value is None:
                    return None
            
            return value
            
        except Exception:
            return None
    
    def _is_numeric(self, value: Any) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class FieldMapper:
    """Maps fields from source to target structure"""
    
    def __init__(self, transformer: DataTransformer = None):
        self.transformer = transformer or DataTransformer()
        self.logger = logging.getLogger(f"{__name__}.FieldMapper")
    
    def map_fields(self, source_data: Dict[str, Any], mappings: List[FieldMapping]) -> Dict[str, Any]:
        """Map fields according to mapping configuration"""
        try:
            target_data = {}
            
            for mapping in mappings:
                source_value = self._get_source_value(source_data, mapping.source_path)
                
                # Apply default value if source is empty and default is specified
                if (source_value is None or source_value == '') and mapping.default_value is not None:
                    source_value = mapping.default_value
                
                # Skip if required field is missing
                if mapping.required and (source_value is None or source_value == ''):
                    self.logger.warning(f"Required field missing: {mapping.source_path}")
                    continue
                
                # Apply transformation
                if source_value is not None:
                    transformed_value = self.transformer.transform_value(
                        source_value,
                        mapping.transformation_type,
                        mapping.transformation_config,
                        source_data
                    )
                    
                    # Set target value
                    self._set_target_value(target_data, mapping.target_path, transformed_value)
                    
                    self.logger.debug(f"Mapped {mapping.source_path} -> {mapping.target_path}")
            
            return target_data
            
        except Exception as e:
            self.logger.error(f"Error mapping fields: {e}")
            return {}
    
    def _get_source_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get value from source data using dot notation path"""
        try:
            keys = path.split('.')
            value = data
            
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                elif isinstance(value, list) and key.isdigit():
                    index = int(key)
                    value = value[index] if 0 <= index < len(value) else None
                else:
                    return None
                
                if value is None:
                    return None
            
            return value
            
        except Exception:
            return None
    
    def _set_target_value(self, data: Dict[str, Any], path: str, value: Any):
        """Set value in target data using dot notation path"""
        keys = path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def validate_mappings(self, mappings: List[FieldMapping]) -> Dict[str, Any]:
        """Validate mapping configuration"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        for mapping in mappings:
            # Check for required fields
            if not mapping.source_path:
                validation_result['errors'].append(f"Missing source path in mapping: {mapping.description}")
                validation_result['is_valid'] = False
            
            if not mapping.target_path:
                validation_result['errors'].append(f"Missing target path in mapping: {mapping.description}")
                validation_result['is_valid'] = False
            
            # Check transformation configuration
            if mapping.transformation_type != TransformationType.COPY:
                if not mapping.transformation_config:
                    validation_result['warnings'].append(
                        f"No transformation config for {mapping.transformation_type} in {mapping.description}"
                    )
        
        return validation_result


class MappingEngine:
    """Main mapping engine that coordinates field mapping and transformations"""
    
    def __init__(self):
        self.transformer = DataTransformer()
        self.field_mapper = FieldMapper(self.transformer)
        self.configurations: Dict[str, MappingConfiguration] = {}
        self.logger = logging.getLogger(f"{__name__}.MappingEngine")
    
    def add_configuration(self, config: MappingConfiguration):
        """Add a mapping configuration"""
        config_key = self._get_config_key(config.document_type, config.customer_gln)
        self.configurations[config_key] = config
        self.logger.info(f"Added mapping configuration: {config_key}")
    
    def remove_configuration(self, document_type: str, customer_gln: Optional[str] = None):
        """Remove a mapping configuration"""
        config_key = self._get_config_key(document_type, customer_gln)
        if config_key in self.configurations:
            del self.configurations[config_key]
            self.logger.info(f"Removed mapping configuration: {config_key}")
    
    def get_configuration(self, document_type: str, customer_gln: Optional[str] = None) -> Optional[MappingConfiguration]:
        """Get mapping configuration for document type and customer"""
        # Try specific customer configuration first
        if customer_gln:
            config_key = self._get_config_key(document_type, customer_gln)
            if config_key in self.configurations:
                return self.configurations[config_key]
        
        # Fall back to general document type configuration
        config_key = self._get_config_key(document_type, None)
        return self.configurations.get(config_key)
    
    def apply_mapping(self, source_data: Dict[str, Any], document_type: str, 
                     customer_gln: Optional[str] = None) -> Dict[str, Any]:
        """Apply mapping to source data"""
        try:
            config = self.get_configuration(document_type, customer_gln)
            if not config:
                self.logger.warning(f"No mapping configuration found for {document_type}/{customer_gln}")
                return source_data
            
            # Apply field mappings
            mapped_data = self.field_mapper.map_fields(source_data, config.field_mappings)
            
            # Apply global transformations
            if config.global_transformations:
                mapped_data = self._apply_global_transformations(mapped_data, config.global_transformations)
            
            # Add metadata
            if config.metadata:
                mapped_data['_metadata'] = config.metadata
            
            self.logger.info(f"Applied mapping for {document_type}/{customer_gln}")
            return mapped_data
            
        except Exception as e:
            self.logger.error(f"Error applying mapping: {e}")
            return source_data
    
    def _get_config_key(self, document_type: str, customer_gln: Optional[str]) -> str:
        """Generate configuration key"""
        return f"{document_type}:{customer_gln or 'default'}"
    
    def _apply_global_transformations(self, data: Dict[str, Any], transformations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply global transformations to the mapped data"""
        # Implementation for global transformations
        # This could include things like adding calculated totals, formatting, etc.
        return data
    
    def validate_configuration(self, config: MappingConfiguration) -> Dict[str, Any]:
        """Validate a mapping configuration"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate basic configuration
        if not config.document_type:
            validation_result['errors'].append("Document type is required")
            validation_result['is_valid'] = False
        
        # Validate field mappings
        if config.field_mappings:
            mapping_validation = self.field_mapper.validate_mappings(config.field_mappings)
            validation_result['errors'].extend(mapping_validation['errors'])
            validation_result['warnings'].extend(mapping_validation['warnings'])
            if not mapping_validation['is_valid']:
                validation_result['is_valid'] = False
        
        return validation_result
    
    def get_available_configurations(self) -> List[str]:
        """Get list of available configuration keys"""
        return list(self.configurations.keys())
    
    def export_configuration(self, document_type: str, customer_gln: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Export configuration as dictionary"""
        config = self.get_configuration(document_type, customer_gln)
        if config:
            return {
                'document_type': config.document_type,
                'customer_gln': config.customer_gln,
                'target_structure': config.target_structure,
                'field_mappings': [
                    {
                        'source_path': mapping.source_path,
                        'target_path': mapping.target_path,
                        'transformation_type': mapping.transformation_type.value,
                        'transformation_config': mapping.transformation_config,
                        'required': mapping.required,
                        'default_value': mapping.default_value,
                        'description': mapping.description
                    }
                    for mapping in config.field_mappings
                ],
                'global_transformations': config.global_transformations,
                'metadata': config.metadata
            }
        return None


# Convenience functions for creating common mappings
def create_simple_mapping(source_path: str, target_path: str, required: bool = False, 
                         default_value: Any = None) -> FieldMapping:
    """Create a simple copy mapping"""
    return FieldMapping(
        source_path=source_path,
        target_path=target_path,
        transformation_type=TransformationType.COPY,
        required=required,
        default_value=default_value
    )


def create_format_mapping(source_path: str, target_path: str, format_type: str, 
                         format_config: Dict[str, Any]) -> FieldMapping:
    """Create a format transformation mapping"""
    return FieldMapping(
        source_path=source_path,
        target_path=target_path,
        transformation_type=TransformationType.FORMAT,
        transformation_config={
            'format_type': format_type,
            **format_config
        }
    )


def create_lookup_mapping(source_path: str, target_path: str, 
                         lookup_table: Dict[str, Any]) -> FieldMapping:
    """Create a lookup transformation mapping"""
    return FieldMapping(
        source_path=source_path,
        target_path=target_path,
        transformation_type=TransformationType.LOOKUP,
        transformation_config={
            'lookup_table': lookup_table
        }
    )

