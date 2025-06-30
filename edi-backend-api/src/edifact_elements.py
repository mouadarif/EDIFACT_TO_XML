#!/usr/bin/env python3
"""
EDIFACT Elements Module
======================

This module defines all EDIFACT data elements with their properties,
validation rules, and formatting specifications according to UN/EDIFACT standards.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Union, Any
from enum import Enum
from dataclasses import dataclass
import re


class DataElementType(Enum):
    """EDIFACT data element types"""
    ALPHABETIC = "a"           # Alphabetic characters only
    NUMERIC = "n"              # Numeric characters only
    ALPHANUMERIC = "an"        # Alphanumeric characters
    VARIABLE = "var"           # Variable format
    BINARY = "b"               # Binary data


class DataElementStatus(Enum):
    """EDIFACT data element status"""
    MANDATORY = "M"            # Mandatory element
    CONDITIONAL = "C"          # Conditional element
    DEPENDENT = "D"            # Dependent element


@dataclass
class DataElementDefinition:
    """
    Complete definition of an EDIFACT data element.
    """
    element_id: str
    name: str
    description: str
    element_type: DataElementType
    min_length: int
    max_length: int
    status: DataElementStatus = DataElementStatus.CONDITIONAL
    format_pattern: Optional[str] = None
    code_list: Optional[List[str]] = None
    representation: Optional[str] = None
    
    def validate(self, value: str) -> bool:
        """
        Validate a value against this element definition.
        
        Args:
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not value and self.status == DataElementStatus.MANDATORY:
            return False
            
        if not value:
            return True  # Empty values allowed for non-mandatory elements
            
        # Check length
        if len(value) < self.min_length or len(value) > self.max_length:
            return False
            
        # Check type
        if self.element_type == DataElementType.ALPHABETIC:
            if not value.isalpha():
                return False
        elif self.element_type == DataElementType.NUMERIC:
            if not value.isdigit():
                return False
        elif self.element_type == DataElementType.ALPHANUMERIC:
            if not value.isalnum():
                return False
                
        # Check format pattern
        if self.format_pattern:
            if not re.match(self.format_pattern, value):
                return False
                
        # Check code list
        if self.code_list and value not in self.code_list:
            return False
            
        return True


class EDIFACTElements:
    """
    Complete EDIFACT data element definitions.
    
    Contains all standard UN/EDIFACT data elements with their properties,
    validation rules, and code lists.
    """
    
    # Service elements (0001-0099)
    ELEMENTS = {
        "0001": DataElementDefinition(
            element_id="0001",
            name="Syntax identifier",
            description="Coded identification of the syntax",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=4,
            max_length=4,
            status=DataElementStatus.MANDATORY,
            code_list=["UNOA", "UNOB", "UNOC", "UNOD", "UNOE", "UNOF", "UNOG", "UNOH", "UNOI", "UNOJ", "UNOK", "UNOL", "UNOM", "UNON", "UNOO", "UNOP"]
        ),
        
        "0002": DataElementDefinition(
            element_id="0002",
            name="Syntax version number",
            description="Version number of the syntax",
            element_type=DataElementType.NUMERIC,
            min_length=1,
            max_length=1,
            status=DataElementStatus.MANDATORY,
            code_list=["1", "2", "3", "4", "5"]
        ),
        
        "0004": DataElementDefinition(
            element_id="0004",
            name="Sender identification",
            description="Name or coded identification of the sender",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35,
            status=DataElementStatus.MANDATORY
        ),
        
        "0007": DataElementDefinition(
            element_id="0007",
            name="Partner identification code qualifier",
            description="Qualifier for partner identification code",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=4,
            code_list=["1", "4", "5", "8", "9", "12", "14", "18", "22", "30", "31", "33", "34", "51", "52", "53", "54", "55", "57", "58", "59", "61", "63", "65", "80", "82", "84", "85", "86", "87", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "ZZZ"]
        ),
        
        "0008": DataElementDefinition(
            element_id="0008",
            name="Address for reverse routing",
            description="Address specified by the sender for routing back",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14
        ),
        
        "0010": DataElementDefinition(
            element_id="0010",
            name="Recipient identification",
            description="Name or coded identification of the recipient",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35,
            status=DataElementStatus.MANDATORY
        ),
        
        "0014": DataElementDefinition(
            element_id="0014",
            name="Routing address",
            description="Address specified by the recipient for routing",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14
        ),
        
        "0017": DataElementDefinition(
            element_id="0017",
            name="Date of preparation",
            description="Local date when interchange was prepared",
            element_type=DataElementType.NUMERIC,
            min_length=6,
            max_length=8,
            status=DataElementStatus.MANDATORY,
            format_pattern=r"^\d{6}(\d{2})?$"  # YYMMDD or CCYYMMDD
        ),
        
        "0019": DataElementDefinition(
            element_id="0019",
            name="Time of preparation",
            description="Local time when interchange was prepared",
            element_type=DataElementType.NUMERIC,
            min_length=4,
            max_length=6,
            format_pattern=r"^\d{4}(\d{2})?$"  # HHMM or HHMMSS
        ),
        
        "0020": DataElementDefinition(
            element_id="0020",
            name="Interchange control reference",
            description="Unique reference assigned by sender",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14,
            status=DataElementStatus.MANDATORY
        ),
        
        "0022": DataElementDefinition(
            element_id="0022",
            name="Recipient's reference/password",
            description="Reference or password as agreed between partners",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14
        ),
        
        "0025": DataElementDefinition(
            element_id="0025",
            name="Recipient's reference/password qualifier",
            description="Qualifier for recipient's reference/password",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=2,
            max_length=2,
            code_list=["AA", "BB", "CC"]
        ),
        
        "0026": DataElementDefinition(
            element_id="0026",
            name="Application reference",
            description="Identification of the application area",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14
        ),
        
        "0029": DataElementDefinition(
            element_id="0029",
            name="Processing priority code",
            description="Code determining processing priority",
            element_type=DataElementType.ALPHABETIC,
            min_length=1,
            max_length=1,
            code_list=["A"]
        ),
        
        "0031": DataElementDefinition(
            element_id="0031",
            name="Acknowledgement request",
            description="Code indicating acknowledgement is requested",
            element_type=DataElementType.NUMERIC,
            min_length=1,
            max_length=1,
            code_list=["1"]
        ),
        
        "0032": DataElementDefinition(
            element_id="0032",
            name="Communications agreement id",
            description="Identification of communications agreement",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "0035": DataElementDefinition(
            element_id="0035",
            name="Test indicator",
            description="Indication that interchange is test data",
            element_type=DataElementType.NUMERIC,
            min_length=1,
            max_length=1,
            code_list=["1"]
        ),
        
        # Message elements (0051-0099)
        "0051": DataElementDefinition(
            element_id="0051",
            name="Message reference number",
            description="Unique message reference assigned by sender",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=14,
            status=DataElementStatus.MANDATORY
        ),
        
        "0052": DataElementDefinition(
            element_id="0052",
            name="Message type identifier",
            description="Code identifying message type",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=6,
            status=DataElementStatus.MANDATORY
        ),
        
        "0054": DataElementDefinition(
            element_id="0054",
            name="Message version number",
            description="Version number of message type",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3,
            status=DataElementStatus.MANDATORY
        ),
        
        "0057": DataElementDefinition(
            element_id="0057",
            name="Message release number",
            description="Release number within version",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3,
            status=DataElementStatus.MANDATORY
        ),
        
        "0058": DataElementDefinition(
            element_id="0058",
            name="Controlling agency",
            description="Code identifying controlling agency",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3,
            status=DataElementStatus.MANDATORY,
            code_list=["UN", "UNH"]
        ),
        
        "0068": DataElementDefinition(
            element_id="0068",
            name="Common access reference",
            description="Reference serving as key to relate messages",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "0070": DataElementDefinition(
            element_id="0070",
            name="Sequence of transfers",
            description="Current sequence number of transfer",
            element_type=DataElementType.NUMERIC,
            min_length=1,
            max_length=2
        ),
        
        "0073": DataElementDefinition(
            element_id="0073",
            name="First and last transfer",
            description="Indication of first and/or last transfer",
            element_type=DataElementType.ALPHABETIC,
            min_length=1,
            max_length=1,
            code_list=["F", "L", "C"]
        ),
        
        # Business elements (1000+)
        "1001": DataElementDefinition(
            element_id="1001",
            name="Document/message name, coded",
            description="Document/message identifier expressed in code",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "1004": DataElementDefinition(
            element_id="1004",
            name="Document/message number",
            description="Reference number assigned to document/message",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "1225": DataElementDefinition(
            element_id="1225",
            name="Message function, coded",
            description="Code indicating function of message",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "1373": DataElementDefinition(
            element_id="1373",
            name="Document/message status, coded",
            description="Code indicating status of document/message",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "2005": DataElementDefinition(
            element_id="2005",
            name="Date/time/period qualifier",
            description="Code giving specific meaning to date/time/period",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "2380": DataElementDefinition(
            element_id="2380",
            name="Date/time/period",
            description="Date and/or time, or period relevant to the specified date/time/period type",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "2379": DataElementDefinition(
            element_id="2379",
            name="Date/time/period format qualifier",
            description="Specification of the representation of the date/time/period",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "3035": DataElementDefinition(
            element_id="3035",
            name="Party qualifier",
            description="Code giving specific meaning to a party",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "3039": DataElementDefinition(
            element_id="3039",
            name="Party id. identification",
            description="Code identifying a party",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "1131": DataElementDefinition(
            element_id="1131",
            name="Code list qualifier",
            description="Identification of a code list",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "3055": DataElementDefinition(
            element_id="3055",
            name="Code list responsible agency, coded",
            description="Code identifying the agency responsible for a code list",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "6060": DataElementDefinition(
            element_id="6060",
            name="Quantity",
            description="Alphanumeric representation of a quantity",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "6411": DataElementDefinition(
            element_id="6411",
            name="Measure unit qualifier",
            description="Code specifying the unit of measurement",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "5025": DataElementDefinition(
            element_id="5025",
            name="Monetary amount",
            description="Number of monetary units",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "6345": DataElementDefinition(
            element_id="6345",
            name="Currency, coded",
            description="Code specifying a currency",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=3,
            max_length=3
        ),
        
        "5189": DataElementDefinition(
            element_id="5189",
            name="Price amount",
            description="Amount of a price",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=15
        ),
        
        "5125": DataElementDefinition(
            element_id="5125",
            name="Price qualifier",
            description="Code identifying pricing specification",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "7143": DataElementDefinition(
            element_id="7143",
            name="Item number",
            description="A number allocated to a group or item",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=35
        ),
        
        "7140": DataElementDefinition(
            element_id="7140",
            name="Item number type, coded",
            description="Code indicating the type of item number",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "4451": DataElementDefinition(
            element_id="4451",
            name="Text literal",
            description="Free form text",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=512
        ),
        
        "4453": DataElementDefinition(
            element_id="4453",
            name="Text subject qualifier",
            description="Code giving specific meaning to text",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "1153": DataElementDefinition(
            element_id="1153",
            name="Reference qualifier",
            description="Code giving specific meaning to a reference segment or a reference number",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=3
        ),
        
        "1154": DataElementDefinition(
            element_id="1154",
            name="Reference number",
            description="Identification number the reference of which is identified in the previous data element",
            element_type=DataElementType.ALPHANUMERIC,
            min_length=1,
            max_length=70
        ),
    }
    
    @classmethod
    def get_element(cls, element_id: str) -> Optional[DataElementDefinition]:
        """
        Get data element definition by ID.
        
        Args:
            element_id: Element ID (e.g., "0001")
            
        Returns:
            DataElementDefinition if found, None otherwise
        """
        return cls.ELEMENTS.get(element_id)
    
    @classmethod
    def validate_element(cls, element_id: str, value: str) -> bool:
        """
        Validate a value against an element definition.
        
        Args:
            element_id: Element ID
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        element = cls.get_element(element_id)
        if not element:
            return False
        return element.validate(value)
    
    @classmethod
    def get_all_elements(cls) -> Dict[str, DataElementDefinition]:
        """Get all element definitions."""
        return cls.ELEMENTS.copy()
    
    @classmethod
    def search_elements(cls, name_pattern: str) -> List[DataElementDefinition]:
        """
        Search elements by name pattern.
        
        Args:
            name_pattern: Pattern to search for in element names
            
        Returns:
            List of matching elements
        """
        pattern = re.compile(name_pattern, re.IGNORECASE)
        return [elem for elem in cls.ELEMENTS.values() 
                if pattern.search(elem.name) or pattern.search(elem.description)]


# Common element groups for convenience
SERVICE_ELEMENTS = ["0001", "0002", "0004", "0007", "0008", "0010", "0014", 
                   "0017", "0019", "0020", "0022", "0025", "0026", "0029", 
                   "0031", "0032", "0035"]

MESSAGE_ELEMENTS = ["0051", "0052", "0054", "0057", "0058", "0068", "0070", "0073"]

BUSINESS_ELEMENTS = ["1001", "1004", "1225", "1373", "2005", "2380", "2379", 
                    "3035", "3039", "1131", "3055", "6060", "6411", "5025", 
                    "6345", "5189", "5125", "7143", "7140", "4451", "4453", 
                    "1153", "1154"]

