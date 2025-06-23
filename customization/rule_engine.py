#!/usr/bin/env python3
"""
Rule Engine for EDI Customization Layer
=======================================

This module provides rule-based filtering and processing for EDI data
based on document types, customer GLNs, and business rules.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional, Callable, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class FilterResult(Enum):
    """Filter result enumeration"""
    INCLUDE = "include"
    EXCLUDE = "exclude"
    TRANSFORM = "transform"


@dataclass
class FilterRule:
    """Represents a single filter rule"""
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    action: FilterResult
    priority: int = 0
    description: str = ""
    
    def __post_init__(self):
        if not self.description:
            self.description = f"Filter rule: {self.name}"


@dataclass
class DocumentTypeRule:
    """Document type specific rule"""
    document_code: str  # e.g., "850", "810"
    document_name: str  # e.g., "PurchaseOrder", "Invoice"
    required_segments: List[str]
    optional_segments: List[str]
    business_rules: List[FilterRule]
    gln_specific_rules: Dict[str, List[FilterRule]]  # GLN -> rules


class BaseFilter(ABC):
    """Abstract base class for filters"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply filter to data"""
        pass
    
    @abstractmethod
    def matches(self, data: Dict[str, Any]) -> bool:
        """Check if filter matches the data"""
        pass


class DocumentTypeFilter(BaseFilter):
    """Filter based on document type"""
    
    def __init__(self, document_mappings: Dict[str, str] = None):
        super().__init__("DocumentTypeFilter")
        
        # Default document type mappings
        self.document_mappings = document_mappings or {
            "ORDERS": "850",
            "INVOIC": "810", 
            "DESADV": "856",
            "ORDRSP": "855",
            "REMADV": "820",
            "PRICAT": "832"
        }
        
        # Reverse mapping for lookup
        self.code_to_name = {v: k for k, v in self.document_mappings.items()}
    
    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply document type filtering"""
        try:
            # Extract document type information
            message_info = data.get('message_info', {})
            document_type = message_info.get('type', '')
            
            # Add document code if not present
            if document_type and document_type in self.document_mappings:
                data['document_code'] = self.document_mappings[document_type]
                data['document_name'] = document_type
            
            # Filter segments based on document type
            if document_type:
                data = self._filter_segments_by_document_type(data, document_type)
            
            self.logger.debug(f"Applied document type filter for {document_type}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error applying document type filter: {e}")
            return data
    
    def matches(self, data: Dict[str, Any]) -> bool:
        """Check if data matches document type criteria"""
        message_info = data.get('message_info', {})
        document_type = message_info.get('type', '')
        return document_type in self.document_mappings
    
    def _filter_segments_by_document_type(self, data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """Filter segments based on document type requirements"""
        segments = data.get('segments', [])
        
        # Define required segments by document type
        required_segments = {
            'ORDERS': ['UNB', 'UNH', 'BGM', 'DTM', 'NAD', 'LIN', 'UNT', 'UNZ'],
            'INVOIC': ['UNB', 'UNH', 'BGM', 'DTM', 'NAD', 'LIN', 'MOA', 'UNT', 'UNZ'],
            'DESADV': ['UNB', 'UNH', 'BGM', 'DTM', 'NAD', 'LIN', 'QTY', 'UNT', 'UNZ']
        }
        
        if document_type in required_segments:
            required_tags = set(required_segments[document_type])
            filtered_segments = [
                seg for seg in segments 
                if seg.get('tag', '') in required_tags or seg.get('tag', '').startswith('UNS')
            ]
            data['segments'] = filtered_segments
        
        return data
    
    def get_document_code(self, document_type: str) -> Optional[str]:
        """Get document code for a document type"""
        return self.document_mappings.get(document_type)
    
    def get_document_name(self, document_code: str) -> Optional[str]:
        """Get document name for a document code"""
        return self.code_to_name.get(document_code)


class CustomerGLNFilter(BaseFilter):
    """Filter based on customer GLN (Global Location Number)"""
    
    def __init__(self, gln_mappings: Dict[str, Dict[str, Any]] = None):
        super().__init__("CustomerGLNFilter")
        
        # GLN to customer configuration mappings
        self.gln_mappings = gln_mappings or {}
    
    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customer GLN filtering"""
        try:
            # Extract GLN information from parties
            parties = data.get('business_data', {}).get('parties', {})
            customer_gln = self._extract_customer_gln(parties)
            
            if customer_gln:
                data['customer_gln'] = customer_gln
                
                # Apply customer-specific rules
                if customer_gln in self.gln_mappings:
                    customer_config = self.gln_mappings[customer_gln]
                    data = self._apply_customer_rules(data, customer_config)
            
            self.logger.debug(f"Applied GLN filter for customer {customer_gln}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error applying GLN filter: {e}")
            return data
    
    def matches(self, data: Dict[str, Any]) -> bool:
        """Check if data matches GLN criteria"""
        parties = data.get('business_data', {}).get('parties', {})
        customer_gln = self._extract_customer_gln(parties)
        return customer_gln in self.gln_mappings if customer_gln else False
    
    def _extract_customer_gln(self, parties: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """Extract customer GLN from parties data"""
        # Look for buyer or customer party
        for qualifier in ['BY', 'BT', 'SU', 'IV']:  # Common customer qualifiers
            if qualifier in parties:
                party = parties[qualifier]
                gln = party.get('id', '')
                if gln and len(gln) == 13 and gln.isdigit():  # GLN format validation
                    return gln
        
        return None
    
    def _apply_customer_rules(self, data: Dict[str, Any], customer_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customer-specific rules"""
        # Apply field filtering rules
        if 'field_filters' in customer_config:
            data = self._apply_field_filters(data, customer_config['field_filters'])
        
        # Apply segment filtering rules
        if 'segment_filters' in customer_config:
            data = self._apply_segment_filters(data, customer_config['segment_filters'])
        
        # Apply transformation rules
        if 'transformations' in customer_config:
            data = self._apply_transformations(data, customer_config['transformations'])
        
        return data
    
    def _apply_field_filters(self, data: Dict[str, Any], field_filters: Dict[str, Any]) -> Dict[str, Any]:
        """Apply field-level filtering"""
        # Implementation for field filtering
        return data
    
    def _apply_segment_filters(self, data: Dict[str, Any], segment_filters: Dict[str, Any]) -> Dict[str, Any]:
        """Apply segment-level filtering"""
        # Implementation for segment filtering
        return data
    
    def _apply_transformations(self, data: Dict[str, Any], transformations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply data transformations"""
        # Implementation for data transformations
        return data
    
    def add_gln_mapping(self, gln: str, config: Dict[str, Any]):
        """Add GLN mapping configuration"""
        self.gln_mappings[gln] = config
    
    def remove_gln_mapping(self, gln: str):
        """Remove GLN mapping configuration"""
        if gln in self.gln_mappings:
            del self.gln_mappings[gln]


class FieldExtractor(BaseFilter):
    """Extract specific fields based on rules"""
    
    def __init__(self, extraction_rules: Dict[str, List[str]] = None):
        super().__init__("FieldExtractor")
        
        # Field extraction rules by document type
        self.extraction_rules = extraction_rules or {
            'ORDERS': [
                'message_info.reference',
                'business_data.parties.BY',
                'business_data.parties.SU',
                'business_data.line_items',
                'business_data.dates.137',  # Order date
                'business_data.totals.79'   # Total amount
            ],
            'INVOIC': [
                'message_info.reference',
                'business_data.parties.SU',
                'business_data.parties.BY',
                'business_data.line_items',
                'business_data.dates.137',  # Invoice date
                'business_data.dates.35',   # Payment date
                'business_data.totals.128'  # Total payable
            ]
        }
    
    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply field extraction"""
        try:
            document_type = data.get('document_name', '')
            
            if document_type in self.extraction_rules:
                extracted_data = {}
                rules = self.extraction_rules[document_type]
                
                for rule in rules:
                    value = self._extract_field_value(data, rule)
                    if value is not None:
                        self._set_nested_value(extracted_data, rule, value)
                
                data['extracted_fields'] = extracted_data
            
            self.logger.debug(f"Applied field extraction for {document_type}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error applying field extraction: {e}")
            return data
    
    def matches(self, data: Dict[str, Any]) -> bool:
        """Check if data matches extraction criteria"""
        document_type = data.get('document_name', '')
        return document_type in self.extraction_rules
    
    def _extract_field_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Extract field value using dot notation path"""
        try:
            keys = field_path.split('.')
            value = data
            
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
    
    def _set_nested_value(self, data: Dict[str, Any], field_path: str, value: Any):
        """Set nested value using dot notation path"""
        keys = field_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def add_extraction_rule(self, document_type: str, field_paths: List[str]):
        """Add extraction rules for a document type"""
        if document_type not in self.extraction_rules:
            self.extraction_rules[document_type] = []
        
        self.extraction_rules[document_type].extend(field_paths)
    
    def remove_extraction_rule(self, document_type: str, field_path: str):
        """Remove extraction rule"""
        if document_type in self.extraction_rules:
            if field_path in self.extraction_rules[document_type]:
                self.extraction_rules[document_type].remove(field_path)


class RuleEngine:
    """Main rule engine for coordinating filters"""
    
    def __init__(self):
        self.filters: List[BaseFilter] = []
        self.rules: List[FilterRule] = []
        self.logger = logging.getLogger(f"{__name__}.RuleEngine")
    
    def add_filter(self, filter_instance: BaseFilter):
        """Add a filter to the engine"""
        self.filters.append(filter_instance)
        self.logger.info(f"Added filter: {filter_instance.name}")
    
    def remove_filter(self, filter_name: str):
        """Remove a filter from the engine"""
        self.filters = [f for f in self.filters if f.name != filter_name]
        self.logger.info(f"Removed filter: {filter_name}")
    
    def add_rule(self, rule: FilterRule):
        """Add a rule to the engine"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        self.logger.info(f"Added rule: {rule.name}")
    
    def apply_all_filters(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all filters to the data"""
        try:
            result_data = data.copy()
            
            # Apply filters in order
            for filter_instance in self.filters:
                if filter_instance.matches(result_data):
                    result_data = filter_instance.apply(result_data)
                    self.logger.debug(f"Applied filter: {filter_instance.name}")
            
            # Apply custom rules
            result_data = self._apply_custom_rules(result_data)
            
            return result_data
            
        except Exception as e:
            self.logger.error(f"Error applying filters: {e}")
            return data
    
    def _apply_custom_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply custom filter rules"""
        for rule in self.rules:
            try:
                if rule.condition(data):
                    if rule.action == FilterResult.EXCLUDE:
                        return {}  # Exclude data
                    elif rule.action == FilterResult.TRANSFORM:
                        # Apply transformation logic here
                        pass
                    # INCLUDE action doesn't modify data
                    
            except Exception as e:
                self.logger.error(f"Error applying rule {rule.name}: {e}")
        
        return data
    
    def get_applicable_filters(self, data: Dict[str, Any]) -> List[BaseFilter]:
        """Get list of filters that apply to the data"""
        applicable = []
        
        for filter_instance in self.filters:
            if filter_instance.matches(data):
                applicable.append(filter_instance)
        
        return applicable
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against all rules"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'applicable_filters': []
        }
        
        try:
            # Check which filters apply
            applicable_filters = self.get_applicable_filters(data)
            validation_result['applicable_filters'] = [f.name for f in applicable_filters]
            
            # Validate against rules
            for rule in self.rules:
                try:
                    if not rule.condition(data):
                        if rule.action == FilterResult.EXCLUDE:
                            validation_result['errors'].append(f"Rule violation: {rule.name}")
                            validation_result['is_valid'] = False
                        else:
                            validation_result['warnings'].append(f"Rule warning: {rule.name}")
                except Exception as e:
                    validation_result['errors'].append(f"Rule error {rule.name}: {str(e)}")
                    validation_result['is_valid'] = False
            
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")
            validation_result['is_valid'] = False
        
        return validation_result


# Convenience functions for creating common rules
def create_document_type_rule(document_type: str, required_segments: List[str]) -> FilterRule:
    """Create a document type validation rule"""
    def condition(data: Dict[str, Any]) -> bool:
        msg_type = data.get('message_info', {}).get('type', '')
        if msg_type != document_type:
            return True  # Rule doesn't apply
        
        segments = data.get('segments', [])
        segment_tags = {seg.get('tag', '') for seg in segments}
        
        return all(tag in segment_tags for tag in required_segments)
    
    return FilterRule(
        name=f"DocumentType_{document_type}_RequiredSegments",
        condition=condition,
        action=FilterResult.EXCLUDE,
        description=f"Validate required segments for {document_type}"
    )


def create_gln_validation_rule(valid_glns: Set[str]) -> FilterRule:
    """Create a GLN validation rule"""
    def condition(data: Dict[str, Any]) -> bool:
        customer_gln = data.get('customer_gln', '')
        return customer_gln in valid_glns if customer_gln else False
    
    return FilterRule(
        name="GLN_Validation",
        condition=condition,
        action=FilterResult.EXCLUDE,
        description="Validate customer GLN"
    )


def create_field_required_rule(field_path: str, document_types: List[str] = None) -> FilterRule:
    """Create a required field validation rule"""
    def condition(data: Dict[str, Any]) -> bool:
        if document_types:
            doc_type = data.get('document_name', '')
            if doc_type not in document_types:
                return True  # Rule doesn't apply
        
        # Check if field exists and has value
        keys = field_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return False
        
        return value is not None and str(value).strip() != ''
    
    return FilterRule(
        name=f"Required_Field_{field_path}",
        condition=condition,
        action=FilterResult.EXCLUDE,
        description=f"Validate required field: {field_path}"
    )

