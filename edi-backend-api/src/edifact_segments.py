#!/usr/bin/env python3
"""
EDIFACT Segments Module
======================

This module contains complete EDIFACT segment definitions with all elements,
components, and their properties according to UN/EDIFACT standards.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from .edifact_elements import DataElementDefinition, DataElementType, DataElementStatus
from .edifact_qualifiers import EDIFACTQualifiers


class SegmentStatus(Enum):
    """EDIFACT segment status"""
    MANDATORY = "M"
    CONDITIONAL = "C"
    OPTIONAL = "O"


class SegmentGroup(Enum):
    """EDIFACT segment groups"""
    SERVICE = "service"
    HEADER = "header"
    DETAIL = "detail"
    SUMMARY = "summary"


@dataclass
class ComponentDefinition:
    """Definition of a component within a composite element"""
    position: int
    name: str
    element_id: str
    data_type: DataElementType
    min_length: int
    max_length: int
    status: DataElementStatus = DataElementStatus.CONDITIONAL
    format_pattern: Optional[str] = None
    code_list: Optional[List[str]] = None


@dataclass
class ElementDefinition:
    """Definition of an element within a segment"""
    position: int
    name: str
    element_id: str
    data_type: DataElementType
    min_length: int
    max_length: int
    status: DataElementStatus = DataElementStatus.CONDITIONAL
    is_composite: bool = False
    components: List[ComponentDefinition] = field(default_factory=list)
    format_pattern: Optional[str] = None
    code_list: Optional[List[str]] = None


@dataclass
class SegmentDefinition:
    """Complete definition of an EDIFACT segment"""
    tag: str
    name: str
    description: str
    group: SegmentGroup
    status: SegmentStatus = SegmentStatus.OPTIONAL
    max_occurrences: int = 1
    elements: List[ElementDefinition] = field(default_factory=list)
    usage_notes: Optional[str] = None
    version_added: Optional[str] = None


class EDIFACTSegments:
    """
    Complete EDIFACT segment definitions.
    
    Contains all standard UN/EDIFACT segments with their complete element
    and component definitions.
    """
    
    SEGMENTS = {
        # SERVICE SEGMENTS
        "UNA": SegmentDefinition(
            tag="UNA",
            name="Service String Advice",
            description="Defines syntax characters used in interchange",
            group=SegmentGroup.SERVICE,
            status=SegmentStatus.OPTIONAL,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Component Data Element Separator",
                    element_id="UNA01",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=2,
                    name="Data Element Separator",
                    element_id="UNA02",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=3,
                    name="Decimal Notation",
                    element_id="UNA03",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=4,
                    name="Escape Character",
                    element_id="UNA04",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=5,
                    name="Reserved for Future Use",
                    element_id="UNA05",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=6,
                    name="Segment Terminator",
                    element_id="UNA06",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.MANDATORY
                )
            ]
        ),
        
        "UNB": SegmentDefinition(
            tag="UNB",
            name="Interchange Header",
            description="Interchange control header",
            group=SegmentGroup.SERVICE,
            status=SegmentStatus.MANDATORY,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Syntax Identifier",
                    element_id="S001",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=4,
                    max_length=7,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Syntax Identifier",
                            element_id="0001",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=4,
                            max_length=4,
                            status=DataElementStatus.MANDATORY,
                            code_list=["UNOA", "UNOB", "UNOC", "UNOD", "UNOE", "UNOF"]
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Syntax Version Number",
                            element_id="0002",
                            data_type=DataElementType.NUMERIC,
                            min_length=1,
                            max_length=1,
                            status=DataElementStatus.MANDATORY,
                            code_list=["1", "2", "3", "4"]
                        )
                    ]
                ),
                ElementDefinition(
                    position=2,
                    name="Interchange Sender",
                    element_id="S002",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Sender Identification",
                            element_id="0004",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Partner Identification Code Qualifier",
                            element_id="0007",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=4,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Address for Reverse Routing",
                            element_id="0008",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=14,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=3,
                    name="Interchange Recipient",
                    element_id="S003",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Recipient Identification",
                            element_id="0010",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Partner Identification Code Qualifier",
                            element_id="0007",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=4,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Routing Address",
                            element_id="0014",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=14,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=4,
                    name="Date/Time of Preparation",
                    element_id="S004",
                    data_type=DataElementType.NUMERIC,
                    min_length=6,
                    max_length=12,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Date of Preparation",
                            element_id="0017",
                            data_type=DataElementType.NUMERIC,
                            min_length=6,
                            max_length=8,
                            status=DataElementStatus.MANDATORY,
                            format_pattern=r"^\d{6}(\d{2})?$"
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Time of Preparation",
                            element_id="0019",
                            data_type=DataElementType.NUMERIC,
                            min_length=4,
                            max_length=6,
                            status=DataElementStatus.CONDITIONAL,
                            format_pattern=r"^\d{4}(\d{2})?$"
                        )
                    ]
                ),
                ElementDefinition(
                    position=5,
                    name="Interchange Control Reference",
                    element_id="0020",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=6,
                    name="Recipients Reference Password",
                    element_id="S005",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Recipients Reference Password",
                            element_id="0022",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=14,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Recipients Reference Password Qualifier",
                            element_id="0025",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=2,
                            max_length=2,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=7,
                    name="Application Reference",
                    element_id="0026",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=8,
                    name="Processing Priority Code",
                    element_id="0029",
                    data_type=DataElementType.ALPHABETIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.CONDITIONAL,
                    code_list=["A"]
                ),
                ElementDefinition(
                    position=9,
                    name="Acknowledgement Request",
                    element_id="0031",
                    data_type=DataElementType.NUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.CONDITIONAL,
                    code_list=["1"]
                ),
                ElementDefinition(
                    position=10,
                    name="Communications Agreement Id",
                    element_id="0032",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=11,
                    name="Test Indicator",
                    element_id="0035",
                    data_type=DataElementType.NUMERIC,
                    min_length=1,
                    max_length=1,
                    status=DataElementStatus.CONDITIONAL,
                    code_list=["1"]
                )
            ]
        ),
        
        "UNH": SegmentDefinition(
            tag="UNH",
            name="Message Header",
            description="Message header identifying message type and version",
            group=SegmentGroup.SERVICE,
            status=SegmentStatus.MANDATORY,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Message Reference Number",
                    element_id="0062",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=2,
                    name="Message Identifier",
                    element_id="S009",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Message Type",
                            element_id="0065",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=6,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Message Version Number",
                            element_id="0052",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Message Release Number",
                            element_id="0054",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Controlling Agency",
                            element_id="0051",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY,
                            code_list=["UN"]
                        ),
                        ComponentDefinition(
                            position=5,
                            name="Association Assigned Code",
                            element_id="0057",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=6,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=6,
                            name="Code List Directory Version Number",
                            element_id="0110",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=6,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=7,
                            name="Message Type Sub-function Identification",
                            element_id="0113",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=6,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=3,
                    name="Common Access Reference",
                    element_id="0068",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=4,
                    name="Status of the Transfer",
                    element_id="S010",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=3,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Sequence of Transfers",
                            element_id="0070",
                            data_type=DataElementType.NUMERIC,
                            min_length=1,
                            max_length=2,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="First and Last Transfer",
                            element_id="0073",
                            data_type=DataElementType.ALPHABETIC,
                            min_length=1,
                            max_length=1,
                            status=DataElementStatus.CONDITIONAL,
                            code_list=["F", "L", "C"]
                        )
                    ]
                )
            ]
        ),
        
        # BUSINESS SEGMENTS
        "BGM": SegmentDefinition(
            tag="BGM",
            name="Beginning of Message",
            description="Beginning of message - identifies document type",
            group=SegmentGroup.HEADER,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Document/Message Name",
                    element_id="C002",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Document/Message Name, Coded",
                            element_id="1001",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Code List Qualifier",
                            element_id="1131",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Code List Responsible Agency, Coded",
                            element_id="3055",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Document/Message Name",
                            element_id="1000",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=2,
                    name="Document/Message Identification",
                    element_id="1004",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=3,
                    name="Message Function, Coded",
                    element_id="1225",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=3,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=4,
                    name="Response Type, Coded",
                    element_id="4343",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=3,
                    status=DataElementStatus.CONDITIONAL
                )
            ]
        ),
        
        "DTM": SegmentDefinition(
            tag="DTM",
            name="Date/Time/Period",
            description="Date/time/period information",
            group=SegmentGroup.HEADER,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=99,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Date/Time/Period",
                    element_id="C507",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Date/Time/Period Qualifier",
                            element_id="2005",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Date/Time/Period",
                            element_id="2380",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Date/Time/Period Format Qualifier",
                            element_id="2379",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        "RFF": SegmentDefinition(
            tag="RFF",
            name="Reference",
            description="Reference identification",
            group=SegmentGroup.HEADER,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=99,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Reference",
                    element_id="C506",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=70,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Reference Qualifier",
                            element_id="1153",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Reference Number",
                            element_id="1154",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=70,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Line Number",
                            element_id="1156",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=6,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Reference Version Number",
                            element_id="4000",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        "NAD": SegmentDefinition(
            tag="NAD",
            name="Name and Address",
            description="Name and address information",
            group=SegmentGroup.HEADER,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=99,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Party Qualifier",
                    element_id="3035",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=3,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=2,
                    name="Party Identification Details",
                    element_id="C082",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Party Id. Identification",
                            element_id="3039",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Code List Qualifier",
                            element_id="1131",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Code List Responsible Agency, Coded",
                            element_id="3055",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=3,
                    name="Name and Address",
                    element_id="C058",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Name and Address Line",
                            element_id="3124",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Name and Address Line",
                            element_id="3124",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Name and Address Line",
                            element_id="3124",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Name and Address Line",
                            element_id="3124",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=5,
                            name="Name and Address Line",
                            element_id="3124",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                ),
                ElementDefinition(
                    position=4,
                    name="Party Name",
                    element_id="C080",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Party Name",
                            element_id="3036",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Party Name",
                            element_id="3036",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Party Name",
                            element_id="3036",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Party Name",
                            element_id="3036",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=5,
                            name="Party Name Format, Coded",
                            element_id="3045",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        # Add more segments as needed...
        "LIN": SegmentDefinition(
            tag="LIN",
            name="Line Item",
            description="Line item identification",
            group=SegmentGroup.DETAIL,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=9999,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Line Item Number",
                    element_id="1082",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=6,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=2,
                    name="Action Request/Notification, Coded",
                    element_id="1229",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=3,
                    status=DataElementStatus.CONDITIONAL
                ),
                ElementDefinition(
                    position=3,
                    name="Item Number Identification",
                    element_id="C212",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Item Number",
                            element_id="7140",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Item Number Type, Coded",
                            element_id="7143",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Code List Qualifier",
                            element_id="1131",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Code List Responsible Agency, Coded",
                            element_id="3055",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        "QTY": SegmentDefinition(
            tag="QTY",
            name="Quantity",
            description="Quantity information",
            group=SegmentGroup.DETAIL,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=99,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Quantity Details",
                    element_id="C186",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=35,
                    status=DataElementStatus.MANDATORY,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Quantity Qualifier",
                            element_id="6063",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Quantity",
                            element_id="6060",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=35,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Measure Unit Qualifier",
                            element_id="6411",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        "PRI": SegmentDefinition(
            tag="PRI",
            name="Price Details",
            description="Price information",
            group=SegmentGroup.DETAIL,
            status=SegmentStatus.CONDITIONAL,
            max_occurrences=25,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Price Information",
                    element_id="C509",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=15,
                    status=DataElementStatus.CONDITIONAL,
                    is_composite=True,
                    components=[
                        ComponentDefinition(
                            position=1,
                            name="Price Qualifier",
                            element_id="5125",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.MANDATORY
                        ),
                        ComponentDefinition(
                            position=2,
                            name="Price",
                            element_id="5118",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=15,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=3,
                            name="Price Type, Coded",
                            element_id="5375",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=4,
                            name="Price Type Qualifier",
                            element_id="5387",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=5,
                            name="Unit Price Basis",
                            element_id="5284",
                            data_type=DataElementType.NUMERIC,
                            min_length=1,
                            max_length=9,
                            status=DataElementStatus.CONDITIONAL
                        ),
                        ComponentDefinition(
                            position=6,
                            name="Measure Unit Qualifier",
                            element_id="6411",
                            data_type=DataElementType.ALPHANUMERIC,
                            min_length=1,
                            max_length=3,
                            status=DataElementStatus.CONDITIONAL
                        )
                    ]
                )
            ]
        ),
        
        # Service trailer segments
        "UNT": SegmentDefinition(
            tag="UNT",
            name="Message Trailer",
            description="Message trailer",
            group=SegmentGroup.SERVICE,
            status=SegmentStatus.MANDATORY,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Number of Segments in the Message",
                    element_id="0074",
                    data_type=DataElementType.NUMERIC,
                    min_length=1,
                    max_length=6,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=2,
                    name="Message Reference Number",
                    element_id="0062",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.MANDATORY
                )
            ]
        ),
        
        "UNZ": SegmentDefinition(
            tag="UNZ",
            name="Interchange Trailer",
            description="Interchange trailer",
            group=SegmentGroup.SERVICE,
            status=SegmentStatus.MANDATORY,
            max_occurrences=1,
            elements=[
                ElementDefinition(
                    position=1,
                    name="Interchange Control Count",
                    element_id="0036",
                    data_type=DataElementType.NUMERIC,
                    min_length=1,
                    max_length=6,
                    status=DataElementStatus.MANDATORY
                ),
                ElementDefinition(
                    position=2,
                    name="Interchange Control Reference",
                    element_id="0020",
                    data_type=DataElementType.ALPHANUMERIC,
                    min_length=1,
                    max_length=14,
                    status=DataElementStatus.MANDATORY
                )
            ]
        )
    }
    
    @classmethod
    def get_segment(cls, tag: str) -> Optional[SegmentDefinition]:
        """
        Get segment definition by tag.
        
        Args:
            tag: Segment tag (e.g., "UNH")
            
        Returns:
            SegmentDefinition if found, None otherwise
        """
        return cls.SEGMENTS.get(tag.upper())
    
    @classmethod
    def get_all_segments(cls) -> Dict[str, SegmentDefinition]:
        """Get all segment definitions."""
        return cls.SEGMENTS.copy()
    
    @classmethod
    def get_segments_by_group(cls, group: SegmentGroup) -> List[SegmentDefinition]:
        """
        Get all segments belonging to a specific group.
        
        Args:
            group: Segment group
            
        Returns:
            List of segment definitions
        """
        return [seg for seg in cls.SEGMENTS.values() if seg.group == group]
    
    @classmethod
    def get_mandatory_segments(cls) -> List[SegmentDefinition]:
        """Get all mandatory segments."""
        return [seg for seg in cls.SEGMENTS.values() if seg.status == SegmentStatus.MANDATORY]
    
    @classmethod
    def validate_segment_structure(cls, tag: str, elements: List[str]) -> List[str]:
        """
        Validate segment structure against definition.
        
        Args:
            tag: Segment tag
            elements: List of element values
            
        Returns:
            List of validation errors
        """
        errors = []
        segment_def = cls.get_segment(tag)
        
        if not segment_def:
            errors.append(f"Unknown segment: {tag}")
            return errors
        
        # Check mandatory elements
        for i, element_def in enumerate(segment_def.elements):
            if element_def.status == DataElementStatus.MANDATORY:
                if i >= len(elements) or not elements[i]:
                    errors.append(f"Missing mandatory element {element_def.position} in segment {tag}")
        
        # Check element count
        if len(elements) > len(segment_def.elements):
            errors.append(f"Too many elements in segment {tag}: expected max {len(segment_def.elements)}, got {len(elements)}")
        
        return errors

