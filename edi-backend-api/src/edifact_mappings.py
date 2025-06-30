#!/usr/bin/env python3
"""
EDIFACT Mappings Module
======================

This module provides semantic mappings between EDIFACT segments/qualifiers
and meaningful XML element names for better readability and processing.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from .edifact_qualifiers import EDIFACTQualifiers


class MappingContext(Enum):
    """Context for semantic mappings"""
    HEADER = "header"
    DETAIL = "detail"
    SUMMARY = "summary"
    SERVICE = "service"


class EDIFACTMappings:
    """
    Comprehensive semantic mappings for EDIFACT elements.
    
    Maps EDIFACT segments and qualifiers to meaningful XML element names
    based on business context and UN/EDIFACT standards.
    """
    
    # Core service segment mappings
    SERVICE_MAPPINGS = {
        "UNA": {
            None: "ServiceStringAdvice",
            "description": "Service string advice defining syntax characters"
        },
        "UNB": {
            None: "InterchangeHeader",
            "description": "Interchange control header"
        },
        "UNH": {
            None: "MessageHeader", 
            "description": "Message header with identification"
        },
        "UNT": {
            None: "MessageTrailer",
            "description": "Message trailer with control totals"
        },
        "UNZ": {
            None: "InterchangeTrailer",
            "description": "Interchange trailer with control totals"
        },
        "UNS": {
            None: "SectionControl",
            "description": "Section control separator"
        }
    }
    
    # Business document segment mappings
    BUSINESS_MAPPINGS = {
        "BGM": {
            None: "BeginningOfMessage",
            "description": "Document type and identification"
        },
        "RFF": {
            "ON": "OrderReference",
            "DQ": "DeliveryNoteReference", 
            "IV": "InvoiceReference",
            "PD": "PromotionDealReference",
            "CR": "CustomerReference",
            "VN": "VendorReference",
            "CT": "ContractReference",
            "AAA": "GeneralReference",
            None: "Reference"
        },
        "DTM": {
            "137": "DocumentDate",
            "2": "DeliveryDate",
            "63": "ExpiryDate",
            "36": "ExpiryDateTime",
            "171": "ReferenceDate",
            "273": "ValidityDate",
            "35": "DeliveryDateTime",
            "4": "OrderDate",
            "3": "InvoiceDate",
            "7": "EffectiveDate",
            "10": "ShipmentDate",
            "11": "DespatchDate",
            "140": "PaymentDueDate",
            "200": "PickupDate",
            None: "DateTime"
        },
        "FTX": {
            "GEN": "GeneralText",
            "DEL": "DeliveryText",
            "AAI": "GeneralInformation",
            "PMT": "PaymentTermsText",
            "TXD": "TaxDeclarationText",
            "REG": "RegulatoryText",
            None: "FreeText"
        }
    }
    
    # Party identification mappings
    PARTY_MAPPINGS = {
        "NAD": {
            "MS": "MessageSender",
            "MR": "MessageRecipient", 
            "BY": "BuyerParty",
            "SU": "SupplierParty",
            "IV": "InvoiceParty",
            "DP": "DeliveryParty",
            "UC": "UltimateConsignee",
            "CN": "Consignee",
            "CA": "Carrier",
            "AG": "Agent",
            "FR": "MessageFrom",
            "TO": "MessageTo",
            "OB": "OrderedBy",
            "PD": "Purchaser",
            "PE": "Payee",
            "PR": "Payer",
            "RE": "RemitTo",
            "SH": "Shipper",
            "WH": "Warehouse",
            None: "PartyIdentification"
        },
        "CTA": {
            "IC": "InformationContact",
            "OC": "OrderContact",
            "PD": "PurchasingContact",
            "SA": "SalesContact",
            "SU": "SupplierContact",
            None: "ContactInformation"
        },
        "COM": {
            "TE": "Telephone",
            "FX": "Fax",
            "EM": "Email",
            "UR": "Website",
            "TL": "Telex",
            None: "CommunicationContact"
        }
    }
    
    # Monetary and currency mappings
    MONETARY_MAPPINGS = {
        "CUX": {
            "2": "ReferenceCurrency",
            "3": "TargetCurrency",
            None: "Currency"
        },
        "MOA": {
            "79": "TotalAmount",
            "125": "TaxableAmount",
            "124": "TaxAmount",
            "128": "TotalAmountIncludingTax",
            "176": "MessageTotal",
            "203": "LineItemAmount",
            "204": "LineItemAmountIncludingTax",
            None: "MonetaryAmount"
        },
        "RTE": {
            "1": "ExchangeRate",
            None: "RateDetails"
        }
    }
    
    # Product/item mappings
    PRODUCT_MAPPINGS = {
        "LIN": {
            None: "LineItem"
        },
        "PIA": {
            "1": "AdditionalProductId",
            "5": "ProductIdentification",
            None: "ProductIdentification"
        },
        "IMD": {
            "E": "ProductDescription",
            "F": "ProductDescriptionFreeText",
            "A": "ProductDescriptionCoded",
            None: "ItemDescription"
        },
        "MEA": {
            "PD": "PhysicalDimensions",
            "AAE": "Measurement",
            "WT": "Weight",
            "VOL": "Volume",
            None: "Measurements"
        },
        "QTY": {
            "21": "OrderedQuantity",
            "59": "ConsumerUnits",
            "12": "DespatchQuantity",
            "46": "DeliveredQuantity",
            "83": "CumulativeQuantity",
            "192": "FreeGoodsQuantity",
            None: "Quantity"
        },
        "QVR": {
            "QD": "QuantityDifference",
            None: "QuantityVariances"
        }
    }
    
    # Pricing mappings
    PRICING_MAPPINGS = {
        "PRI": {
            "AAA": "NetPrice",
            "AAB": "GrossPrice",
            "AAC": "UnitPrice",
            "AAE": "InformationPrice",
            "CA": "CataloguePrice",
            "CT": "ContractPrice",
            "DI": "DiscountPrice",
            "NTP": "NetPrice",
            "SRP": "SuggestedRetailPrice",
            None: "PriceDetails"
        },
        "APR": {
            "WS": "WholesalePrice",
            "RS": "RetailPrice",
            None: "AdditionalPriceInformation"
        },
        "RNG": {
            "4": "QuantityRange",
            None: "RangeDetails"
        }
    }
    
    # Packaging and transport mappings
    PACKAGING_MAPPINGS = {
        "PAC": {
            None: "PackageInformation"
        },
        "PCI": {
            None: "PackageIdentification"
        },
        "GIN": {
            "BX": "BatchNumber",
            "SN": "SerialNumber",
            None: "GoodsIdentityNumber"
        },
        "TDT": {
            "20": "MainCarriageTransport",
            None: "TransportDetails"
        },
        "LOC": {
            "7": "PlaceOfDelivery",
            "8": "PlaceOfDestination",
            "9": "PlaceOfLoading",
            "11": "PlaceOfDeparture",
            "22": "BorderCrossingPlace",
            "88": "PlaceOfReceipt",
            None: "LocationIdentification"
        }
    }
    
    # Tax and charges mappings
    TAX_MAPPINGS = {
        "TAX": {
            "7": "TaxInformation",
            None: "TaxDetails"
        },
        "ALC": {
            "A": "Allowance",
            "C": "Charge",
            "N": "NoAllowanceOrCharge",
            None: "AllowanceCharge"
        },
        "PCD": {
            "1": "AllowancePercentage",
            "2": "ChargePercentage", 
            "3": "DiscountPercentage",
            None: "PercentageDetails"
        }
    }
    
    # Terms and conditions mappings
    TERMS_MAPPINGS = {
        "PAT": {
            "1": "PaymentTerms",
            None: "PaymentTermsBasis"
        },
        "TOD": {
            None: "TermsOfDelivery"
        },
        "TCC": {
            None: "TransportChargeCalculations"
        }
    }
    
    # Additional segment mappings
    ADDITIONAL_MAPPINGS = {
        "AJT": {
            None: "AdjustmentDetails"
        },
        "CNT": {
            "2": "TotalNumberOfLineItems",
            "3": "TotalNumberOfPackages",
            None: "ControlTotal"
        },
        "EQD": {
            None: "EquipmentDetails"
        },
        "GDS": {
            None: "NatureOfCargo"
        },
        "HAN": {
            None: "HandlingInstructions"
        },
        "LGO": {
            None: "LogoInformation"
        },
        "PGI": {
            None: "ProductGroupInformation"
        },
        "SCC": {
            None: "SchedulingConditions"
        },
        "TEM": {
            None: "TestMethod"
        }
    }
    
    # Combined mappings dictionary
    ALL_MAPPINGS = {
        **SERVICE_MAPPINGS,
        **BUSINESS_MAPPINGS,
        **PARTY_MAPPINGS,
        **MONETARY_MAPPINGS,
        **PRODUCT_MAPPINGS,
        **PRICING_MAPPINGS,
        **PACKAGING_MAPPINGS,
        **TAX_MAPPINGS,
        **TERMS_MAPPINGS,
        **ADDITIONAL_MAPPINGS
    }
    
    # Element name mappings for XML generation
    ELEMENT_MAPPINGS = {
        # UNB elements
        "S001": "SyntaxIdentifier",
        "S002": "InterchangeSender", 
        "S003": "InterchangeRecipient",
        "S004": "DateTimeOfPreparation",
        "S005": "RecipientsReferencePassword",
        
        # UNH elements
        "S009": "MessageIdentifier",
        "S010": "StatusOfTransfer",
        
        # BGM elements
        "C002": "DocumentMessageName",
        
        # DTM elements
        "C507": "DateTimePeriod",
        
        # RFF elements
        "C506": "Reference",
        
        # NAD elements
        "C082": "PartyIdentificationDetails",
        "C058": "NameAndAddress",
        "C080": "PartyName",
        "C059": "Street",
        "C819": "CountrySubEntityDetails",
        
        # LIN elements
        "C212": "ItemNumberIdentification",
        
        # QTY elements
        "C186": "QuantityDetails",
        
        # PRI elements
        "C509": "PriceInformation",
        
        # MOA elements
        "C516": "MonetaryAmount",
        
        # CUX elements
        "C504": "CurrencyDetails",
        
        # Generic element names
        "Field1": "Element01",
        "Field2": "Element02", 
        "Field3": "Element03",
        "Field4": "Element04",
        "Field5": "Element05",
        "Field6": "Element06",
        "Field7": "Element07",
        "Field8": "Element08",
        "Field9": "Element09",
        "Field10": "Element10"
    }
    
    @classmethod
    def get_semantic_name(cls, segment_tag: str, qualifier: Optional[str] = None, 
                         context: Optional[MappingContext] = None) -> str:
        """
        Get semantic XML element name for a segment and qualifier.
        
        Args:
            segment_tag: EDIFACT segment tag
            qualifier: Optional qualifier code
            context: Optional context for mapping
            
        Returns:
            Semantic XML element name
        """
        segment_tag = segment_tag.upper()
        
        # Get segment mapping
        segment_mapping = cls.ALL_MAPPINGS.get(segment_tag, {})
        
        # Try qualifier-specific mapping first
        if qualifier and qualifier in segment_mapping:
            return segment_mapping[qualifier]
        
        # Fall back to default mapping
        if None in segment_mapping:
            return segment_mapping[None]
        
        # Ultimate fallback to segment tag
        return segment_tag.title()
    
    @classmethod
    def get_element_name(cls, element_id: str, position: int = 0) -> str:
        """
        Get XML element name for a data element.
        
        Args:
            element_id: Element ID (e.g., "S001", "C507")
            position: Element position in segment
            
        Returns:
            XML element name
        """
        # Check for specific element mapping
        if element_id in cls.ELEMENT_MAPPINGS:
            return cls.ELEMENT_MAPPINGS[element_id]
        
        # Generate generic name based on position
        if position > 0:
            return f"Element{position:02d}"
        
        return "Element"
    
    @classmethod
    def get_component_name(cls, component_position: int) -> str:
        """
        Get XML component name for a composite element component.
        
        Args:
            component_position: Component position within composite
            
        Returns:
            XML component name
        """
        return f"Component{component_position:02d}"
    
    @classmethod
    def get_qualifier_description(cls, segment_tag: str, qualifier: str) -> Optional[str]:
        """
        Get description for a qualifier in context of a segment.
        
        Args:
            segment_tag: EDIFACT segment tag
            qualifier: Qualifier code
            
        Returns:
            Description if found, None otherwise
        """
        # Map segment to qualifier type
        qualifier_type_map = {
            "NAD": "party",
            "DTM": "date_time", 
            "RFF": "reference",
            "BGM": "document",
            "CUX": "currency",
            "QTY": "quantity",
            "PRI": "price",
            "FTX": "text_subject",
            "CTA": "contact_function",
            "COM": "communication_channel",
            "TDT": "transport_mode",
            "LOC": "location",
            "TAX": "tax_type",
            "ALC": "allowance_charge"
        }
        
        qualifier_type = qualifier_type_map.get(segment_tag.upper())
        if qualifier_type:
            qualifier_info = EDIFACTQualifiers.get_qualifier_description(qualifier_type, qualifier)
            if qualifier_info:
                return qualifier_info.get("description")
        
        return None
    
    @classmethod
    def get_xml_structure_template(cls) -> Dict[str, Any]:
        """
        Get default XML structure template for EDIFACT messages.
        
        Returns:
            Dictionary defining XML structure
        """
        return {
            "root": "EDIFACTMessage",
            "envelope": {
                "name": "Envelope",
                "elements": ["TIEXMLVersionNumber"]
            },
            "interchange": {
                "name": "Interchange", 
                "header": "InterchangeHeader",
                "trailer": "InterchangeTrailer"
            },
            "message": {
                "name": "Message",
                "header": "MessageHeader",
                "body": "MessageBody", 
                "trailer": "MessageTrailer"
            },
            "sections": {
                "header": "HeaderSection",
                "detail": "DetailSection", 
                "summary": "SummarySection"
            },
            "groups": {
                "references": "References",
                "parties": "Parties",
                "dates": "Dates",
                "texts": "Texts",
                "monetary": "MonetarySection",
                "line_items": "LineItems",
                "packaging": "PackagingSection",
                "transport": "TransportSection",
                "taxes": "TaxSection",
                "terms": "TermsSection"
            }
        }
    
    @classmethod
    def get_message_type_mappings(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get message type specific mappings.
        
        Returns:
            Dictionary of message type mappings
        """
        return {
            "ORDERS": {
                "name": "PurchaseOrder",
                "description": "Purchase order message",
                "root_element": "PurchaseOrderMessage",
                "header_segments": ["BGM", "DTM", "RFF", "NAD", "CTA", "COM"],
                "detail_segments": ["LIN", "PIA", "IMD", "QTY", "PRI", "MOA"],
                "summary_segments": ["UNS", "CNT", "MOA"]
            },
            "INVOIC": {
                "name": "Invoice", 
                "description": "Invoice message",
                "root_element": "InvoiceMessage",
                "header_segments": ["BGM", "DTM", "RFF", "NAD", "CTA", "COM", "CUX"],
                "detail_segments": ["LIN", "PIA", "IMD", "QTY", "MOA", "PRI", "TAX"],
                "summary_segments": ["UNS", "CNT", "MOA", "TAX"]
            },
            "DESADV": {
                "name": "DespatchAdvice",
                "description": "Despatch advice message", 
                "root_element": "DespatchAdviceMessage",
                "header_segments": ["BGM", "DTM", "RFF", "NAD", "TDT", "LOC"],
                "detail_segments": ["LIN", "PIA", "IMD", "QTY", "MEA", "PCI", "GIN"],
                "summary_segments": ["UNS", "CNT"]
            },
            "ORDRSP": {
                "name": "OrderResponse",
                "description": "Purchase order response message",
                "root_element": "OrderResponseMessage", 
                "header_segments": ["BGM", "DTM", "RFF", "NAD", "CTA", "COM"],
                "detail_segments": ["LIN", "PIA", "IMD", "QTY", "PRI", "MOA"],
                "summary_segments": ["UNS", "CNT"]
            }
        }
    
    @classmethod
    def apply_message_type_mapping(cls, message_type: str, base_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply message type specific mappings to base structure.
        
        Args:
            message_type: EDIFACT message type
            base_structure: Base XML structure
            
        Returns:
            Modified structure with message type mappings
        """
        message_mappings = cls.get_message_type_mappings()
        
        if message_type in message_mappings:
            mapping = message_mappings[message_type]
            
            # Update root element name
            if "root_element" in mapping:
                base_structure["root"] = mapping["root_element"]
            
            # Add message type specific metadata
            base_structure["message_type"] = {
                "name": mapping["name"],
                "description": mapping["description"],
                "type": message_type
            }
        
        return base_structure
    
    @classmethod
    def get_segment_grouping_rules(cls) -> Dict[str, List[str]]:
        """
        Get rules for grouping segments in XML output.
        
        Returns:
            Dictionary of grouping rules
        """
        return {
            "service_segments": ["UNA", "UNB", "UNH", "UNT", "UNZ", "UNS"],
            "reference_segments": ["RFF"],
            "party_segments": ["NAD", "CTA", "COM"],
            "date_segments": ["DTM"],
            "text_segments": ["FTX"],
            "monetary_segments": ["MOA", "CUX", "RTE"],
            "line_item_segments": ["LIN", "PIA", "IMD", "QTY", "PRI"],
            "packaging_segments": ["PAC", "PCI", "GIN"],
            "transport_segments": ["TDT", "LOC"],
            "tax_segments": ["TAX", "ALC", "PCD"],
            "terms_segments": ["PAT", "TOD", "TCC"],
            "control_segments": ["CNT"]
        }
    
    @classmethod
    def should_create_empty_element(cls, segment_tag: str, element_position: int) -> bool:
        """
        Determine if an empty XML element should be created for missing data.
        
        Args:
            segment_tag: EDIFACT segment tag
            element_position: Position of element in segment
            
        Returns:
            True if empty element should be created
        """
        # Always create empty elements for mandatory segments
        mandatory_segments = ["UNB", "UNH", "UNT", "UNZ"]
        if segment_tag.upper() in mandatory_segments:
            return True
        
        # Create empty elements for key business segments
        key_segments = ["BGM", "NAD", "LIN"]
        if segment_tag.upper() in key_segments:
            return True
        
        # Default to creating empty elements for completeness
        return True

