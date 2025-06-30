#!/usr/bin/env python3
"""
EDIFACT Validators Module
========================

This module provides comprehensive validation for EDIFACT messages,
including syntax validation, structure validation, and business rule validation.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime
from .edifact_syntax import EDIFACTSyntax, validate_segment_tag, validate_numeric, validate_alphanumeric
from .edifact_segments import EDIFACTSegments, SegmentDefinition, ElementDefinition, ComponentDefinition
from .edifact_elements import EDIFACTElements, DataElementDefinition, DataElementType, DataElementStatus
from .edifact_qualifiers import EDIFACTQualifiers
from .edifact_constants import ValidationLevel, ERROR_CODES, WARNING_CODES


class ValidationSeverity(Enum):
    """Validation message severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


@dataclass
class ValidationMessage:
    """Validation message structure"""
    severity: ValidationSeverity
    code: str
    message: str
    segment_tag: Optional[str] = None
    segment_position: Optional[int] = None
    element_position: Optional[int] = None
    component_position: Optional[int] = None
    value: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of validation message"""
        location = ""
        if self.segment_tag:
            location = f"[{self.segment_tag}"
            if self.segment_position is not None:
                location += f"#{self.segment_position}"
            if self.element_position is not None:
                location += f".{self.element_position}"
            if self.component_position is not None:
                location += f".{self.component_position}"
            location += "] "
        
        return f"{self.severity.value.upper()}: {location}{self.message} ({self.code})"


@dataclass
class ValidationResult:
    """Validation result structure"""
    is_valid: bool
    messages: List[ValidationMessage]
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    
    def add_message(self, message: ValidationMessage):
        """Add a validation message"""
        self.messages.append(message)
        if message.severity == ValidationSeverity.ERROR or message.severity == ValidationSeverity.FATAL:
            self.error_count += 1
            self.is_valid = False
        elif message.severity == ValidationSeverity.WARNING:
            self.warning_count += 1
        elif message.severity == ValidationSeverity.INFO:
            self.info_count += 1
    
    def get_summary(self) -> str:
        """Get validation summary"""
        status = "VALID" if self.is_valid else "INVALID"
        return f"Validation {status}: {self.error_count} errors, {self.warning_count} warnings, {self.info_count} info"


class EDIFACTValidator:
    """
    Comprehensive EDIFACT message validator.
    
    Provides multiple levels of validation from basic syntax checking
    to full business rule validation.
    """
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        """
        Initialize validator.
        
        Args:
            validation_level: Level of validation to perform
        """
        self.validation_level = validation_level
        self.syntax = EDIFACTSyntax()
        
    def validate_message(self, content: str) -> ValidationResult:
        """
        Validate complete EDIFACT message.
        
        Args:
            content: Raw EDIFACT message content
            
        Returns:
            ValidationResult with all validation messages
        """
        result = ValidationResult(is_valid=True, messages=[])
        
        if not content or not content.strip():
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.FATAL,
                code="E013",
                message="Empty message content"
            ))
            return result
        
        # Parse UNA segment if present
        if content.startswith("UNA"):
            try:
                self.syntax = EDIFACTSyntax.from_una_segment(content[:9])
            except ValueError as e:
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E011",
                    message=f"Invalid UNA segment: {e}"
                ))
        
        # Split into segments
        segments = self.syntax.split_segments(content)
        
        if not segments:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.FATAL,
                code="E013",
                message="No segments found in message"
            ))
            return result
        
        # Validate message structure
        self._validate_message_structure(segments, result)
        
        # Validate individual segments
        for i, segment in enumerate(segments):
            self._validate_segment(segment, i + 1, result)
        
        return result
    
    def _validate_message_structure(self, segments: List[str], result: ValidationResult):
        """Validate overall message structure"""
        if not segments:
            return
        
        segment_tags = []
        for segment in segments:
            elements = self.syntax.split_elements(segment)
            if elements:
                segment_tags.append(elements[0])
        
        # Check for mandatory segments
        mandatory_segments = {"UNB", "UNH", "UNT", "UNZ"}
        found_segments = set(segment_tags)
        
        for mandatory in mandatory_segments:
            if mandatory not in found_segments:
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E002",
                    message=f"Missing mandatory segment: {mandatory}"
                ))
        
        # Check segment order
        self._validate_segment_order(segment_tags, result)
        
        # Check segment occurrence limits
        self._validate_segment_occurrences(segment_tags, result)
    
    def _validate_segment_order(self, segment_tags: List[str], result: ValidationResult):
        """Validate segment order according to EDIFACT rules"""
        expected_order = {
            "UNA": 0,
            "UNB": 1,
            "UNH": 2,
            "BGM": 3,
            "DTM": 4,
            "RFF": 5,
            "NAD": 6,
            "LIN": 100,  # Detail segments
            "UNS": 200,  # Summary separator
            "CNT": 201,  # Summary segments
            "UNT": 998,
            "UNZ": 999
        }
        
        last_order = -1
        for i, tag in enumerate(segment_tags):
            if tag in expected_order:
                current_order = expected_order[tag]
                if current_order < last_order and tag not in ["DTM", "RFF", "NAD", "LIN"]:
                    result.add_message(ValidationMessage(
                        severity=ValidationSeverity.WARNING,
                        code="W004",
                        message=f"Segment {tag} appears out of expected order",
                        segment_tag=tag,
                        segment_position=i + 1
                    ))
                last_order = max(last_order, current_order)
    
    def _validate_segment_occurrences(self, segment_tags: List[str], result: ValidationResult):
        """Validate segment occurrence limits"""
        segment_counts = {}
        for tag in segment_tags:
            segment_counts[tag] = segment_counts.get(tag, 0) + 1
        
        # Check occurrence limits
        occurrence_limits = {
            "UNA": 1,
            "UNB": 1,
            "UNH": 1,
            "BGM": 1,
            "UNT": 1,
            "UNZ": 1,
            "UNS": 1,
            "DTM": 99,
            "RFF": 99,
            "NAD": 99,
            "LIN": 9999
        }
        
        for tag, count in segment_counts.items():
            if tag in occurrence_limits:
                limit = occurrence_limits[tag]
                if count > limit:
                    result.add_message(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        code="E012",
                        message=f"Segment {tag} occurs {count} times, maximum allowed is {limit}",
                        segment_tag=tag
                    ))
    
    def _validate_segment(self, segment: str, position: int, result: ValidationResult):
        """Validate individual segment"""
        if not segment.strip():
            return
        
        elements = self.syntax.split_elements(segment)
        if not elements:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E001",
                message="Empty segment",
                segment_position=position
            ))
            return
        
        segment_tag = elements[0]
        
        # Validate segment tag format
        if not validate_segment_tag(segment_tag):
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E001",
                message=f"Invalid segment tag format: {segment_tag}",
                segment_tag=segment_tag,
                segment_position=position
            ))
            return
        
        # Get segment definition
        segment_def = EDIFACTSegments.get_segment(segment_tag)
        if not segment_def and self.validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT]:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.WARNING,
                code="W001",
                message=f"Unknown segment: {segment_tag}",
                segment_tag=segment_tag,
                segment_position=position
            ))
            return
        
        if segment_def:
            self._validate_segment_elements(segment_tag, elements[1:], segment_def, position, result)
    
    def _validate_segment_elements(self, segment_tag: str, elements: List[str], 
                                 segment_def: SegmentDefinition, position: int, 
                                 result: ValidationResult):
        """Validate segment elements against definition"""
        
        # Check mandatory elements
        for i, element_def in enumerate(segment_def.elements):
            if element_def.status == DataElementStatus.MANDATORY:
                if i >= len(elements) or not elements[i].strip():
                    result.add_message(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        code="E004",
                        message=f"Missing mandatory element {element_def.position}",
                        segment_tag=segment_tag,
                        segment_position=position,
                        element_position=element_def.position
                    ))
        
        # Validate each element
        for i, element_value in enumerate(elements):
            if i < len(segment_def.elements):
                element_def = segment_def.elements[i]
                self._validate_element(segment_tag, element_value, element_def, position, i + 1, result)
    
    def _validate_element(self, segment_tag: str, element_value: str, 
                         element_def: ElementDefinition, segment_position: int, 
                         element_position: int, result: ValidationResult):
        """Validate individual element"""
        
        if not element_value.strip():
            if element_def.status == DataElementStatus.MANDATORY:
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E004",
                    message=f"Empty mandatory element",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position
                ))
            return
        
        # Validate element length
        if len(element_value) < element_def.min_length:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E010",
                message=f"Element value too short: {len(element_value)} < {element_def.min_length}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                value=element_value
            ))
        
        if len(element_value) > element_def.max_length:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E009",
                message=f"Element value too long: {len(element_value)} > {element_def.max_length}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                value=element_value
            ))
        
        # Validate composite elements
        if element_def.is_composite:
            components = self.syntax.split_components(element_value)
            self._validate_composite_element(segment_tag, components, element_def, 
                                           segment_position, element_position, result)
        else:
            # Validate simple element
            self._validate_simple_element(segment_tag, element_value, element_def,
                                        segment_position, element_position, result)
    
    def _validate_composite_element(self, segment_tag: str, components: List[str],
                                  element_def: ElementDefinition, segment_position: int,
                                  element_position: int, result: ValidationResult):
        """Validate composite element components"""
        
        for i, component_def in enumerate(element_def.components):
            if i < len(components):
                component_value = components[i]
                self._validate_component(segment_tag, component_value, component_def,
                                       segment_position, element_position, i + 1, result)
            elif component_def.status == DataElementStatus.MANDATORY:
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E004",
                    message=f"Missing mandatory component {i + 1}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=i + 1
                ))
    
    def _validate_component(self, segment_tag: str, component_value: str,
                          component_def: ComponentDefinition, segment_position: int,
                          element_position: int, component_position: int,
                          result: ValidationResult):
        """Validate individual component"""
        
        if not component_value.strip():
            if component_def.status == DataElementStatus.MANDATORY:
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E004",
                    message=f"Empty mandatory component",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=component_position
                ))
            return
        
        # Validate component length
        if len(component_value) < component_def.min_length:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E010",
                message=f"Component value too short: {len(component_value)} < {component_def.min_length}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                component_position=component_position,
                value=component_value
            ))
        
        if len(component_value) > component_def.max_length:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E009",
                message=f"Component value too long: {len(component_value)} > {component_def.max_length}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                component_position=component_position,
                value=component_value
            ))
        
        # Validate data type
        self._validate_data_type(component_value, component_def.data_type, segment_tag,
                               segment_position, element_position, component_position, result)
        
        # Validate code list
        if component_def.code_list and component_value not in component_def.code_list:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E005",
                message=f"Invalid code value: {component_value}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                component_position=component_position,
                value=component_value
            ))
        
        # Validate format pattern
        if component_def.format_pattern:
            if not re.match(component_def.format_pattern, component_value):
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E003",
                    message=f"Invalid format: {component_value}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=component_position,
                    value=component_value
                ))
    
    def _validate_simple_element(self, segment_tag: str, element_value: str,
                               element_def: ElementDefinition, segment_position: int,
                               element_position: int, result: ValidationResult):
        """Validate simple (non-composite) element"""
        
        # Validate data type
        self._validate_data_type(element_value, element_def.data_type, segment_tag,
                               segment_position, element_position, None, result)
        
        # Validate code list
        if element_def.code_list and element_value not in element_def.code_list:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E005",
                message=f"Invalid code value: {element_value}",
                segment_tag=segment_tag,
                segment_position=segment_position,
                element_position=element_position,
                value=element_value
            ))
        
        # Validate format pattern
        if element_def.format_pattern:
            if not re.match(element_def.format_pattern, element_value):
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E003",
                    message=f"Invalid format: {element_value}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    value=element_value
                ))
    
    def _validate_data_type(self, value: str, data_type: DataElementType,
                          segment_tag: str, segment_position: int,
                          element_position: int, component_position: Optional[int],
                          result: ValidationResult):
        """Validate data type constraints"""
        
        if data_type == DataElementType.NUMERIC:
            if not validate_numeric(value):
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E008",
                    message=f"Invalid numeric value: {value}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=component_position,
                    value=value
                ))
        
        elif data_type == DataElementType.ALPHABETIC:
            if not value.isalpha():
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    code="E003",
                    message=f"Invalid alphabetic value: {value}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=component_position,
                    value=value
                ))
        
        elif data_type == DataElementType.ALPHANUMERIC:
            if not validate_alphanumeric(value):
                result.add_message(ValidationMessage(
                    severity=ValidationSeverity.WARNING,
                    code="W005",
                    message=f"Non-alphanumeric characters in value: {value}",
                    segment_tag=segment_tag,
                    segment_position=segment_position,
                    element_position=element_position,
                    component_position=component_position,
                    value=value
                ))
    
    def validate_business_rules(self, segments: List[str]) -> ValidationResult:
        """
        Validate business rules for EDIFACT message.
        
        Args:
            segments: List of segment strings
            
        Returns:
            ValidationResult with business rule validation messages
        """
        result = ValidationResult(is_valid=True, messages=[])
        
        # Extract segment data for business rule validation
        segment_data = {}
        for segment in segments:
            elements = self.syntax.split_elements(segment)
            if elements:
                tag = elements[0]
                if tag not in segment_data:
                    segment_data[tag] = []
                segment_data[tag].append(elements[1:])
        
        # Validate UNH/UNT message reference consistency
        self._validate_message_references(segment_data, result)
        
        # Validate UNB/UNZ interchange reference consistency
        self._validate_interchange_references(segment_data, result)
        
        # Validate date/time consistency
        self._validate_date_consistency(segment_data, result)
        
        # Validate party relationships
        self._validate_party_relationships(segment_data, result)
        
        return result
    
    def _validate_message_references(self, segment_data: Dict[str, List[List[str]]], 
                                   result: ValidationResult):
        """Validate UNH/UNT message reference consistency"""
        unh_refs = []
        unt_refs = []
        
        if "UNH" in segment_data:
            for elements in segment_data["UNH"]:
                if elements:
                    unh_refs.append(elements[0])  # Message reference number
        
        if "UNT" in segment_data:
            for elements in segment_data["UNT"]:
                if len(elements) > 1:
                    unt_refs.append(elements[1])  # Message reference number
        
        if unh_refs != unt_refs:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E013",
                message="UNH/UNT message reference mismatch"
            ))
    
    def _validate_interchange_references(self, segment_data: Dict[str, List[List[str]]], 
                                       result: ValidationResult):
        """Validate UNB/UNZ interchange reference consistency"""
        unb_refs = []
        unz_refs = []
        
        if "UNB" in segment_data:
            for elements in segment_data["UNB"]:
                if len(elements) > 4:
                    unb_refs.append(elements[4])  # Interchange control reference
        
        if "UNZ" in segment_data:
            for elements in segment_data["UNZ"]:
                if len(elements) > 1:
                    unz_refs.append(elements[1])  # Interchange control reference
        
        if unb_refs != unz_refs:
            result.add_message(ValidationMessage(
                severity=ValidationSeverity.ERROR,
                code="E013",
                message="UNB/UNZ interchange reference mismatch"
            ))
    
    def _validate_date_consistency(self, segment_data: Dict[str, List[List[str]]], 
                                 result: ValidationResult):
        """Validate date/time consistency"""
        # This is a placeholder for date consistency validation
        # Could include checks like:
        # - Delivery date after order date
        # - Invoice date not in future
        # - Expiry date after production date
        pass
    
    def _validate_party_relationships(self, segment_data: Dict[str, List[List[str]]], 
                                    result: ValidationResult):
        """Validate party relationship consistency"""
        # This is a placeholder for party relationship validation
        # Could include checks like:
        # - Buyer and supplier are different parties
        # - Invoice party matches order party
        # - Delivery party is specified for delivery orders
        pass


def validate_edifact_message(content: str, 
                           validation_level: ValidationLevel = ValidationLevel.STANDARD) -> ValidationResult:
    """
    Convenience function to validate EDIFACT message.
    
    Args:
        content: Raw EDIFACT message content
        validation_level: Level of validation to perform
        
    Returns:
        ValidationResult with all validation messages
    """
    validator = EDIFACTValidator(validation_level)
    return validator.validate_message(content)

