#!/usr/bin/env python3
"""
XML Generator Module
===================

This module generates XML output from parsed EDIFACT messages,
providing comprehensive and structured XML representation.

Author: EDIFACT Parser Team
Version: 1.0.0
"""
import re # Ensure re is imported
from typing import Dict, List, Optional, Any, Union
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import logging
from .edifact_parser import ParsedMessage, ParsedSegment, ParsedElement, ParsedComponent
from .edifact_mappings import EDIFACTMappings, MappingContext
from .edifact_constants import DEFAULT_XML_STRUCTURE, XML_NAMESPACES


class XMLGeneratorConfig:
    """Configuration for XML generation"""
    
    def __init__(self,
                 generate_empty_tags: bool = True,
                 include_attributes: bool = True,
                 include_descriptions: bool = False,
                 pretty_print: bool = True,
                 indent_size: int = 2,
                 xml_encoding: str = 'UTF-8',
                 xml_version: str = '1.0',
                 use_semantic_names: bool = True,
                 group_segments: bool = True,
                 include_statistics: bool = True,
                 include_validation_info: bool = True):
        """
        Initialize XML generator configuration.
        
        Args:
            generate_empty_tags: Generate empty XML tags for missing elements
            include_attributes: Include EDIFACT attributes in XML elements
            include_descriptions: Include description attributes
            pretty_print: Format XML with indentation
            indent_size: Number of spaces for indentation
            xml_encoding: XML encoding declaration
            xml_version: XML version declaration
            use_semantic_names: Use semantic element names instead of generic ones
            group_segments: Group segments by type in XML structure
            include_statistics: Include parsing statistics in XML
            include_validation_info: Include validation results in XML
        """
        self.generate_empty_tags = generate_empty_tags
        self.include_attributes = include_attributes
        self.include_descriptions = include_descriptions
        self.pretty_print = pretty_print
        self.indent_size = indent_size
        self.xml_encoding = xml_encoding
        self.xml_version = xml_version
        self.use_semantic_names = use_semantic_names
        self.group_segments = group_segments
        self.include_statistics = include_statistics
        self.include_validation_info = include_validation_info


class XMLGenerator:
    """
    XML generator for EDIFACT messages.
    
    Converts parsed EDIFACT messages into comprehensive XML representation
    with semantic element names and proper structure.
    """
    
    def __init__(self, config: Optional[XMLGeneratorConfig] = None):
        """
        Initialize XML generator.
        
        Args:
            config: XML generation configuration
        """
        self.config = config or XMLGeneratorConfig()
        self.logger = logging.getLogger(__name__)
        
        # XML namespace handling
        self.namespaces = XML_NAMESPACES.copy()
        
        # Register namespaces
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)

    def _sanitize_xml_tag_name(self, name: str, default_prefix: str = "Element") -> str:
        if not name:
            return f"{default_prefix}Unnamed"

        # Remove leading/trailing whitespace
        name = name.strip()

        # Replace common separators and problematic characters with underscore
        # This list can beexpanded.
        name = re.sub(r"[\s,:;()\/?#*']+", "_", name) # More comprehensive, excluding " . - which are handled or valid

        # Remove any characters not allowed in XML names (simplified: letters, digits, underscore, period, hyphen)
        # XML spec is more complex, but this covers many cases.
        # Keep letters, digits, underscore, period, hyphen.
        name = re.sub(r"[^a-zA-Z0-9_.-]", "", name) # Added hyphen to allowed characters

        # XML names must start with a letter or underscore.
        if not re.match(r"^[a-zA-Z_]", name):
            name = default_prefix + "_" + name # Prepend prefix and underscore if it doesn't start correctly

        # If the name became empty or just underscores after sanitization, provide a default
        if not name or name.strip("_") == "":
            return f"{default_prefix}SanitizedEmpty"

        return name
    
    def generate_xml(self, parsed_message: ParsedMessage, 
                    root_element_name: Optional[str] = None) -> ET.Element:
        """
        Generate XML from parsed EDIFACT message.
        
        Args:
            parsed_message: Parsed EDIFACT message
            root_element_name: Custom root element name
            
        Returns:
            XML Element tree root
        """
        # Determine root element name
        if root_element_name:
            root_name = root_element_name
        elif parsed_message.message_type:
            # Use message type specific root element
            message_mappings = EDIFACTMappings.get_message_type_mappings()
            if parsed_message.message_type in message_mappings:
                root_name = message_mappings[parsed_message.message_type].get(
                    'root_element', 'EDIFACTMessage'
                )
            else:
                root_name = f"{parsed_message.message_type}Message"
        else:
            root_name = "EDIFACTMessage"
        
        # Create root element
        root = ET.Element(root_name)
        
        # Add namespace declarations
        if self.config.include_attributes:
            for prefix, uri in self.namespaces.items():
                root.set(f"xmlns:{prefix}", uri)
        
        # Add message metadata
        self._add_message_metadata(root, parsed_message)
        
        # Generate XML structure
        if self.config.group_segments:
            self._generate_grouped_structure(root, parsed_message)
        else:
            self._generate_flat_structure(root, parsed_message)
        
        # Add statistics if requested
        if self.config.include_statistics and parsed_message.parsing_statistics:
            self._add_statistics(root, parsed_message.parsing_statistics)
        
        # Add validation information if requested
        if (self.config.include_validation_info and 
            parsed_message.validation_result):
            self._add_validation_info(root, parsed_message.validation_result)
        
        return root
    
    def _add_message_metadata(self, root: ET.Element, parsed_message: ParsedMessage):
        """Add message metadata to root element"""
        if self.config.include_attributes:
            # Add message attributes
            if parsed_message.message_type:
                root.set("messageType", parsed_message.message_type)
            if parsed_message.message_version:
                root.set("messageVersion", parsed_message.message_version)
            if parsed_message.message_release:
                root.set("messageRelease", parsed_message.message_release)
            if parsed_message.message_reference:
                root.set("messageReference", parsed_message.message_reference)
            if parsed_message.interchange_reference:
                root.set("interchangeReference", parsed_message.interchange_reference)
            if parsed_message.syntax_identifier:
                root.set("syntaxIdentifier", parsed_message.syntax_identifier)
            
            # Add generation timestamp
            root.set("generatedAt", datetime.now().isoformat())
        
        # Create envelope section
        envelope = ET.SubElement(root, "Envelope")
        
        # Add version information
        version_elem = ET.SubElement(envelope, "TIEXMLVersionNumber")
        version_elem.text = "2.3.2"
        
        # Add interchange information
        if any([parsed_message.sender_id, parsed_message.recipient_id, 
                parsed_message.preparation_date]):
            interchange = ET.SubElement(envelope, "InterchangeInfo")
            
            if parsed_message.sender_id:
                sender_elem = ET.SubElement(interchange, "Sender")
                sender_elem.text = parsed_message.sender_id
            
            if parsed_message.recipient_id:
                recipient_elem = ET.SubElement(interchange, "Recipient")
                recipient_elem.text = parsed_message.recipient_id
            
            if parsed_message.preparation_date:
                date_elem = ET.SubElement(interchange, "PreparationDate")
                date_elem.text = parsed_message.preparation_date
                
                if parsed_message.preparation_time:
                    time_elem = ET.SubElement(interchange, "PreparationTime")
                    time_elem.text = parsed_message.preparation_time
    
    def _generate_grouped_structure(self, root: ET.Element, parsed_message: ParsedMessage):
        """Generate XML with segments grouped by type"""
        
        # Group segments by category
        segment_groups = {
            'service': [],
            'header': [],
            'detail': [],
            'summary': []
        }
        
        for segment in parsed_message.segments:
            if segment.tag in ['UNA', 'UNB', 'UNH', 'UNT', 'UNZ', 'UNS']:
                segment_groups['service'].append(segment)
            elif segment.tag in ['BGM', 'DTM', 'RFF', 'NAD', 'CTA', 'COM', 'CUX', 'PAT', 'TOD']:
                segment_groups['header'].append(segment)
            elif segment.tag in ['LIN', 'PIA', 'IMD', 'QTY', 'PRI', 'MOA', 'TAX', 'ALC']:
                segment_groups['detail'].append(segment)
            elif segment.tag in ['CNT', 'UNS']:
                segment_groups['summary'].append(segment)
            else:
                # Default to header for unknown segments
                segment_groups['header'].append(segment)
        
        # Create grouped sections
        if segment_groups['service']:
            service_section = ET.SubElement(root, "ServiceSegments")
            for segment in segment_groups['service']:
                self._add_segment_to_xml(service_section, segment)
        
        if segment_groups['header']:
            header_section = ET.SubElement(root, "HeaderSegments")
            for segment in segment_groups['header']:
                self._add_segment_to_xml(header_section, segment)
        
        if segment_groups['detail']:
            detail_section = ET.SubElement(root, "DetailSegments")
            for segment in segment_groups['detail']:
                self._add_segment_to_xml(detail_section, segment)
        
        if segment_groups['summary']:
            summary_section = ET.SubElement(root, "SummarySegments")
            for segment in segment_groups['summary']:
                self._add_segment_to_xml(summary_section, segment)
    
    def _generate_flat_structure(self, root: ET.Element, parsed_message: ParsedMessage):
        """Generate XML with flat segment structure"""
        segments_container = ET.SubElement(root, "Segments")
        
        for segment in parsed_message.segments:
            self._add_segment_to_xml(segments_container, segment)
    
    def _add_segment_to_xml(self, parent: ET.Element, segment: ParsedSegment):
        """Add segment to XML parent element"""
        
        # Determine element name
        raw_name = ""
        if self.config.use_semantic_names and segment.semantic_name:
            raw_name = segment.semantic_name
        else:
            raw_name = segment.tag
        element_name = self._sanitize_xml_tag_name(raw_name, default_prefix=segment.tag or "Segment")
        
        # Create segment element
        segment_elem = ET.SubElement(parent, element_name)
        
        # Add attributes
        if self.config.include_attributes:
            segment_elem.set("segmentTag", segment.tag)
            segment_elem.set("position", str(segment.position))
            
            if segment.qualifier:
                segment_elem.set("qualifier", segment.qualifier)
            
            if segment.group:
                segment_elem.set("group", segment.group.value)
            
            if self.config.include_descriptions and segment.description:
                segment_elem.set("description", segment.description)
        
        # Add elements
        for element in segment.elements:
            self._add_element_to_xml(segment_elem, element, segment.tag)
        
        # Generate empty elements if requested
        if self.config.generate_empty_tags:
            self._add_empty_elements(segment_elem, segment)
    
    def _add_element_to_xml(self, parent: ET.Element, element: ParsedElement, segment_tag: str):
        """Add element to XML parent"""
        
        # Determine element name
        raw_name = ""
        if self.config.use_semantic_names and element.name:
            raw_name = element.name
        # else, raw_name remains empty, sanitize_xml_tag_name will use default_prefix

        default_el_prefix = f"Element{element.position:02d}"
        element_name = self._sanitize_xml_tag_name(raw_name, default_prefix=default_el_prefix)
        if not raw_name and not (self.config.use_semantic_names and element.name): # if raw_name was truly empty from start
            element_name = default_el_prefix # Fallback to Element01 if semantic name was empty/not used
        
        # Create element
        element_elem = ET.SubElement(parent, element_name)
        
        # Add attributes
        if self.config.include_attributes:
            element_elem.set("position", str(element.position))
            
            if element.element_id:
                element_elem.set("elementId", element.element_id)
            
            if element.is_composite:
                element_elem.set("type", "composite")
            else:
                element_elem.set("type", "simple")
            
            if self.config.include_descriptions and element.description:
                element_elem.set("description", element.description)
        
        # Handle composite elements
        if element.is_composite and element.components:
            for component in element.components:
                self._add_component_to_xml(element_elem, component)
        else:
            # Simple element - add text content
            element_elem.text = element.value or ""
        
        # Generate empty components if requested
        if self.config.generate_empty_tags and element.is_composite:
            self._add_empty_components(element_elem, element)
    
    def _add_component_to_xml(self, parent: ET.Element, component: ParsedComponent):
        """Add component to XML parent"""
        
        # Determine component name
        raw_name = ""
        if self.config.use_semantic_names and component.name:
            raw_name = component.name
        # else, raw_name remains empty

        default_comp_prefix = f"Component{component.position:02d}"
        component_name = self._sanitize_xml_tag_name(raw_name, default_prefix=default_comp_prefix)
        if not raw_name and not (self.config.use_semantic_names and component.name): # if raw_name was truly empty
            component_name = default_comp_prefix # Fallback to Component01
        
        # Create component element
        component_elem = ET.SubElement(parent, component_name)
        component_elem.text = component.value or ""
        
        # Add attributes
        if self.config.include_attributes:
            component_elem.set("position", str(component.position))
            
            if component.element_id:
                component_elem.set("elementId", component.element_id)
            
            if self.config.include_descriptions and component.description:
                component_elem.set("description", component.description)
    
    def _add_empty_elements(self, parent: ET.Element, segment: ParsedSegment):
        """Add empty elements for missing data"""
        # This would add empty elements based on segment definition
        # Implementation depends on specific requirements
        pass
    
    def _add_empty_components(self, parent: ET.Element, element: ParsedElement):
        """Add empty components for missing data"""
        # This would add empty components based on element definition
        # Implementation depends on specific requirements
        pass
    
    def _add_statistics(self, root: ET.Element, statistics: Dict[str, Any]):
        """Add parsing statistics to XML"""
        stats_elem = ET.SubElement(root, "ParsingStatistics")
        
        for key, value in statistics.items():
            if isinstance(value, dict):
                # Handle nested dictionaries
                sub_elem = ET.SubElement(stats_elem, key.title().replace("_", ""))
                for sub_key, sub_value in value.items():
                    item_elem = ET.SubElement(sub_elem, "Item")
                    item_elem.set("key", str(sub_key))
                    item_elem.text = str(sub_value)
            else:
                # Handle simple values
                stat_elem = ET.SubElement(stats_elem, key.title().replace("_", ""))
                stat_elem.text = str(value)
    
    def _add_validation_info(self, root: ET.Element, validation_result):
        """Add validation information to XML"""
        validation_elem = ET.SubElement(root, "ValidationInfo")
        
        # Add summary
        summary_elem = ET.SubElement(validation_elem, "Summary")
        summary_elem.set("isValid", str(validation_result.is_valid).lower())
        summary_elem.set("errorCount", str(validation_result.error_count))
        summary_elem.set("warningCount", str(validation_result.warning_count))
        summary_elem.set("infoCount", str(validation_result.info_count))
        
        # Add messages
        if validation_result.messages:
            messages_elem = ET.SubElement(validation_elem, "Messages")
            
            for message in validation_result.messages:
                msg_elem = ET.SubElement(messages_elem, "Message")
                msg_elem.set("severity", message.severity.value)
                msg_elem.set("code", message.code)
                msg_elem.text = message.message
                
                if message.segment_tag:
                    msg_elem.set("segmentTag", message.segment_tag)
                if message.segment_position is not None:
                    msg_elem.set("segmentPosition", str(message.segment_position))
                if message.element_position is not None:
                    msg_elem.set("elementPosition", str(message.element_position))
                if message.component_position is not None:
                    msg_elem.set("componentPosition", str(message.component_position))
    
    def to_string(self, xml_root: ET.Element) -> str:
        """
        Convert XML element to string.
        
        Args:
            xml_root: XML root element
            
        Returns:
            XML string representation
        """
        if self.config.pretty_print:
            # Use minidom for pretty printing
            rough_string = ET.tostring(xml_root, encoding='unicode')
            try:
                reparsed = minidom.parseString(rough_string)
                pretty_xml = reparsed.toprettyxml(indent=" " * self.config.indent_size)

                # Remove extra blank lines
                lines = [line for line in pretty_xml.split('\n') if line.strip()]
                return '\n'.join(lines)
            except Exception as e:
                print(f"DEBUG: Error during minidom.parseString or subsequent pretty_print processing: {e}")
                print(f"DEBUG: Dumping rough_string (len={len(rough_string)}):")
                # Print in chunks if it's extremely long to avoid truncation in logs,
                # though for this error at col 3017, it should be manageable.
                # Ensure the full string relevant to the error is printed.
                # For an error at column 3017, we need to see at least that much.
                # Let's print a sizeable portion around the suspected error point if possible,
                # or just the beginning portion that includes it.
                # Max length to print to avoid flooding logs, but enough to catch col 3017
                print_limit = 4000
                print(rough_string[:print_limit])
                if len(rough_string) > print_limit:
                    print("...")
                    print(f"(Rough string was truncated in this debug output. Total length: {len(rough_string)})")
                raise # Re-raise the original exception
        else:
            return ET.tostring(xml_root, encoding='unicode')
    
    def save_to_file(self, xml_root: ET.Element, file_path: str):
        """
        Save XML to file.
        
        Args:
            xml_root: XML root element
            file_path: Output file path
        """
        try:
            xml_string = self.to_string(xml_root)
            
            with open(file_path, 'w', encoding=self.config.xml_encoding) as f:
                f.write(f'<?xml version="{self.config.xml_version}" encoding="{self.config.xml_encoding}"?>\n')
                f.write(xml_string)
            
            self.logger.info(f"XML saved to: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving XML to {file_path}: {e}")
            raise
    
    def generate_xml_from_file(self, edifact_file_path: str, 
                              xml_file_path: str,
                              encoding: str = 'utf-8') -> bool:
        """
        Generate XML file from EDIFACT file.
        
        Args:
            edifact_file_path: Input EDIFACT file path
            xml_file_path: Output XML file path
            encoding: File encoding
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from .edifact_parser import EDIFACTParser
            
            # Parse EDIFACT file
            parser = EDIFACTParser()
            parsed_message = parser.parse_file(edifact_file_path, encoding)
            
            # Generate XML
            xml_root = self.generate_xml(parsed_message)
            
            # Save to file
            self.save_to_file(xml_root, xml_file_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting {edifact_file_path} to XML: {e}")
            return False


def generate_xml_from_parsed_message(parsed_message: ParsedMessage,
                                   config: Optional[XMLGeneratorConfig] = None) -> str:
    """
    Convenience function to generate XML string from parsed message.
    
    Args:
        parsed_message: Parsed EDIFACT message
        config: XML generation configuration
        
    Returns:
        XML string representation
    """
    generator = XMLGenerator(config)
    xml_root = generator.generate_xml(parsed_message)
    return generator.to_string(xml_root)


def convert_edifact_to_xml(edifact_content: str,
                          config: Optional[XMLGeneratorConfig] = None) -> str:
    """
    Convenience function to convert EDIFACT content to XML string.
    
    Args:
        edifact_content: Raw EDIFACT content
        config: XML generation configuration
        
    Returns:
        XML string representation
    """
    from .edifact_parser import EDIFACTParser
    
    # Parse EDIFACT content
    parser = EDIFACTParser()
    parsed_message = parser.parse_message(edifact_content)
    
    # Generate XML
    return generate_xml_from_parsed_message(parsed_message, config)

