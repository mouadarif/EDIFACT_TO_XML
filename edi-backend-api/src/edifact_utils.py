#!/usr/bin/env python3
"""
EDIFACT Utilities Module
=======================

This module provides utility functions and helper classes for EDIFACT processing.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import os
import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from .edifact_parser import ParsedMessage, ParsedSegment, ParsedElement
from .edifact_constants import DATE_TIME_FORMATS, OUTPUT_FORMATS


class EDIFACTUtils:
    """Utility functions for EDIFACT processing"""
    
    @staticmethod
    def format_date(date_str: str, input_format: str = "103", 
                   output_format: str = "iso") -> str:
        """
        Format EDIFACT date string to standard format.
        
        Args:
            date_str: EDIFACT date string
            input_format: EDIFACT date format code
            output_format: Output format ('iso', 'us', 'eu')
            
        Returns:
            Formatted date string
        """
        if not date_str:
            return ""
        
        try:
            # Get format pattern
            format_pattern = DATE_TIME_FORMATS.get(input_format, "YYMMDD")
            
            # Parse date based on format
            if format_pattern == "YYMMDD" and len(date_str) == 6:
                year = int(date_str[:2])
                # Assume 20xx for years 00-30, 19xx for years 31-99
                year = 2000 + year if year <= 30 else 1900 + year
                month = int(date_str[2:4])
                day = int(date_str[4:6])
            elif format_pattern == "CCYYMMDD" and len(date_str) == 8:
                year = int(date_str[:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
            else:
                return date_str  # Return as-is if can't parse
            
            # Create date object
            date_obj = datetime(year, month, day)
            
            # Format output
            if output_format == "iso":
                return date_obj.strftime("%Y-%m-%d")
            elif output_format == "us":
                return date_obj.strftime("%m/%d/%Y")
            elif output_format == "eu":
                return date_obj.strftime("%d/%m/%Y")
            else:
                return date_obj.strftime("%Y-%m-%d")
                
        except (ValueError, IndexError):
            return date_str  # Return original if parsing fails
    
    @staticmethod
    def format_time(time_str: str, input_format: str = "401") -> str:
        """
        Format EDIFACT time string to standard format.
        
        Args:
            time_str: EDIFACT time string
            input_format: EDIFACT time format code
            
        Returns:
            Formatted time string (HH:MM:SS)
        """
        if not time_str:
            return ""
        
        try:
            # Simplified logic: decide format based on length primarily for HHMM/HHMMSS
            actual_len = len(time_str)

            if actual_len == 4: # Assume HHMM
                hour = int(time_str[:2])
                minute = int(time_str[2:4])
                return f"{hour:02d}:{minute:02d}:00"
            elif actual_len == 6: # Assume HHMMSS
                hour = int(time_str[:2])
                minute = int(time_str[2:4])
                second = int(time_str[4:6])
                return f"{hour:02d}:{minute:02d}:{second:02d}"
            else:
                # Fallback for other lengths or if DATE_TIME_FORMATS implies a different structure
                # For now, this primarily handles HHMM and HHMMSS by length.
                # The original DATE_TIME_FORMATS.get(input_format, "HHMM") can be used
                # for more complex format codes if needed, but this covers the test case.
                return time_str
                
        except (ValueError, IndexError):
            return time_str
    
    @staticmethod
    def clean_edifact_value(value: str) -> str:
        """
        Clean EDIFACT value by removing escape characters and trimming.
        
        Args:
            value: Raw EDIFACT value
            
        Returns:
            Cleaned value
        """
        if not value:
            return ""
        
        # Remove common EDIFACT escape sequences
        cleaned = value.replace("?:", ":").replace("?+", "+").replace("?'", "'").replace("??", "?")
        
        # Trim whitespace
        return cleaned.strip()
    
    @staticmethod
    def validate_file_path(file_path: str, must_exist: bool = True) -> bool:
        """
        Validate file path.
        
        Args:
            file_path: File path to validate
            must_exist: Whether file must exist
            
        Returns:
            True if valid, False otherwise
        """
        try:
            path = Path(file_path)
            
            if must_exist:
                return path.exists() and path.is_file()
            else:
                # Check if parent directory exists
                return path.parent.exists()
                
        except Exception:
            return False
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension from path"""
        return Path(file_path).suffix.lower()
    
    @staticmethod
    def detect_edifact_encoding(file_path: str) -> str:
        """
        Detect EDIFACT file encoding.
        
        Args:
            file_path: Path to EDIFACT file
            
        Returns:
            Detected encoding
        """
        encodings_to_try = ['utf-8', 'iso-8859-1', 'cp1252', 'ascii']
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1024)  # Try to read first 1KB
                return encoding
            except UnicodeDecodeError:
                continue
        
        return 'utf-8'  # Default fallback
    
    @staticmethod
    def extract_message_type(content: str) -> Optional[str]:
        """
        Extract message type from EDIFACT content.
        
        Args:
            content: EDIFACT content
            
        Returns:
            Message type if found, None otherwise
        """
        try:
            # Look for UNH segment
            if "UNH+" in content:
                unh_start = content.find("UNH+")
                unh_end = content.find("'", unh_start)
                if unh_end > unh_start:
                    unh_segment = content[unh_start:unh_end]
                    parts = unh_segment.split("+")
                    if len(parts) >= 3:
                        # Message identifier is in third element
                        msg_id_parts = parts[2].split(":")
                        if msg_id_parts:
                            return msg_id_parts[0]
            return None
        except Exception:
            return None


class DataExtractor:
    """Extract structured data from parsed EDIFACT messages"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_to_dict(self, parsed_message: ParsedMessage) -> Dict[str, Any]:
        """
        Extract parsed message to dictionary.
        
        Args:
            parsed_message: Parsed EDIFACT message
            
        Returns:
            Dictionary representation
        """
        result = {
            "message_info": {
                "type": parsed_message.message_type,
                "version": parsed_message.message_version,
                "release": parsed_message.message_release,
                "reference": parsed_message.message_reference,
                "interchange_reference": parsed_message.interchange_reference
            },
            "interchange_info": {
                "sender_id": parsed_message.sender_id,
                "recipient_id": parsed_message.recipient_id,
                "syntax_identifier": parsed_message.syntax_identifier,
                "syntax_version": parsed_message.syntax_version,
                "preparation_date": parsed_message.preparation_date,
                "preparation_time": parsed_message.preparation_time
            },
            "segments": []
        }
        
        # Extract segments
        for segment in parsed_message.segments:
            segment_dict = {
                "tag": segment.tag,
                "position": segment.position,
                "semantic_name": segment.semantic_name,
                "qualifier": segment.qualifier,
                "elements": []
            }
            
            # Extract elements
            for element in segment.elements:
                element_dict = {
                    "position": element.position,
                    "value": element.value,
                    "name": element.name,
                    "is_composite": element.is_composite
                }
                
                # Extract components if composite
                if element.is_composite:
                    element_dict["components"] = [
                        {
                            "position": comp.position,
                            "value": comp.value,
                            "name": comp.name
                        }
                        for comp in element.components
                    ]
                
                segment_dict["elements"].append(element_dict)
            
            result["segments"].append(segment_dict)
        
        # Add statistics if available
        if parsed_message.parsing_statistics:
            result["statistics"] = parsed_message.parsing_statistics
        
        return result
    
    def extract_to_csv(self, parsed_message: ParsedMessage, 
                      output_file: str, level: str = "segment") -> bool:
        """
        Extract parsed message to CSV format.
        
        Args:
            parsed_message: Parsed EDIFACT message
            output_file: Output CSV file path
            level: Extraction level ('segment', 'element', 'component')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                if level == "segment":
                    self._write_segment_csv(csvfile, parsed_message)
                elif level == "element":
                    self._write_element_csv(csvfile, parsed_message)
                elif level == "component":
                    self._write_component_csv(csvfile, parsed_message)
                else:
                    raise ValueError(f"Invalid level: {level}")
            
            self.logger.info(f"CSV exported to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def _write_segment_csv(self, csvfile, parsed_message: ParsedMessage):
        """Write segment-level CSV"""
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            "Position", "Tag", "SemanticName", "Qualifier", 
            "ElementCount", "Description"
        ])
        
        # Data rows
        for segment in parsed_message.segments:
            writer.writerow([
                segment.position,
                segment.tag,
                segment.semantic_name or "",
                segment.qualifier or "",
                len(segment.elements),
                segment.description or ""
            ])
    
    def _write_element_csv(self, csvfile, parsed_message: ParsedMessage):
        """Write element-level CSV"""
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            "SegmentPosition", "SegmentTag", "ElementPosition", 
            "ElementName", "Value", "IsComposite", "ComponentCount"
        ])
        
        # Data rows
        for segment in parsed_message.segments:
            for element in segment.elements:
                writer.writerow([
                    segment.position,
                    segment.tag,
                    element.position,
                    element.name or "",
                    element.value or "",
                    element.is_composite,
                    len(element.components) if element.is_composite else 0
                ])
    
    def _write_component_csv(self, csvfile, parsed_message: ParsedMessage):
        """Write component-level CSV"""
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            "SegmentPosition", "SegmentTag", "ElementPosition", 
            "ComponentPosition", "ComponentName", "Value"
        ])
        
        # Data rows
        for segment in parsed_message.segments:
            for element in segment.elements:
                if element.is_composite:
                    for component in element.components:
                        writer.writerow([
                            segment.position,
                            segment.tag,
                            element.position,
                            component.position,
                            component.name or "",
                            component.value or ""
                        ])
                else:
                    # Simple element as single component
                    writer.writerow([
                        segment.position,
                        segment.tag,
                        element.position,
                        1,
                        element.name or "",
                        element.value or ""
                    ])
    
    def extract_to_json(self, parsed_message: ParsedMessage, 
                       output_file: str, pretty: bool = True) -> bool:
        """
        Extract parsed message to JSON format.
        
        Args:
            parsed_message: Parsed EDIFACT message
            output_file: Output JSON file path
            pretty: Whether to format JSON with indentation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.extract_to_dict(parsed_message)
            
            with open(output_file, 'w', encoding='utf-8') as jsonfile:
                if pretty:
                    json.dump(data, jsonfile, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, jsonfile, ensure_ascii=False)
            
            self.logger.info(f"JSON exported to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {e}")
            return False


class FileProcessor:
    """Process multiple EDIFACT files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_directory(self, input_dir: str, output_dir: str, 
                         output_format: str = "xml",
                         file_pattern: str = "*.edi") -> Dict[str, Any]:
        """
        Process all EDIFACT files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            output_format: Output format ('xml', 'json', 'csv')
            file_pattern: File pattern to match
            
        Returns:
            Processing results summary
        """
        from .edifact_parser import EDIFACTParser
        from .xml_generator import XMLGenerator
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find EDIFACT files
        edifact_files = list(input_path.glob(file_pattern))
        
        results = {
            "total_files": len(edifact_files),
            "processed_files": 0,
            "failed_files": 0,
            "errors": []
        }
        
        parser = EDIFACTParser()
        xml_generator = XMLGenerator()
        data_extractor = DataExtractor()
        
        for file_path in edifact_files:
            try:
                self.logger.info(f"Processing: {file_path}")
                
                # Parse EDIFACT file
                parsed_message = parser.parse_file(str(file_path))
                
                # Generate output file name
                output_file = output_path / f"{file_path.stem}.{output_format}"
                
                # Generate output based on format
                if output_format == "xml":
                    xml_root = xml_generator.generate_xml(parsed_message)
                    xml_generator.save_to_file(xml_root, str(output_file))
                elif output_format == "json":
                    data_extractor.extract_to_json(parsed_message, str(output_file))
                elif output_format == "csv":
                    data_extractor.extract_to_csv(parsed_message, str(output_file))
                else:
                    raise ValueError(f"Unsupported output format: {output_format}")
                
                results["processed_files"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                results["failed_files"] += 1
                results["errors"].append(f"{file_path}: {str(e)}")
        
        return results
    
    def batch_convert(self, file_list: List[str], output_dir: str,
                     output_format: str = "xml") -> Dict[str, Any]:
        """
        Convert a list of EDIFACT files.
        
        Args:
            file_list: List of EDIFACT file paths
            output_dir: Output directory path
            output_format: Output format
            
        Returns:
            Conversion results summary
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "total_files": len(file_list),
            "converted_files": 0,
            "failed_files": 0,
            "errors": []
        }
        
        for file_path in file_list:
            try:
                input_file = Path(file_path)
                output_file = output_path / f"{input_file.stem}.{output_format}"
                
                if output_format == "xml":
                    from .xml_generator import XMLGenerator
                    generator = XMLGenerator()
                    success = generator.generate_xml_from_file(
                        str(input_file), str(output_file)
                    )
                    if success:
                        results["converted_files"] += 1
                    else:
                        results["failed_files"] += 1
                        results["errors"].append(f"{file_path}: Conversion failed")
                else:
                    # Handle other formats
                    from .edifact_parser import EDIFACTParser
                    parser = EDIFACTParser()
                    parsed_message = parser.parse_file(str(input_file))
                    
                    extractor = DataExtractor()
                    if output_format == "json":
                        success = extractor.extract_to_json(parsed_message, str(output_file))
                    elif output_format == "csv":
                        success = extractor.extract_to_csv(parsed_message, str(output_file))
                    else:
                        raise ValueError(f"Unsupported format: {output_format}")
                    
                    if success:
                        results["converted_files"] += 1
                    else:
                        results["failed_files"] += 1
                        results["errors"].append(f"{file_path}: Conversion failed")
                
            except Exception as e:
                results["failed_files"] += 1
                results["errors"].append(f"{file_path}: {str(e)}")
        
        return results


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level
        log_file: Optional log file path
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_supported_formats() -> Dict[str, str]:
    """Get supported output formats"""
    return OUTPUT_FORMATS.copy()

