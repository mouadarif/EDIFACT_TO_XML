# EDIFACT Parser Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Architecture](#architecture)
5. [API Reference](#api-reference)
6. [Examples](#examples)
7. [Configuration](#configuration)
8. [Validation](#validation)
9. [Output Formats](#output-formats)
10. [Error Handling](#error-handling)
11. [Performance](#performance)
12. [Extending the Parser](#extending-the-parser)

## Introduction

The EDIFACT Parser is a comprehensive, modular Python library for parsing EDIFACT (Electronic Data Interchange For Administration, Commerce and Transport) messages and converting them to XML format. It provides professional-grade validation, semantic mapping, and structured output generation.

### Key Features

- **Complete EDIFACT Support**: Handles all standard EDIFACT segments, elements, and qualifiers
- **Semantic Mapping**: Converts EDIFACT codes to meaningful XML element names
- **Multiple Validation Levels**: From basic syntax checking to full business rule validation
- **Multiple Output Formats**: XML, JSON, CSV with customizable formatting
- **Modular Architecture**: Extensible design for custom mappings and validations
- **Comprehensive Error Handling**: Graceful handling of malformed or incomplete messages
- **Performance Optimized**: Efficient parsing with detailed statistics tracking
- **Batch Processing**: Support for processing multiple files and directories

### Supported Message Types

The parser supports all standard EDIFACT message types including:

- **ORDERS** - Purchase Orders
- **INVOIC** - Invoices
- **DESADV** - Despatch Advice
- **ORDRSP** - Order Response
- **REMADV** - Remittance Advice
- **PRICAT** - Price/Sales Catalogue
- And many more...

## Installation

### Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

### Installation Methods

#### Method 1: Direct Installation
```bash
# Clone or download the edifact_parser directory
# Add to your Python path or install locally
pip install -e /path/to/edifact_parser
```

#### Method 2: Copy Module
```bash
# Copy the edifact_parser directory to your project
cp -r edifact_parser /your/project/path/
```

#### Method 3: Python Path
```python
import sys
sys.path.append('/path/to/edifact_parser')
import edifact_parser
```

## Quick Start

### Basic Usage

```python
from edifact_parser import convert_edifact_to_xml

# EDIFACT message content
edifact_content = """UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""

# Convert to XML
xml_result = convert_edifact_to_xml(edifact_content)
print(xml_result)
```

### File Conversion

```python
from edifact_parser import convert_edifact_file_to_xml

# Convert file
success = convert_edifact_file_to_xml('input.edi', 'output.xml')
if success:
    print("Conversion successful!")
```

### Detailed Parsing

```python
from edifact_parser import parse_edifact_message

# Parse and extract structured data
data = parse_edifact_message(edifact_content)

print(f"Message Type: {data['message_info']['type']}")
print(f"Sender: {data['interchange_info']['sender_id']}")
print(f"Segments: {len(data['segments'])}")
```

## Architecture

The EDIFACT Parser follows a modular architecture with clear separation of concerns:

### Core Modules

1. **edifact_syntax.py** - EDIFACT syntax parsing and character handling
2. **edifact_elements.py** - Data element definitions and types
3. **edifact_qualifiers.py** - Qualifier codes and descriptions
4. **edifact_segments.py** - Segment definitions and structures
5. **edifact_mappings.py** - Semantic mappings for XML generation
6. **edifact_validators.py** - Validation rules and error checking
7. **edifact_parser.py** - Main parsing engine
8. **xml_generator.py** - XML output generation
9. **edifact_utils.py** - Utility functions and helpers

### Data Flow

```
EDIFACT Input → Syntax Parser → Segment Parser → Element Parser → Validator → XML Generator → Output
```

### Key Classes

- **EDIFACTToXMLConverter** - Main interface class
- **EDIFACTParser** - Core parsing functionality
- **XMLGenerator** - XML output generation
- **EDIFACTValidator** - Message validation
- **EDIFACTMappings** - Semantic mappings

## API Reference

### Main Interface

#### EDIFACTToXMLConverter

The primary interface for EDIFACT parsing and conversion.

```python
class EDIFACTToXMLConverter:
    def __init__(self,
                 validation_level: ValidationLevel = ValidationLevel.STANDARD,
                 generate_empty_tags: bool = True,
                 use_semantic_names: bool = True,
                 pretty_print: bool = True,
                 include_statistics: bool = True,
                 include_validation_info: bool = True)
```

**Methods:**

- `convert_string(edifact_content: str) -> str` - Convert EDIFACT string to XML
- `convert_file(input_file: str, output_file: str) -> bool` - Convert file to file
- `parse_and_extract(edifact_content: str) -> Dict` - Parse and extract data
- `validate_message(edifact_content: str) -> Dict` - Validate message
- `get_message_info(edifact_content: str) -> Dict` - Get basic message info

### Convenience Functions

```python
# Quick conversion
convert_edifact_to_xml(edifact_content: str, **kwargs) -> str

# File conversion
convert_edifact_file_to_xml(input_file: str, output_file: str, **kwargs) -> bool

# Parsing
parse_edifact_message(edifact_content: str, **kwargs) -> Dict

# Validation
validate_edifact_message(edifact_content: str, **kwargs) -> Dict
```

### Configuration Classes

#### XMLGeneratorConfig

```python
class XMLGeneratorConfig:
    def __init__(self,
                 generate_empty_tags: bool = True,
                 include_attributes: bool = True,
                 include_descriptions: bool = False,
                 pretty_print: bool = True,
                 indent_size: int = 2,
                 xml_encoding: str = 'UTF-8',
                 use_semantic_names: bool = True,
                 group_segments: bool = True)
```

#### ValidationLevel

```python
class ValidationLevel(Enum):
    NONE = "none"           # No validation
    BASIC = "basic"         # Basic syntax validation
    STANDARD = "standard"   # Standard validation (default)
    STRICT = "strict"       # Strict validation with business rules
```

## Examples

### Example 1: Basic Conversion

```python
from edifact_parser import convert_edifact_to_xml

edifact = """UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'DTM+137:20231201:102'UNT+5+1'UNZ+1+1'"""

xml_result = convert_edifact_to_xml(edifact)
print(xml_result)
```

### Example 2: Custom Configuration

```python
from edifact_parser import EDIFACTToXMLConverter, ValidationLevel

converter = EDIFACTToXMLConverter(
    validation_level=ValidationLevel.STRICT,
    generate_empty_tags=True,
    use_semantic_names=True,
    pretty_print=True
)

xml_result = converter.convert_string(edifact_content)
```

### Example 3: Data Extraction

```python
from edifact_parser import parse_edifact_message

data = parse_edifact_message(edifact_content)

# Access message information
print(f"Type: {data['message_info']['type']}")
print(f"Reference: {data['message_info']['reference']}")

# Access business data
business_data = data['business_data']
for qualifier, party in business_data['parties'].items():
    print(f"Party {qualifier}: {party['name']}")
```

### Example 4: Validation

```python
from edifact_parser import validate_edifact_message

result = validate_edifact_message(edifact_content)

if result['is_valid']:
    print("Message is valid!")
else:
    print(f"Validation failed: {result['error_count']} errors")
    for message in result['messages']:
        print(f"  - {message}")
```

### Example 5: Multiple Output Formats

```python
from edifact_parser import EDIFACTToXMLConverter

converter = EDIFACTToXMLConverter()

# XML output
xml_result = converter.convert_to_format(edifact_content, 'xml')

# JSON output
json_result = converter.convert_to_format(edifact_content, 'json')

# CSV output
csv_result = converter.convert_to_format(edifact_content, 'csv')
```

### Example 6: Batch Processing

```python
from edifact_parser import EDIFACTToXMLConverter

converter = EDIFACTToXMLConverter()

# Process directory
results = converter.batch_convert_directory(
    input_dir='/path/to/edifact/files',
    output_dir='/path/to/xml/output',
    output_format='xml',
    file_pattern='*.edi'
)

print(f"Processed: {results['processed_files']}")
print(f"Failed: {results['failed_files']}")
```

## Configuration

### Validation Levels

- **NONE**: No validation performed, fastest processing
- **BASIC**: Basic syntax validation only
- **STANDARD**: Standard validation including segment structure (default)
- **STRICT**: Full validation including business rules

### XML Generation Options

- **generate_empty_tags**: Create empty XML elements for missing data
- **use_semantic_names**: Use meaningful element names instead of generic ones
- **pretty_print**: Format XML with indentation
- **include_attributes**: Include EDIFACT attributes in XML elements
- **include_descriptions**: Include description attributes
- **group_segments**: Group segments by type in XML structure

### Output Customization

```python
from edifact_parser import XMLGeneratorConfig, EDIFACTToXMLConverter

config = XMLGeneratorConfig(
    generate_empty_tags=True,
    pretty_print=True,
    indent_size=4,
    xml_encoding='UTF-8',
    use_semantic_names=True,
    group_segments=True
)

converter = EDIFACTToXMLConverter()
converter.xml_generator.config = config
```

## Validation

The parser provides comprehensive validation at multiple levels:

### Syntax Validation

- Segment structure validation
- Element format validation
- Component data type validation
- Length constraints validation

### Semantic Validation

- Mandatory element checking
- Code list validation
- Cross-reference validation
- Business rule validation

### Validation Results

```python
validation_result = {
    'is_valid': bool,
    'error_count': int,
    'warning_count': int,
    'info_count': int,
    'messages': [str],
    'summary': str
}
```

### Custom Validation

You can extend validation by subclassing `EDIFACTValidator`:

```python
from edifact_parser.edifact_validators import EDIFACTValidator

class CustomValidator(EDIFACTValidator):
    def validate_custom_rules(self, segments):
        # Implement custom validation logic
        pass
```

## Output Formats

### XML Output

The primary output format with full semantic mapping:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ORDERSMessage messageType="ORDERS" messageVersion="D" messageRelease="03B">
  <Envelope>
    <TIEXMLVersionNumber>2.3.2</TIEXMLVersionNumber>
  </Envelope>
  <ServiceSegments>
    <InterchangeHeader segmentTag="UNB" position="1">
      <SyntaxIdentifier position="1">
        <Component01>UNOC</Component01>
        <Component02>3</Component02>
      </SyntaxIdentifier>
      <!-- More elements... -->
    </InterchangeHeader>
  </ServiceSegments>
  <!-- More sections... -->
</ORDERSMessage>
```

### JSON Output

Structured data representation:

```json
{
  "message_info": {
    "type": "ORDERS",
    "version": "D",
    "release": "03B",
    "reference": "1"
  },
  "segments": [
    {
      "tag": "UNB",
      "position": 1,
      "semantic_name": "InterchangeHeader",
      "elements": [...]
    }
  ]
}
```

### CSV Output

Tabular representation for analysis:

```csv
SegmentTag,Position,ElementCount,SemanticName
UNB,1,5,InterchangeHeader
UNH,2,2,MessageHeader
BGM,3,3,BeginningOfMessage
```

## Error Handling

The parser is designed to handle errors gracefully:

### Error Types

1. **Syntax Errors**: Malformed EDIFACT structure
2. **Validation Errors**: Rule violations
3. **Processing Errors**: Unexpected data or system issues

### Error Recovery

- Continues processing after non-fatal errors
- Generates placeholder elements for missing data
- Provides detailed error reporting

### Exception Handling

```python
from edifact_parser import EDIFACTToXMLConverter

converter = EDIFACTToXMLConverter()

try:
    result = converter.convert_string(edifact_content)
except Exception as e:
    print(f"Conversion failed: {e}")
    
    # Get validation info for details
    validation = converter.validate_message(edifact_content)
    for message in validation['messages']:
        print(f"  {message}")
```

## Performance

### Optimization Features

- Efficient string parsing algorithms
- Lazy loading of definitions
- Memory-conscious processing
- Detailed performance statistics

### Performance Statistics

```python
stats = converter.get_statistics()
print(f"Processing time: {stats['processing_time']:.3f}s")
print(f"Segments processed: {stats['total_segments']}")
print(f"Elements processed: {stats['total_elements']}")
print(f"Memory usage: {stats['file_size']} bytes")
```

### Best Practices

1. **Reuse Converter Instances**: Create once, use multiple times
2. **Choose Appropriate Validation Level**: Balance speed vs. accuracy
3. **Use Batch Processing**: For multiple files
4. **Monitor Statistics**: Track performance metrics

## Extending the Parser

### Custom Mappings

Add custom semantic mappings:

```python
from edifact_parser.edifact_mappings import EDIFACTMappings

# Add custom segment mapping
EDIFACTMappings.BUSINESS_MAPPINGS["ZZZ"] = {
    None: "CustomSegment",
    "description": "Custom business segment"
}
```

### Custom Validators

Implement custom validation rules:

```python
from edifact_parser.edifact_validators import EDIFACTValidator, ValidationResult

class CustomValidator(EDIFACTValidator):
    def validate_custom_business_rules(self, segments):
        result = ValidationResult(is_valid=True, messages=[])
        # Implement custom validation logic
        return result
```

### Custom Output Formats

Add support for new output formats:

```python
from edifact_parser.edifact_utils import DataExtractor

class CustomExtractor(DataExtractor):
    def extract_to_custom_format(self, parsed_message):
        # Implement custom format extraction
        pass
```

### Plugin Architecture

The modular design allows for easy extension through plugins:

```python
# Custom plugin example
class EDIFACTPlugin:
    def process_segment(self, segment):
        # Custom segment processing
        pass
    
    def generate_output(self, data):
        # Custom output generation
        pass
```

---

## Support and Contributing

For support, bug reports, or feature requests, please refer to the project documentation or contact the development team.

### Version Information

- **Version**: 1.0.0
- **Author**: EDIFACT Parser Team
- **License**: MIT
- **Python**: 3.7+

### Changelog

#### Version 1.0.0
- Initial release
- Complete EDIFACT parsing support
- XML, JSON, CSV output formats
- Comprehensive validation
- Modular architecture
- Extensive documentation and examples

