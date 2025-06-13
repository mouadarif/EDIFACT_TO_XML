#!/usr/bin/env python3
"""
EDIFACT Syntax Module
====================

This module defines the EDIFACT syntax characters and provides utilities
for parsing UNA segments and handling syntax variations.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, Optional, NamedTuple
import re


class EDIFACTSyntaxChars(NamedTuple):
    """EDIFACT syntax characters structure"""
    component_separator: str = ":"
    element_separator: str = "+"
    decimal_point: str = "."
    escape_character: str = "?"
    reserved: str = " "
    segment_terminator: str = "'"


class EDIFACTSyntax:
    """
    EDIFACT syntax character definitions and parsing utilities.
    
    Handles UNA segment parsing and provides default syntax characters
    according to UN/EDIFACT standards.
    """
    
    # Default syntax characters (UN/EDIFACT standard)
    DEFAULT_SYNTAX = EDIFACTSyntaxChars()
    
    def __init__(self, syntax_chars: Optional[EDIFACTSyntaxChars] = None):
        """
        Initialize EDIFACT syntax handler.
        
        Args:
            syntax_chars: Custom syntax characters, defaults to standard if None
        """
        self.syntax = syntax_chars or self.DEFAULT_SYNTAX
    
    @classmethod
    def from_una_segment(cls, una_content: str) -> 'EDIFACTSyntax':
        """
        Create EDIFACTSyntax instance from UNA segment.
        
        Args:
            una_content: UNA segment content (e.g., "UNA:+.? '")
            
        Returns:
            EDIFACTSyntax instance with parsed syntax characters
            
        Raises:
            ValueError: If UNA segment format is invalid
        """
        if not una_content or len(una_content) < 9:
            raise ValueError("Invalid UNA segment: too short")
            
        if not una_content.startswith("UNA"):
            raise ValueError("Invalid UNA segment: must start with 'UNA'")
        
        try:
            syntax_chars = EDIFACTSyntaxChars(
                component_separator=una_content[3],
                element_separator=una_content[4],
                decimal_point=una_content[5],
                escape_character=una_content[6],
                reserved=una_content[7],
                segment_terminator=una_content[8]
            )
            return cls(syntax_chars)
        except IndexError as e:
            raise ValueError(f"Invalid UNA segment format: {e}")
    
    def parse_una_segment(self, una_content: str) -> Dict[str, str]:
        """
        Parse UNA segment and return syntax characters as dictionary.
        
        Args:
            una_content: UNA segment content
            
        Returns:
            Dictionary with syntax character mappings
        """
        if len(una_content) >= 9 and una_content.startswith("UNA"):
            return {
                'component_separator': una_content[3],
                'element_separator': una_content[4],
                'decimal_point': una_content[5],
                'escape_character': una_content[6],
                'reserved': una_content[7],
                'segment_terminator': una_content[8]
            }
        return {}
    
    def escape_data(self, data: str) -> str:
        """
        Escape special characters in EDIFACT data.
        
        Args:
            data: Raw data string
            
        Returns:
            Escaped data string
        """
        if not data:
            return data
            
        # Escape in correct order to avoid double escaping
        escape_char = self.syntax.escape_character
        
        # First escape the escape character itself
        data = data.replace(escape_char, escape_char + escape_char)
        
        # Then escape other special characters
        data = data.replace(self.syntax.component_separator, 
                          escape_char + self.syntax.component_separator)
        data = data.replace(self.syntax.element_separator, 
                          escape_char + self.syntax.element_separator)
        data = data.replace(self.syntax.segment_terminator, 
                          escape_char + self.syntax.segment_terminator)
        
        return data
    
    def unescape_data(self, data: str) -> str:
        """
        Unescape EDIFACT data by removing escape characters.
        
        Args:
            data: Escaped data string
            
        Returns:
            Unescaped data string
        """
        if not data:
            return data
            
        escape_char = self.syntax.escape_character
        
        # Remove escape sequences
        data = data.replace(escape_char + self.syntax.component_separator, 
                          self.syntax.component_separator)
        data = data.replace(escape_char + self.syntax.element_separator, 
                          self.syntax.element_separator)
        data = data.replace(escape_char + self.syntax.segment_terminator, 
                          self.syntax.segment_terminator)
        
        # Finally unescape the escape character itself
        data = data.replace(escape_char + escape_char, escape_char)
        
        return data
    
    def split_segments(self, content: str) -> list:
        """
        Split EDIFACT content into segments.
        
        Args:
            content: Raw EDIFACT content
            
        Returns:
            List of segment strings
        """
        # Handle escaped segment terminators
        segments = []
        current_segment = ""
        i = 0
        
        while i < len(content):
            char = content[i]
            
            if char == self.syntax.escape_character and i + 1 < len(content):
                # Escaped character - add both escape and next character
                current_segment += char + content[i + 1]
                i += 2
            elif char == self.syntax.segment_terminator:
                # End of segment
                if current_segment.strip():
                    segments.append(current_segment.strip())
                current_segment = ""
                i += 1
            else:
                current_segment += char
                i += 1
        
        # Add final segment if exists
        if current_segment.strip():
            segments.append(current_segment.strip())
            
        return segments
    
    def split_elements(self, segment: str) -> list:
        """
        Split segment into elements.
        
        Args:
            segment: Segment string
            
        Returns:
            List of element strings
        """
        elements = []
        current_element = ""
        i = 0
        
        while i < len(segment):
            char = segment[i]
            
            if char == self.syntax.escape_character and i + 1 < len(segment):
                # Escaped character
                current_element += char + segment[i + 1]
                i += 2
            elif char == self.syntax.element_separator:
                # End of element
                elements.append(current_element)
                current_element = ""
                i += 1
            else:
                current_element += char
                i += 1
        
        # Add final element
        elements.append(current_element)
        
        return elements
    
    def split_components(self, element: str) -> list:
        """
        Split element into components.
        
        Args:
            element: Element string
            
        Returns:
            List of component strings
        """
        components = []
        current_component = ""
        i = 0
        
        while i < len(element):
            char = element[i]
            
            if char == self.syntax.escape_character and i + 1 < len(element):
                # Escaped character
                current_component += char + element[i + 1]
                i += 2
            elif char == self.syntax.component_separator:
                # End of component
                components.append(current_component)
                current_component = ""
                i += 1
            else:
                current_component += char
                i += 1
        
        # Add final component
        components.append(current_component)
        
        return components
    
    def validate_syntax_characters(self) -> bool:
        """
        Validate that all syntax characters are unique.
        
        Returns:
            True if all syntax characters are unique, False otherwise
        """
        chars = [
            self.syntax.component_separator,
            self.syntax.element_separator,
            self.syntax.decimal_point,
            self.syntax.escape_character,
            self.syntax.segment_terminator
        ]
        
        return len(chars) == len(set(chars))
    
    def __str__(self) -> str:
        """String representation of syntax characters."""
        return (f"EDIFACTSyntax("
                f"component='{self.syntax.component_separator}', "
                f"element='{self.syntax.element_separator}', "
                f"decimal='{self.syntax.decimal_point}', "
                f"escape='{self.syntax.escape_character}', "
                f"segment='{self.syntax.segment_terminator}')")
    
    def __repr__(self) -> str:
        """Detailed representation of syntax characters."""
        return self.__str__()


# Syntax validation patterns
SYNTAX_PATTERNS = {
    'segment_tag': re.compile(r'^[A-Z]{3}$'),
    'numeric': re.compile(r'^\d+$'),
    'alphanumeric': re.compile(r'^[A-Za-z0-9]+$'),
    'date_yymmdd': re.compile(r'^\d{6}$'),
    'date_ccyymmdd': re.compile(r'^\d{8}$'),
    'time_hhmm': re.compile(r'^\d{4}$'),
    'time_hhmmss': re.compile(r'^\d{6}$'),
}


def validate_segment_tag(tag: str) -> bool:
    """Validate EDIFACT segment tag format."""
    return bool(SYNTAX_PATTERNS['segment_tag'].match(tag))


def validate_numeric(value: str) -> bool:
    """Validate numeric value format."""
    return bool(SYNTAX_PATTERNS['numeric'].match(value))


def validate_alphanumeric(value: str) -> bool:
    """Validate alphanumeric value format."""
    return bool(SYNTAX_PATTERNS['alphanumeric'].match(value))


def validate_date_format(date_str: str, format_type: str = 'yymmdd') -> bool:
    """
    Validate date format.
    
    Args:
        date_str: Date string to validate
        format_type: 'yymmdd' or 'ccyymmdd'
        
    Returns:
        True if valid format, False otherwise
    """
    pattern_key = f'date_{format_type}'
    if pattern_key in SYNTAX_PATTERNS:
        return bool(SYNTAX_PATTERNS[pattern_key].match(date_str))
    return False


def validate_time_format(time_str: str, format_type: str = 'hhmm') -> bool:
    """
    Validate time format.
    
    Args:
        time_str: Time string to validate
        format_type: 'hhmm' or 'hhmmss'
        
    Returns:
        True if valid format, False otherwise
    """
    pattern_key = f'time_{format_type}'
    if pattern_key in SYNTAX_PATTERNS:
        return bool(SYNTAX_PATTERNS[pattern_key].match(time_str))
    return False

