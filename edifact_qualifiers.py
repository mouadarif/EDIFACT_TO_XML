#!/usr/bin/env python3
"""
EDIFACT Qualifiers Module
========================

This module contains comprehensive qualifier code lists for EDIFACT elements.
Qualifiers provide specific meaning to data elements and are essential for
proper interpretation of EDIFACT messages.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Set
from enum import Enum


class QualifierCategory(Enum):
    """Categories of EDIFACT qualifiers"""
    PARTY = "party"
    DATE_TIME = "date_time"
    REFERENCE = "reference"
    DOCUMENT = "document"
    PRICE = "price"
    QUANTITY = "quantity"
    CURRENCY = "currency"
    MEASUREMENT = "measurement"
    TEXT = "text"
    TRANSPORT = "transport"
    LOCATION = "location"
    TAX = "tax"
    ALLOWANCE_CHARGE = "allowance_charge"
    CONTACT = "contact"
    COMMUNICATION = "communication"


class EDIFACTQualifiers:
    """
    Complete EDIFACT qualifier code lists.
    
    Contains all standard UN/EDIFACT qualifier codes organized by category
    with descriptions and usage context.
    """
    
    # Party qualifiers (3035)
    PARTY_QUALIFIERS = {
        "AG": {"name": "Agent", "description": "Party authorized to act on behalf of another party"},
        "BY": {"name": "Buyer", "description": "Party to whom merchandise or services are sold"},
        "CA": {"name": "Carrier", "description": "Party undertaking or arranging transport of goods"},
        "CN": {"name": "Consignee", "description": "Party to whom goods are consigned"},
        "DP": {"name": "Delivery party", "description": "Party to whom goods should be delivered"},
        "FR": {"name": "Message from", "description": "Party where the message comes from"},
        "FW": {"name": "Freight forwarder", "description": "Party arranging the forwarding of goods"},
        "II": {"name": "Issuer of invoice", "description": "Party issuing an invoice"},
        "IV": {"name": "Invoicee", "description": "Party to whom an invoice is issued"},
        "MR": {"name": "Message recipient", "description": "Party receiving the message"},
        "MS": {"name": "Message sender", "description": "Party sending the message"},
        "OB": {"name": "Ordered by", "description": "Party who ordered the goods or services"},
        "OY": {"name": "Origin of consignment", "description": "Party from whom goods are consigned"},
        "PD": {"name": "Purchaser", "description": "Party purchasing goods or services"},
        "PE": {"name": "Payee", "description": "Party to whom payment is made"},
        "PR": {"name": "Payer", "description": "Party making payment"},
        "RE": {"name": "Remit to", "description": "Party to whom payment should be remitted"},
        "SH": {"name": "Shipper", "description": "Party shipping goods"},
        "SU": {"name": "Supplier", "description": "Party supplying goods or services"},
        "TO": {"name": "Message to", "description": "Party to whom the message is directed"},
        "UC": {"name": "Ultimate consignee", "description": "Final party to receive goods"},
        "UD": {"name": "Ultimate customer", "description": "Final customer"},
        "WH": {"name": "Warehouse", "description": "Party operating a warehouse"},
    }
    
    # Date/time qualifiers (2005)
    DATE_TIME_QUALIFIERS = {
        "2": {"name": "Delivery date/time", "description": "Date/time of delivery"},
        "3": {"name": "Invoice date/time", "description": "Date/time of invoice"},
        "4": {"name": "Order date/time", "description": "Date/time of order"},
        "7": {"name": "Effective date/time", "description": "Date/time when something becomes effective"},
        "10": {"name": "Shipment date/time", "description": "Date/time of shipment"},
        "11": {"name": "Despatch date/time", "description": "Date/time of despatch"},
        "35": {"name": "Delivery date/time, latest", "description": "Latest date/time for delivery"},
        "36": {"name": "Expiry date", "description": "Date when something expires"},
        "37": {"name": "Ship not before date/time", "description": "Earliest date/time for shipment"},
        "38": {"name": "Ship not later than date/time", "description": "Latest date/time for shipment"},
        "63": {"name": "Best before date/time", "description": "Date/time before which product is best"},
        "64": {"name": "Sell by date/time", "description": "Date/time by which product should be sold"},
        "94": {"name": "Production date/time", "description": "Date/time of production"},
        "137": {"name": "Document/message date/time", "description": "Date/time of document or message"},
        "140": {"name": "Payment due date/time", "description": "Date/time when payment is due"},
        "171": {"name": "Reference date/time", "description": "Date/time used as reference"},
        "200": {"name": "Pick-up/collection date/time", "description": "Date/time for pick-up or collection"},
        "273": {"name": "Validity date/time", "description": "Date/time until which something is valid"},
    }
    
    # Reference qualifiers (1153)
    REFERENCE_QUALIFIERS = {
        "AAA": {"name": "Reference number assigned by issuer", "description": "Reference number assigned by the issuer"},
        "AAB": {"name": "Proforma invoice number", "description": "Reference number of proforma invoice"},
        "AAC": {"name": "Container/package reference number", "description": "Reference number for container or package"},
        "AAS": {"name": "Transport document number", "description": "Reference number of transport document"},
        "AAT": {"name": "Master reference number", "description": "Master reference number"},
        "CR": {"name": "Customer reference number", "description": "Reference number assigned by customer"},
        "CT": {"name": "Contract number", "description": "Reference number of contract"},
        "DQ": {"name": "Delivery note number", "description": "Reference number of delivery note"},
        "IV": {"name": "Invoice number", "description": "Reference number of invoice"},
        "ON": {"name": "Order number", "description": "Reference number of order"},
        "PD": {"name": "Promotion deal number", "description": "Reference number of promotion deal"},
        "PK": {"name": "Packing list number", "description": "Reference number of packing list"},
        "VN": {"name": "Vendor number", "description": "Reference number assigned to vendor"},
        "WE": {"name": "Warehouse entry number", "description": "Reference number for warehouse entry"},
    }
    
    # Document/message name codes (1001)
    DOCUMENT_MESSAGE_CODES = {
        "105": {"name": "Purchase order", "description": "Document/message for ordering goods or services"},
        "220": {"name": "Order", "description": "Document/message for placing an order"},
        "221": {"name": "Blanket order", "description": "Document/message for blanket ordering"},
        "224": {"name": "Rush order", "description": "Document/message for urgent ordering"},
        "230": {"name": "Delivery schedule", "description": "Document/message with delivery schedule"},
        "231": {"name": "Delivery just-in-time", "description": "Document/message for just-in-time delivery"},
        "270": {"name": "Invoice", "description": "Document/message claiming payment"},
        "271": {"name": "Self billed invoice", "description": "Invoice prepared by buyer"},
        "380": {"name": "Commercial invoice", "description": "Document/message claiming payment for goods or services"},
        "381": {"name": "Credit note", "description": "Document/message for crediting an account"},
        "383": {"name": "Debit note", "description": "Document/message for debiting an account"},
        "751": {"name": "Invoice information for accounting purposes", "description": "Invoice information for accounting"},
    }
    
    # Message function codes (1225)
    MESSAGE_FUNCTION_CODES = {
        "1": {"name": "Cancellation", "description": "Message cancels a previous message"},
        "2": {"name": "Addition", "description": "Message adds to a previous message"},
        "3": {"name": "Deletion", "description": "Message deletes from a previous message"},
        "4": {"name": "Change", "description": "Message changes a previous message"},
        "5": {"name": "Replace", "description": "Message replaces a previous message"},
        "7": {"name": "Duplicate", "description": "Message is a duplicate"},
        "9": {"name": "Original", "description": "Message is original"},
        "31": {"name": "Copy", "description": "Message is a copy"},
        "42": {"name": "Confirmation", "description": "Message confirms a previous message"},
        "43": {"name": "Duplicate", "description": "Message is a duplicate"},
    }
    
    # Price qualifiers (5125)
    PRICE_QUALIFIERS = {
        "AAA": {"name": "Net price", "description": "Price after deductions"},
        "AAB": {"name": "Gross price", "description": "Price before deductions"},
        "AAC": {"name": "Unit price", "description": "Price per unit"},
        "AAE": {"name": "Information price", "description": "Price for information only"},
        "CA": {"name": "Catalogue price", "description": "Price from catalogue"},
        "CT": {"name": "Contract price", "description": "Price according to contract"},
        "DI": {"name": "Discount price", "description": "Discounted price"},
        "NTP": {"name": "Net price", "description": "Net price"},
        "SRP": {"name": "Suggested retail price", "description": "Recommended retail price"},
    }
    
    # Quantity qualifiers (6063)
    QUANTITY_QUALIFIERS = {
        "12": {"name": "Despatch quantity", "description": "Quantity despatched"},
        "21": {"name": "Ordered quantity", "description": "Quantity ordered"},
        "46": {"name": "Delivered quantity", "description": "Quantity delivered"},
        "59": {"name": "Consumer units", "description": "Number of consumer units in traded unit"},
        "83": {"name": "Cumulative quantity", "description": "Total cumulative quantity"},
        "192": {"name": "Free goods quantity", "description": "Quantity of free goods"},
    }
    
    # Currency codes (6345) - ISO 4217
    CURRENCY_CODES = {
        "EUR": {"name": "Euro", "description": "European Union currency"},
        "USD": {"name": "US Dollar", "description": "United States currency"},
        "GBP": {"name": "Pound Sterling", "description": "United Kingdom currency"},
        "JPY": {"name": "Yen", "description": "Japanese currency"},
        "CHF": {"name": "Swiss Franc", "description": "Swiss currency"},
        "CAD": {"name": "Canadian Dollar", "description": "Canadian currency"},
        "AUD": {"name": "Australian Dollar", "description": "Australian currency"},
        "SEK": {"name": "Swedish Krona", "description": "Swedish currency"},
        "NOK": {"name": "Norwegian Krone", "description": "Norwegian currency"},
        "DKK": {"name": "Danish Krone", "description": "Danish currency"},
    }
    
    # Measurement unit qualifiers (6411)
    MEASUREMENT_UNIT_QUALIFIERS = {
        "KGM": {"name": "Kilogram", "description": "Unit of mass"},
        "GRM": {"name": "Gram", "description": "Unit of mass"},
        "LTR": {"name": "Litre", "description": "Unit of volume"},
        "MTR": {"name": "Metre", "description": "Unit of length"},
        "CMT": {"name": "Centimetre", "description": "Unit of length"},
        "MMT": {"name": "Millimetre", "description": "Unit of length"},
        "MTK": {"name": "Square metre", "description": "Unit of area"},
        "MTQ": {"name": "Cubic metre", "description": "Unit of volume"},
        "PCE": {"name": "Piece", "description": "Unit of count"},
        "SET": {"name": "Set", "description": "Unit of count"},
        "PAR": {"name": "Pair", "description": "Unit of count"},
        "DOZ": {"name": "Dozen", "description": "Unit of count (12)"},
    }
    
    # Text subject qualifiers (4453)
    TEXT_SUBJECT_QUALIFIERS = {
        "AAI": {"name": "General information", "description": "General information text"},
        "DEL": {"name": "Delivery text", "description": "Text related to delivery"},
        "GEN": {"name": "General text", "description": "General purpose text"},
        "PMT": {"name": "Payment terms", "description": "Text describing payment terms"},
        "REG": {"name": "Regulatory text", "description": "Text related to regulations"},
        "TXD": {"name": "Tax declaration", "description": "Text for tax declaration"},
    }
    
    # Contact function codes (3139)
    CONTACT_FUNCTION_CODES = {
        "IC": {"name": "Information contact", "description": "Contact for information"},
        "OC": {"name": "Order contact", "description": "Contact for orders"},
        "PD": {"name": "Purchasing contact", "description": "Contact for purchasing"},
        "SA": {"name": "Sales contact", "description": "Contact for sales"},
        "SU": {"name": "Supplier contact", "description": "Contact at supplier"},
    }
    
    # Communication channel qualifiers (3155)
    COMMUNICATION_CHANNEL_QUALIFIERS = {
        "EM": {"name": "Electronic mail", "description": "Email communication"},
        "FX": {"name": "Telefax", "description": "Fax communication"},
        "TE": {"name": "Telephone", "description": "Telephone communication"},
        "TL": {"name": "Telex", "description": "Telex communication"},
        "UR": {"name": "Uniform resource locator", "description": "URL/website"},
    }
    
    # Transport mode codes (8067)
    TRANSPORT_MODE_CODES = {
        "1": {"name": "Maritime transport", "description": "Transport by sea"},
        "2": {"name": "Rail transport", "description": "Transport by rail"},
        "3": {"name": "Road transport", "description": "Transport by road"},
        "4": {"name": "Air transport", "description": "Transport by air"},
        "5": {"name": "Mail", "description": "Transport by mail"},
        "6": {"name": "Multimodal transport", "description": "Transport using multiple modes"},
        "7": {"name": "Fixed transport installations", "description": "Transport by pipeline etc."},
        "8": {"name": "Inland water transport", "description": "Transport by inland waterway"},
    }
    
    # Location qualifiers (3227)
    LOCATION_QUALIFIERS = {
        "7": {"name": "Place of delivery", "description": "Location where goods are delivered"},
        "8": {"name": "Place of destination", "description": "Final destination location"},
        "9": {"name": "Place of loading", "description": "Location where goods are loaded"},
        "11": {"name": "Place of departure", "description": "Location where transport starts"},
        "22": {"name": "Border crossing place", "description": "Location of border crossing"},
        "88": {"name": "Place of receipt", "description": "Location where goods are received"},
    }
    
    # Tax type qualifiers (5153)
    TAX_TYPE_QUALIFIERS = {
        "VAT": {"name": "Value added tax", "description": "Value added tax"},
        "GST": {"name": "Goods and services tax", "description": "Goods and services tax"},
        "EXC": {"name": "Excise tax", "description": "Excise tax"},
        "STT": {"name": "State tax", "description": "State tax"},
        "LOC": {"name": "Local tax", "description": "Local tax"},
    }
    
    # Allowance/charge qualifiers (5463)
    ALLOWANCE_CHARGE_QUALIFIERS = {
        "A": {"name": "Allowance", "description": "Amount is an allowance"},
        "C": {"name": "Charge", "description": "Amount is a charge"},
        "N": {"name": "No allowance or charge", "description": "No allowance or charge applies"},
    }
    
    @classmethod
    def get_qualifier_description(cls, qualifier_type: str, code: str) -> Optional[Dict[str, str]]:
        """
        Get description for a qualifier code.
        
        Args:
            qualifier_type: Type of qualifier (e.g., 'party', 'date_time')
            code: Qualifier code
            
        Returns:
            Dictionary with name and description, or None if not found
        """
        qualifier_maps = {
            'party': cls.PARTY_QUALIFIERS,
            'date_time': cls.DATE_TIME_QUALIFIERS,
            'reference': cls.REFERENCE_QUALIFIERS,
            'document': cls.DOCUMENT_MESSAGE_CODES,
            'message_function': cls.MESSAGE_FUNCTION_CODES,
            'price': cls.PRICE_QUALIFIERS,
            'quantity': cls.QUANTITY_QUALIFIERS,
            'currency': cls.CURRENCY_CODES,
            'measurement_unit': cls.MEASUREMENT_UNIT_QUALIFIERS,
            'text_subject': cls.TEXT_SUBJECT_QUALIFIERS,
            'contact_function': cls.CONTACT_FUNCTION_CODES,
            'communication_channel': cls.COMMUNICATION_CHANNEL_QUALIFIERS,
            'transport_mode': cls.TRANSPORT_MODE_CODES,
            'location': cls.LOCATION_QUALIFIERS,
            'tax_type': cls.TAX_TYPE_QUALIFIERS,
            'allowance_charge': cls.ALLOWANCE_CHARGE_QUALIFIERS,
        }
        
        qualifier_map = qualifier_maps.get(qualifier_type)
        if qualifier_map:
            return qualifier_map.get(code)
        return None
    
    @classmethod
    def get_all_qualifiers_by_type(cls, qualifier_type: str) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Get all qualifiers of a specific type.
        
        Args:
            qualifier_type: Type of qualifier
            
        Returns:
            Dictionary of all qualifiers of that type, or None if type not found
        """
        qualifier_maps = {
            'party': cls.PARTY_QUALIFIERS,
            'date_time': cls.DATE_TIME_QUALIFIERS,
            'reference': cls.REFERENCE_QUALIFIERS,
            'document': cls.DOCUMENT_MESSAGE_CODES,
            'message_function': cls.MESSAGE_FUNCTION_CODES,
            'price': cls.PRICE_QUALIFIERS,
            'quantity': cls.QUANTITY_QUALIFIERS,
            'currency': cls.CURRENCY_CODES,
            'measurement_unit': cls.MEASUREMENT_UNIT_QUALIFIERS,
            'text_subject': cls.TEXT_SUBJECT_QUALIFIERS,
            'contact_function': cls.CONTACT_FUNCTION_CODES,
            'communication_channel': cls.COMMUNICATION_CHANNEL_QUALIFIERS,
            'transport_mode': cls.TRANSPORT_MODE_CODES,
            'location': cls.LOCATION_QUALIFIERS,
            'tax_type': cls.TAX_TYPE_QUALIFIERS,
            'allowance_charge': cls.ALLOWANCE_CHARGE_QUALIFIERS,
        }
        
        return qualifier_maps.get(qualifier_type)
    
    @classmethod
    def validate_qualifier(cls, qualifier_type: str, code: str) -> bool:
        """
        Validate if a qualifier code exists for a given type.
        
        Args:
            qualifier_type: Type of qualifier
            code: Qualifier code to validate
            
        Returns:
            True if valid, False otherwise
        """
        qualifiers = cls.get_all_qualifiers_by_type(qualifier_type)
        if qualifiers:
            return code in qualifiers
        return False
    
    @classmethod
    def search_qualifiers(cls, search_term: str) -> List[Dict[str, str]]:
        """
        Search for qualifiers containing the search term.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching qualifiers with their details
        """
        results = []
        search_term = search_term.lower()
        
        all_qualifier_maps = [
            ('party', cls.PARTY_QUALIFIERS),
            ('date_time', cls.DATE_TIME_QUALIFIERS),
            ('reference', cls.REFERENCE_QUALIFIERS),
            ('document', cls.DOCUMENT_MESSAGE_CODES),
            ('message_function', cls.MESSAGE_FUNCTION_CODES),
            ('price', cls.PRICE_QUALIFIERS),
            ('quantity', cls.QUANTITY_QUALIFIERS),
            ('currency', cls.CURRENCY_CODES),
            ('measurement_unit', cls.MEASUREMENT_UNIT_QUALIFIERS),
            ('text_subject', cls.TEXT_SUBJECT_QUALIFIERS),
            ('contact_function', cls.CONTACT_FUNCTION_CODES),
            ('communication_channel', cls.COMMUNICATION_CHANNEL_QUALIFIERS),
            ('transport_mode', cls.TRANSPORT_MODE_CODES),
            ('location', cls.LOCATION_QUALIFIERS),
            ('tax_type', cls.TAX_TYPE_QUALIFIERS),
            ('allowance_charge', cls.ALLOWANCE_CHARGE_QUALIFIERS),
        ]
        
        for qualifier_type, qualifier_map in all_qualifier_maps:
            for code, details in qualifier_map.items():
                if (search_term in code.lower() or 
                    search_term in details['name'].lower() or 
                    search_term in details['description'].lower()):
                    results.append({
                        'type': qualifier_type,
                        'code': code,
                        'name': details['name'],
                        'description': details['description']
                    })
        
        return results


# Convenience functions for common qualifier lookups
def get_party_qualifier(code: str) -> Optional[Dict[str, str]]:
    """Get party qualifier description."""
    return EDIFACTQualifiers.get_qualifier_description('party', code)


def get_date_time_qualifier(code: str) -> Optional[Dict[str, str]]:
    """Get date/time qualifier description."""
    return EDIFACTQualifiers.get_qualifier_description('date_time', code)


def get_reference_qualifier(code: str) -> Optional[Dict[str, str]]:
    """Get reference qualifier description."""
    return EDIFACTQualifiers.get_qualifier_description('reference', code)


def get_document_code(code: str) -> Optional[Dict[str, str]]:
    """Get document/message code description."""
    return EDIFACTQualifiers.get_qualifier_description('document', code)


def get_currency_code(code: str) -> Optional[Dict[str, str]]:
    """Get currency code description."""
    return EDIFACTQualifiers.get_qualifier_description('currency', code)

