#!/usr/bin/env python3
"""
EDIFACT Parser Module
====================

This module provides the main EDIFACT parsing functionality,
converting EDIFACT messages into structured data objects.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import re
from .edifact_syntax import EDIFACTSyntax, EDIFACTSyntaxChars
from .edifact_segments import EDIFACTSegments, SegmentDefinition
from .edifact_elements import EDIFACTElements
from .edifact_qualifiers import EDIFACTQualifiers
from .edifact_mappings import EDIFACTMappings, MappingContext
from .edifact_validators import EDIFACTValidator, ValidationResult, ValidationLevel
from .edifact_constants import ValidationLevel, MessageType, SegmentGroup


@dataclass
class ParsedComponent:
    """Parsed component data structure"""
    position: int
    value: str
    element_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class ParsedElement:
    """Parsed element data structure"""
    position: int
    value: str
    element_id: Optional[str] = None
    name: Optional[str] = None
    is_composite: bool = False
    components: List[ParsedComponent] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class ParsedSegment:
    """Parsed segment data structure"""
    tag: str
    position: int
    elements: List[ParsedElement] = field(default_factory=list)
    semantic_name: Optional[str] = None
    group: Optional[SegmentGroup] = None
    description: Optional[str] = None
    qualifier: Optional[str] = None


@dataclass
class ParsedMessage:
    """Complete parsed EDIFACT message"""
    message_type: Optional[str] = None
    message_version: Optional[str] = None
    message_release: Optional[str] = None
    message_reference: Optional[str] = None
    interchange_reference: Optional[str] = None
    sender_id: Optional[str] = None
    recipient_id: Optional[str] = None
    syntax_identifier: Optional[str] = None
    syntax_version: Optional[str] = None
    preparation_date: Optional[str] = None
    preparation_time: Optional[str] = None
    segments: List[ParsedSegment] = field(default_factory=list)
    validation_result: Optional[ValidationResult] = None
    parsing_statistics: Dict[str, Any] = field(default_factory=dict)


class EDIFACTParser:
    """
    Main EDIFACT parser class.
    
    Provides comprehensive parsing of EDIFACT messages with validation,
    semantic mapping, and structured data extraction.
    """
    
    def __init__(self, 
                 validation_level: ValidationLevel = ValidationLevel.STANDARD,
                 generate_empty_elements: bool = True,
                 preserve_whitespace: bool = False):
        """
        Initialize EDIFACT parser.
        
        Args:
            validation_level: Level of validation to perform
            generate_empty_elements: Whether to generate empty elements for missing data
            preserve_whitespace: Whether to preserve whitespace in element values
        """
        self.validation_level = validation_level
        self.generate_empty_elements = generate_empty_elements
        self.preserve_whitespace = preserve_whitespace
        
        self.syntax = EDIFACTSyntax()
        self.validator = EDIFACTValidator(validation_level)
        
        # Statistics tracking
        self.reset_statistics()
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    def reset_statistics(self):
        """Reset parsing statistics"""
        self.statistics = {
            'total_segments': 0,
            'total_elements': 0,
            'total_components': 0,
            'processing_time': 0.0,
            'file_size': 0,
            'validation_errors': 0,
            'validation_warnings': 0,
            'segments_by_type': {},
            'elements_by_type': {},
            'parsing_errors': 0
        }
    
    def parse_message(self, content: str) -> ParsedMessage:
        """
        Parse complete EDIFACT message.
        
        Args:
            content: Raw EDIFACT message content
            
        Returns:
            ParsedMessage with structured data
        """
        start_time = datetime.now()
        self.reset_statistics()
        
        parsed_message = ParsedMessage()
        
        try:
            # Update statistics
            self.statistics['file_size'] = len(content)
            
            # Validate message if requested
            if self.validation_level != ValidationLevel.NONE:
                parsed_message.validation_result = self.validator.validate_message(content)
                self.statistics['validation_errors'] = parsed_message.validation_result.error_count
                self.statistics['validation_warnings'] = parsed_message.validation_result.warning_count
            
            # Parse UNA segment if present
            if content.startswith("UNA"):
                try:
                    self.syntax = EDIFACTSyntax.from_una_segment(content[:9])
                    self.logger.debug(f"Parsed UNA segment: {self.syntax}")
                except ValueError as e:
                    self.logger.warning(f"Invalid UNA segment: {e}")
                    self.statistics['parsing_errors'] += 1
            
            # Split into segments
            segments = self.syntax.split_segments(content)
            self.statistics['total_segments'] = len(segments)
            
            # Parse each segment
            for i, segment_content in enumerate(segments):
                try:
                    parsed_segment = self._parse_segment(segment_content, i + 1)
                    if parsed_segment:
                        parsed_message.segments.append(parsed_segment)
                        
                        # Update segment statistics
                        tag = parsed_segment.tag
                        self.statistics['segments_by_type'][tag] = \
                            self.statistics['segments_by_type'].get(tag, 0) + 1
                        
                        # Extract message metadata from service segments
                        self._extract_message_metadata(parsed_segment, parsed_message)
                        
                except Exception as e:
                    self.logger.error(f"Error parsing segment {i + 1}: {e}")
                    self.statistics['parsing_errors'] += 1
            
            # Calculate processing time
            end_time = datetime.now()
            self.statistics['processing_time'] = (end_time - start_time).total_seconds()
            
            # Store statistics in parsed message
            parsed_message.parsing_statistics = self.statistics.copy()
            
            self.logger.info(f"Parsed message with {len(parsed_message.segments)} segments "
                           f"in {self.statistics['processing_time']:.3f} seconds")
            
        except Exception as e:
            self.logger.error(f"Fatal error parsing message: {e}")
            self.statistics['parsing_errors'] += 1
            parsed_message.parsing_statistics = self.statistics.copy()
        
        return parsed_message
    
    def _parse_segment(self, segment_content: str, position: int) -> Optional[ParsedSegment]:
        """
        Parse individual segment.
        
        Args:
            segment_content: Raw segment content
            position: Segment position in message
            
        Returns:
            ParsedSegment or None if parsing fails
        """
        if not segment_content.strip():
            return None
        
        elements = self.syntax.split_elements(segment_content)
        if not elements:
            return None
        
        segment_tag = elements[0].strip()
        if not segment_tag:
            return None
        
        # Create parsed segment
        parsed_segment = ParsedSegment(
            tag=segment_tag,
            position=position
        )
        
        # Get segment definition
        segment_def = EDIFACTSegments.get_segment(segment_tag)
        if segment_def:
            parsed_segment.description = segment_def.description
            parsed_segment.group = segment_def.group
        
        # Determine qualifier for semantic mapping
        qualifier = None
        if len(elements) > 1 and elements[1]:
            # For most segments, first element contains the qualifier
            first_element_components = self.syntax.split_components(elements[1])
            if first_element_components:
                qualifier = first_element_components[0].strip()
        
        parsed_segment.qualifier = qualifier
        
        # Get semantic name
        parsed_segment.semantic_name = EDIFACTMappings.get_semantic_name(
            segment_tag, qualifier
        )
        
        # Parse elements
        for i, element_content in enumerate(elements[1:], start=1):
            try:
                parsed_element = self._parse_element(
                    element_content, i, segment_tag, segment_def
                )
                if parsed_element:
                    parsed_segment.elements.append(parsed_element)
                    self.statistics['total_elements'] += 1
                    
            except Exception as e:
                self.logger.warning(f"Error parsing element {i} in segment {segment_tag}: {e}")
                # Create placeholder element for failed parsing
                if self.generate_empty_elements:
                    parsed_segment.elements.append(ParsedElement(
                        position=i,
                        value=element_content,
                        name=f"Element{i:02d}"
                    ))
        
        return parsed_segment
    
    def _parse_element(self, element_content: str, position: int, 
                      segment_tag: str, segment_def: Optional[SegmentDefinition]) -> Optional[ParsedElement]:
        """
        Parse individual element.
        
        Args:
            element_content: Raw element content
            position: Element position in segment
            segment_tag: Parent segment tag
            segment_def: Segment definition if available
            
        Returns:
            ParsedElement or None if parsing fails
        """
        # Create parsed element
        parsed_element = ParsedElement(
            position=position,
            value=element_content if self.preserve_whitespace else element_content.strip()
        )
        
        # Get element definition
        element_def = None
        if segment_def and position <= len(segment_def.elements):
            element_def = segment_def.elements[position - 1]
            parsed_element.element_id = element_def.element_id
            parsed_element.name = element_def.name
            parsed_element.description = element_def.name
            parsed_element.is_composite = element_def.is_composite
        else:
            # Generate generic name
            parsed_element.name = EDIFACTMappings.get_element_name("", position)
        
        # Parse composite elements
        if element_def and element_def.is_composite:
            components = self.syntax.split_components(element_content)
            for j, component_content in enumerate(components, start=1):
                try:
                    parsed_component = self._parse_component(
                        component_content, j, element_def
                    )
                    if parsed_component:
                        parsed_element.components.append(parsed_component)
                        self.statistics['total_components'] += 1
                        
                except Exception as e:
                    self.logger.warning(f"Error parsing component {j} in element {position}: {e}")
                    # Create placeholder component
                    if self.generate_empty_elements:
                        parsed_element.components.append(ParsedComponent(
                            position=j,
                            value=component_content,
                            name=f"Component{j:02d}"
                        ))
        
        return parsed_element
    
    def _parse_component(self, component_content: str, position: int,
                        element_def) -> Optional[ParsedComponent]:
        """
        Parse individual component.
        
        Args:
            component_content: Raw component content
            position: Component position in element
            element_def: Parent element definition
            
        Returns:
            ParsedComponent or None if parsing fails
        """
        # Create parsed component
        parsed_component = ParsedComponent(
            position=position,
            value=component_content if self.preserve_whitespace else component_content.strip()
        )
        
        # Get component definition
        if element_def and position <= len(element_def.components):
            component_def = element_def.components[position - 1]
            parsed_component.element_id = component_def.element_id
            parsed_component.name = component_def.name
            parsed_component.description = component_def.name
        else:
            # Generate generic name
            parsed_component.name = EDIFACTMappings.get_component_name(position)
        
        return parsed_component
    
    def _extract_message_metadata(self, segment: ParsedSegment, message: ParsedMessage):
        """
        Extract message metadata from service segments.
        
        Args:
            segment: Parsed segment
            message: Message to update with metadata
        """
        if segment.tag == "UNB":
            # Extract interchange information
            if len(segment.elements) >= 5:
                # Syntax identifier
                if segment.elements[0].components:
                    message.syntax_identifier = segment.elements[0].components[0].value
                    if len(segment.elements[0].components) > 1:
                        message.syntax_version = segment.elements[0].components[1].value
                
                # Sender ID
                if segment.elements[1].components:
                    message.sender_id = segment.elements[1].components[0].value
                
                # Recipient ID
                if segment.elements[2].components:
                    message.recipient_id = segment.elements[2].components[0].value
                
                # Date/time of preparation
                if segment.elements[3].components:
                    message.preparation_date = segment.elements[3].components[0].value
                    if len(segment.elements[3].components) > 1:
                        message.preparation_time = segment.elements[3].components[1].value
                
                # Interchange reference
                if len(segment.elements) > 4:
                    message.interchange_reference = segment.elements[4].value
        
        elif segment.tag == "UNH":
            # Extract message information
            if len(segment.elements) >= 2:
                # Message reference
                message.message_reference = segment.elements[0].value
                
                # Message identifier
                if segment.elements[1].components:
                    message.message_type = segment.elements[1].components[0].value
                    if len(segment.elements[1].components) > 1:
                        message.message_version = segment.elements[1].components[1].value
                    if len(segment.elements[1].components) > 2:
                        message.message_release = segment.elements[1].components[2].value
    
    def parse_file(self, file_path: str, encoding: str = 'utf-8') -> ParsedMessage:
        """
        Parse EDIFACT message from file.
        
        Args:
            file_path: Path to EDIFACT file
            encoding: File encoding
            
        Returns:
            ParsedMessage with structured data
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            self.logger.info(f"Parsing file: {file_path}")
            return self.parse_message(content)
            
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            parsed_message = ParsedMessage()
            parsed_message.parsing_statistics = {'parsing_errors': 1}
            return parsed_message
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current parsing statistics"""
        return self.statistics.copy()
    
    def get_segment_summary(self, parsed_message: ParsedMessage) -> Dict[str, Any]:
        """
        Get summary of segments in parsed message.
        
        Args:
            parsed_message: Parsed message
            
        Returns:
            Dictionary with segment summary
        """
        summary = {
            'total_segments': len(parsed_message.segments),
            'segment_types': {},
            'service_segments': [],
            'business_segments': [],
            'unknown_segments': []
        }
        
        for segment in parsed_message.segments:
            # Count by type
            tag = segment.tag
            summary['segment_types'][tag] = summary['segment_types'].get(tag, 0) + 1
            
            # Categorize segments
            if tag in ['UNA', 'UNB', 'UNH', 'UNT', 'UNZ', 'UNS']:
                summary['service_segments'].append(tag)
            elif EDIFACTSegments.get_segment(tag):
                summary['business_segments'].append(tag)
            else:
                summary['unknown_segments'].append(tag)
        
        return summary
    
    def extract_business_data(self, parsed_message: ParsedMessage) -> Dict[str, Any]:
        """
        Extract business data from parsed message.
        
        Args:
            parsed_message: Parsed message
            
        Returns:
            Dictionary with extracted business data
        """
        business_data = {
            'message_info': {
                'type': parsed_message.message_type,
                'version': parsed_message.message_version,
                'release': parsed_message.message_release,
                'reference': parsed_message.message_reference
            },
            'interchange_info': {
                'sender': parsed_message.sender_id,
                'recipient': parsed_message.recipient_id,
                'reference': parsed_message.interchange_reference,
                'date': parsed_message.preparation_date,
                'time': parsed_message.preparation_time
            },
            'document_info': {},
            'parties': {},
            'dates': {},
            'references': {},
            'line_items': [],
            'totals': {}
        }
        
        # Extract data from business segments
        for segment in parsed_message.segments:
            if segment.tag == "BGM":
                self._extract_bgm_data(segment, business_data)
            elif segment.tag == "NAD":
                self._extract_nad_data(segment, business_data)
            elif segment.tag == "DTM":
                self._extract_dtm_data(segment, business_data)
            elif segment.tag == "RFF":
                self._extract_rff_data(segment, business_data)
            elif segment.tag == "LIN":
                self._extract_lin_data(segment, business_data)
            elif segment.tag == "MOA":
                self._extract_moa_data(segment, business_data)
        
        return business_data
    
    def _extract_bgm_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from BGM segment"""
        if segment.elements:
            # Document type
            if segment.elements[0].components:
                business_data['document_info']['type_code'] = segment.elements[0].components[0].value
            
            # Document number
            if len(segment.elements) > 1:
                business_data['document_info']['number'] = segment.elements[1].value
            
            # Message function
            if len(segment.elements) > 2:
                business_data['document_info']['function'] = segment.elements[2].value
    
    def _extract_nad_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from NAD segment"""
        if segment.elements:
            qualifier = segment.elements[0].value
            party_data = {'qualifier': qualifier}
            
            # Party ID
            if len(segment.elements) > 1 and segment.elements[1].components:
                party_data['id'] = segment.elements[1].components[0].value
            
            # Party name
            if len(segment.elements) > 3 and segment.elements[3].components:
                party_data['name'] = segment.elements[3].components[0].value
            
            business_data['parties'][qualifier] = party_data
    
    def _extract_dtm_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from DTM segment"""
        if segment.elements and segment.elements[0].components:
            qualifier = segment.elements[0].components[0].value
            date_value = segment.elements[0].components[1].value if len(segment.elements[0].components) > 1 else ""
            
            business_data['dates'][qualifier] = date_value
    
    def _extract_rff_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from RFF segment"""
        if segment.elements and segment.elements[0].components:
            qualifier = segment.elements[0].components[0].value
            reference_value = segment.elements[0].components[1].value if len(segment.elements[0].components) > 1 else ""
            
            business_data['references'][qualifier] = reference_value
    
    def _extract_lin_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from LIN segment"""
        line_item = {}
        
        if segment.elements:
            # Line number
            line_item['line_number'] = segment.elements[0].value
            
            # Item identification
            if len(segment.elements) > 2 and segment.elements[2].components:
                line_item['item_id'] = segment.elements[2].components[0].value
                if len(segment.elements[2].components) > 1:
                    line_item['item_type'] = segment.elements[2].components[1].value
        
        business_data['line_items'].append(line_item)
    
    def _extract_moa_data(self, segment: ParsedSegment, business_data: Dict[str, Any]):
        """Extract data from MOA segment"""
        if segment.elements and segment.elements[0].components:
            qualifier = segment.elements[0].components[0].value
            amount_value = segment.elements[0].components[1].value if len(segment.elements[0].components) > 1 else ""
            
            business_data['totals'][qualifier] = amount_value

