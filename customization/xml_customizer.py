#!/usr/bin/env python3
"""
XML Customizer for EDI Customization Layer
==========================================

This module provides custom XML generation capabilities based on
user-defined templates and structures.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class XMLTemplate:
    """Represents an XML template structure"""
    name: str
    root_element: str
    namespace: Optional[str] = None
    schema_location: Optional[str] = None
    structure: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ElementDefinition:
    """Defines an XML element structure"""
    name: str
    path: str
    data_type: str = "string"
    required: bool = False
    multiple: bool = False
    attributes: Dict[str, str] = field(default_factory=dict)
    children: List['ElementDefinition'] = field(default_factory=list)
    default_value: Any = None
    validation_rules: List[str] = field(default_factory=list)


class TemplateProcessor:
    """Processes XML templates and structures"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.TemplateProcessor")
        self.templates: Dict[str, XMLTemplate] = {}
    
    def load_template(self, template: XMLTemplate):
        """Load an XML template"""
        self.templates[template.name] = template
        self.logger.info(f"Loaded template: {template.name}")
    
    def load_template_from_file(self, file_path: Union[str, Path]) -> XMLTemplate:
        """Load template from XML file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            template = XMLTemplate(
                name=Path(file_path).stem,
                root_element=root.tag,
                namespace=self._extract_namespace(root),
                attributes=dict(root.attrib),
                structure=self._analyze_structure(root)
            )
            
            self.load_template(template)
            return template
            
        except Exception as e:
            self.logger.error(f"Error loading template from {file_path}: {e}")
            raise
    
    def load_template_from_string(self, xml_string: str, template_name: str) -> XMLTemplate:
        """Load template from XML string"""
        try:
            root = ET.fromstring(xml_string)
            
            template = XMLTemplate(
                name=template_name,
                root_element=root.tag,
                namespace=self._extract_namespace(root),
                attributes=dict(root.attrib),
                structure=self._analyze_structure(root)
            )
            
            self.load_template(template)
            return template
            
        except Exception as e:
            self.logger.error(f"Error loading template from string: {e}")
            raise
    
    def get_template(self, name: str) -> Optional[XMLTemplate]:
        """Get template by name"""
        return self.templates.get(name)
    
    def create_element_definitions(self, template: XMLTemplate) -> List[ElementDefinition]:
        """Create element definitions from template structure"""
        definitions = []
        
        def process_structure(structure: Dict[str, Any], parent_path: str = ""):
            for key, value in structure.items():
                current_path = f"{parent_path}.{key}" if parent_path else key
                
                if isinstance(value, dict):
                    # Complex element with children
                    element_def = ElementDefinition(
                        name=key,
                        path=current_path,
                        data_type="complex"
                    )
                    
                    # Process children
                    process_structure(value, current_path)
                    definitions.append(element_def)
                    
                else:
                    # Simple element
                    element_def = ElementDefinition(
                        name=key,
                        path=current_path,
                        data_type="string"
                    )
                    definitions.append(element_def)
        
        process_structure(template.structure)
        return definitions
    
    def _extract_namespace(self, element: ET.Element) -> Optional[str]:
        """Extract namespace from XML element"""
        if element.tag.startswith('{'):
            return element.tag[1:element.tag.index('}')]
        return None
    
    def _analyze_structure(self, element: ET.Element, path: str = "") -> Dict[str, Any]:
        """Analyze XML structure recursively"""
        structure = {}
        
        # Process attributes
        if element.attrib:
            structure['@attributes'] = dict(element.attrib)
        
        # Process text content
        if element.text and element.text.strip():
            structure['@text'] = element.text.strip()
        
        # Process child elements
        child_counts = {}
        for child in element:
            child_name = self._clean_tag_name(child.tag)
            
            # Count occurrences for multiple elements
            child_counts[child_name] = child_counts.get(child_name, 0) + 1
            
            if child_counts[child_name] == 1:
                structure[child_name] = self._analyze_structure(child, f"{path}.{child_name}" if path else child_name)
            elif child_counts[child_name] == 2:
                # Convert to array when second occurrence found
                existing = structure[child_name]
                structure[child_name] = [existing, self._analyze_structure(child, f"{path}.{child_name}" if path else child_name)]
            else:
                # Add to existing array
                structure[child_name].append(self._analyze_structure(child, f"{path}.{child_name}" if path else child_name))
        
        return structure
    
    def _clean_tag_name(self, tag: str) -> str:
        """Clean tag name by removing namespace"""
        if '}' in tag:
            return tag.split('}')[1]
        return tag


class XMLStructureValidator:
    """Validates XML structures against templates"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.XMLStructureValidator")
    
    def validate_against_template(self, data: Dict[str, Any], template: XMLTemplate) -> Dict[str, Any]:
        """Validate data against XML template"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'missing_elements': [],
            'extra_elements': []
        }
        
        try:
            # Validate structure
            self._validate_structure(data, template.structure, "", validation_result)
            
            # Check for required elements
            self._check_required_elements(data, template.structure, validation_result)
            
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")
            validation_result['is_valid'] = False
        
        return validation_result
    
    def _validate_structure(self, data: Dict[str, Any], template_structure: Dict[str, Any], 
                           path: str, result: Dict[str, Any]):
        """Validate data structure recursively"""
        for key, template_value in template_structure.items():
            if key.startswith('@'):
                continue  # Skip metadata
            
            current_path = f"{path}.{key}" if path else key
            
            if key not in data:
                result['missing_elements'].append(current_path)
                continue
            
            data_value = data[key]
            
            if isinstance(template_value, dict):
                if isinstance(data_value, dict):
                    self._validate_structure(data_value, template_value, current_path, result)
                else:
                    result['errors'].append(f"Expected object at {current_path}, got {type(data_value)}")
                    result['is_valid'] = False
            elif isinstance(template_value, list):
                if not isinstance(data_value, list):
                    result['errors'].append(f"Expected array at {current_path}, got {type(data_value)}")
                    result['is_valid'] = False
        
        # Check for extra elements in data
        for key in data:
            if key not in template_structure and not key.startswith('_'):
                current_path = f"{path}.{key}" if path else key
                result['extra_elements'].append(current_path)
    
    def _check_required_elements(self, data: Dict[str, Any], template_structure: Dict[str, Any], 
                                result: Dict[str, Any]):
        """Check for required elements"""
        # This would be enhanced with actual required field definitions
        pass


class CustomXMLGenerator:
    """Generates custom XML based on templates and mapped data"""
    
    def __init__(self, template_processor: TemplateProcessor = None):
        self.template_processor = template_processor or TemplateProcessor()
        self.logger = logging.getLogger(f"{__name__}.CustomXMLGenerator")
    
    def generate_xml(self, data: Dict[str, Any], template_name: str, 
                    pretty_print: bool = True, encoding: str = 'UTF-8') -> str:
        """Generate XML from data using specified template"""
        try:
            template = self.template_processor.get_template(template_name)
            if not template:
                raise ValueError(f"Template not found: {template_name}")
            
            # Create root element
            root = self._create_root_element(template)
            
            # Populate XML structure
            self._populate_element(root, data, template.structure)
            
            # Convert to string
            return self._to_string(root, pretty_print, encoding)
            
        except Exception as e:
            self.logger.error(f"Error generating XML: {e}")
            raise
    
    def generate_xml_from_structure(self, data: Dict[str, Any], root_name: str = "Document",
                                   namespace: Optional[str] = None, pretty_print: bool = True,
                                   encoding: str = 'UTF-8') -> str:
        """Generate XML from data without predefined template"""
        try:
            # Create root element
            if namespace:
                root = ET.Element(f"{{{namespace}}}{root_name}")
            else:
                root = ET.Element(root_name)
            
            # Populate from data structure
            self._populate_from_data(root, data)
            
            # Convert to string
            return self._to_string(root, pretty_print, encoding)
            
        except Exception as e:
            self.logger.error(f"Error generating XML from structure: {e}")
            raise
    
    def _create_root_element(self, template: XMLTemplate) -> ET.Element:
        """Create root XML element from template"""
        if template.namespace:
            root = ET.Element(f"{{{template.namespace}}}{template.root_element}")
        else:
            root = ET.Element(template.root_element)
        
        # Add root attributes
        for attr_name, attr_value in template.attributes.items():
            root.set(attr_name, attr_value)
        
        return root
    
    def _populate_element(self, element: ET.Element, data: Dict[str, Any], 
                         structure: Dict[str, Any]):
        """Populate XML element based on template structure"""
        for key, template_value in structure.items():
            if key.startswith('@'):
                continue  # Skip metadata
            
            if key not in data:
                # Create empty element if defined in template
                if isinstance(template_value, dict):
                    child_elem = ET.SubElement(element, key)
                    self._populate_element(child_elem, {}, template_value)
                else:
                    child_elem = ET.SubElement(element, key)
                    child_elem.text = ""
                continue
            
            data_value = data[key]
            
            if isinstance(template_value, dict):
                # Complex element
                child_elem = ET.SubElement(element, key)
                if isinstance(data_value, dict):
                    self._populate_element(child_elem, data_value, template_value)
                else:
                    child_elem.text = str(data_value)
            
            elif isinstance(template_value, list):
                # Multiple elements
                if isinstance(data_value, list):
                    for item in data_value:
                        child_elem = ET.SubElement(element, key)
                        if isinstance(item, dict) and isinstance(template_value[0], dict):
                            self._populate_element(child_elem, item, template_value[0])
                        else:
                            child_elem.text = str(item)
                else:
                    child_elem = ET.SubElement(element, key)
                    child_elem.text = str(data_value)
            
            else:
                # Simple element
                child_elem = ET.SubElement(element, key)
                child_elem.text = str(data_value) if data_value is not None else ""
    
    def _populate_from_data(self, element: ET.Element, data: Dict[str, Any]):
        """Populate XML element directly from data structure"""
        for key, value in data.items():
            if key.startswith('_'):
                continue  # Skip metadata
            
            if isinstance(value, dict):
                child_elem = ET.SubElement(element, key)
                self._populate_from_data(child_elem, value)
            
            elif isinstance(value, list):
                for item in value:
                    child_elem = ET.SubElement(element, key)
                    if isinstance(item, dict):
                        self._populate_from_data(child_elem, item)
                    else:
                        child_elem.text = str(item) if item is not None else ""
            
            else:
                child_elem = ET.SubElement(element, key)
                child_elem.text = str(value) if value is not None else ""
    
    def _to_string(self, root: ET.Element, pretty_print: bool, encoding: str) -> str:
        """Convert XML element to string"""
        if pretty_print:
            # Use minidom for pretty printing
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ", encoding=encoding).decode(encoding)
        else:
            return ET.tostring(root, encoding=encoding).decode(encoding)
    
    def create_template_from_data(self, data: Dict[str, Any], template_name: str,
                                 root_element: str = "Document") -> XMLTemplate:
        """Create template from data structure"""
        structure = self._analyze_data_structure(data)
        
        template = XMLTemplate(
            name=template_name,
            root_element=root_element,
            structure=structure
        )
        
        self.template_processor.load_template(template)
        return template
    
    def _analyze_data_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data structure to create template"""
        structure = {}
        
        for key, value in data.items():
            if key.startswith('_'):
                continue
            
            if isinstance(value, dict):
                structure[key] = self._analyze_data_structure(value)
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    structure[key] = [self._analyze_data_structure(value[0])]
                else:
                    structure[key] = ["string"]
            else:
                structure[key] = "string"
        
        return structure


# Convenience functions
def create_simple_template(name: str, root_element: str, structure: Dict[str, Any]) -> XMLTemplate:
    """Create a simple XML template"""
    return XMLTemplate(
        name=name,
        root_element=root_element,
        structure=structure
    )


def generate_xml_from_template(data: Dict[str, Any], template: XMLTemplate, 
                              pretty_print: bool = True) -> str:
    """Generate XML from data and template"""
    generator = CustomXMLGenerator()
    generator.template_processor.load_template(template)
    return generator.generate_xml(data, template.name, pretty_print)


# Predefined templates for common document types
def create_purchase_order_template() -> XMLTemplate:
    """Create a standard purchase order XML template"""
    structure = {
        "Header": {
            "OrderNumber": "string",
            "OrderDate": "string",
            "DeliveryDate": "string",
            "Currency": "string"
        },
        "Parties": {
            "Buyer": {
                "ID": "string",
                "Name": "string",
                "Address": {
                    "Street": "string",
                    "City": "string",
                    "PostalCode": "string",
                    "Country": "string"
                }
            },
            "Supplier": {
                "ID": "string",
                "Name": "string",
                "Address": {
                    "Street": "string",
                    "City": "string",
                    "PostalCode": "string",
                    "Country": "string"
                }
            }
        },
        "LineItems": {
            "LineItem": [{
                "LineNumber": "string",
                "ItemID": "string",
                "Description": "string",
                "Quantity": "string",
                "UnitPrice": "string",
                "TotalAmount": "string"
            }]
        },
        "Summary": {
            "TotalLines": "string",
            "TotalAmount": "string",
            "TaxAmount": "string",
            "GrandTotal": "string"
        }
    }
    
    return XMLTemplate(
        name="PurchaseOrder",
        root_element="PurchaseOrder",
        structure=structure,
        attributes={
            "version": "1.0",
            "xmlns": "http://example.com/purchaseorder"
        }
    )


def create_invoice_template() -> XMLTemplate:
    """Create a standard invoice XML template"""
    structure = {
        "Header": {
            "InvoiceNumber": "string",
            "InvoiceDate": "string",
            "DueDate": "string",
            "Currency": "string",
            "OrderReference": "string"
        },
        "Parties": {
            "Supplier": {
                "ID": "string",
                "Name": "string",
                "Address": {
                    "Street": "string",
                    "City": "string",
                    "PostalCode": "string",
                    "Country": "string"
                }
            },
            "Customer": {
                "ID": "string",
                "Name": "string",
                "Address": {
                    "Street": "string",
                    "City": "string",
                    "PostalCode": "string",
                    "Country": "string"
                }
            }
        },
        "LineItems": {
            "LineItem": [{
                "LineNumber": "string",
                "ItemID": "string",
                "Description": "string",
                "Quantity": "string",
                "UnitPrice": "string",
                "TaxRate": "string",
                "TaxAmount": "string",
                "TotalAmount": "string"
            }]
        },
        "Summary": {
            "SubTotal": "string",
            "TotalTax": "string",
            "TotalAmount": "string"
        }
    }
    
    return XMLTemplate(
        name="Invoice",
        root_element="Invoice",
        structure=structure,
        attributes={
            "version": "1.0",
            "xmlns": "http://example.com/invoice"
        }
    )

