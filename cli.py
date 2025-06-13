#!/usr/bin/env python3
"""
Command Line Interface for EDIFACT Parser
=========================================

This module provides a command-line interface for the EDIFACT parser,
allowing users to convert EDIFACT files from the command line.

Author: EDIFACT Parser Team
Version: 1.0.0
"""

import argparse
import sys
import os
from pathlib import Path
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from edifact_parser import (
    EDIFACTToXMLConverter,
    ValidationLevel,
    get_supported_output_formats,
    setup_parser_logging,
    __version__
)


def setup_argument_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description='EDIFACT to XML Parser - Convert EDIFACT messages to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.edi output.xml
  %(prog)s input.edi output.json --format json
  %(prog)s --batch input_dir output_dir --format xml
  %(prog)s input.edi --validate-only
  %(prog)s input.edi output.xml --validation strict --pretty
        """
    )
    
    # Version
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'EDIFACT Parser {__version__}'
    )
    
    # Input/Output
    parser.add_argument(
        'input',
        help='Input EDIFACT file or directory (for batch processing)'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output file or directory (required unless --validate-only)'
    )
    
    # Output format
    parser.add_argument(
        '--format', '-f',
        choices=['xml', 'json', 'csv'],
        default='xml',
        help='Output format (default: xml)'
    )
    
    # Validation
    parser.add_argument(
        '--validation', '-v',
        choices=['none', 'basic', 'standard', 'strict'],
        default='standard',
        help='Validation level (default: standard)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate the message, do not generate output'
    )
    
    # XML options
    parser.add_argument(
        '--no-empty-tags',
        action='store_true',
        help='Do not generate empty XML tags'
    )
    
    parser.add_argument(
        '--no-semantic-names',
        action='store_true',
        help='Use generic element names instead of semantic names'
    )
    
    parser.add_argument(
        '--no-pretty',
        action='store_true',
        help='Do not format output with indentation'
    )
    
    parser.add_argument(
        '--no-statistics',
        action='store_true',
        help='Do not include parsing statistics in output'
    )
    
    parser.add_argument(
        '--no-validation-info',
        action='store_true',
        help='Do not include validation information in output'
    )
    
    # Batch processing
    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Process all files in input directory'
    )
    
    parser.add_argument(
        '--pattern',
        default='*.edifact',
        help='File pattern for batch processing (default: *.edifact)'
    )
    
    # Encoding
    parser.add_argument(
        '--encoding', '-e',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    # Logging
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        help='Log file path (default: console only)'
    )
    
    # Information
    parser.add_argument(
        '--info', '-i',
        action='store_true',
        help='Show message information only'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List supported output formats'
    )
    
    return parser


def validate_arguments(args):
    """Validate command line arguments"""
    errors = []
    
    # Check if output is required
    if not args.validate_only and not args.info and not args.list_formats and not args.output:
        errors.append("Output file/directory is required unless using --validate-only, --info, or --list-formats")
    
    # Check input file/directory exists
    if not args.list_formats:
        input_path = Path(args.input)
        if not input_path.exists():
            errors.append(f"Input file/directory does not exist: {args.input}")
        
        if args.batch and not input_path.is_dir():
            errors.append(f"Input must be a directory for batch processing: {args.input}")
        
        if not args.batch and input_path.is_dir():
            errors.append(f"Input must be a file for single file processing: {args.input}")
    
    # Check output directory for batch processing
    if args.batch and args.output:
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_dir():
            errors.append(f"Output must be a directory for batch processing: {args.output}")
    
    return errors


def process_single_file(args):
    """Process a single EDIFACT file"""
    try:
        # Setup converter
        validation_level = getattr(ValidationLevel, args.validation.upper())
        
        converter = EDIFACTToXMLConverter(
            validation_level=validation_level,
            generate_empty_tags=not args.no_empty_tags,
            use_semantic_names=not args.no_semantic_names,
            pretty_print=not args.no_pretty,
            include_statistics=not args.no_statistics,
            include_validation_info=not args.no_validation_info
        )
        
        # Read input file
        with open(args.input, 'r', encoding=args.encoding) as f:
            content = f.read()
        
        # Handle different modes
        if args.validate_only:
            # Validation only
            result = converter.validate_message(content)
            
            print(f"Validation Result: {'PASS' if result['is_valid'] else 'FAIL'}")
            print(f"Errors: {result['error_count']}")
            print(f"Warnings: {result['warning_count']}")
            print(f"Summary: {result['summary']}")
            
            if result['messages']:
                print("\nValidation Messages:")
                for message in result['messages']:
                    print(f"  {message}")
            
            return result['is_valid']
        
        elif args.info:
            # Information only
            info = converter.get_message_info(content)
            
            print("Message Information:")
            for key, value in info.items():
                if value is not None:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            return True
        
        else:
            # Convert to output format
            if args.format == 'xml':
                result = converter.convert_string(content)
            else:
                result = converter.convert_to_format(content, args.format)
            
            # Write output
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            
            print(f"Successfully converted {args.input} to {args.output}")
            
            # Show statistics
            stats = converter.get_statistics()
            print(f"Processing time: {stats.get('processing_time', 0):.3f} seconds")
            print(f"Segments: {stats.get('total_segments', 0)}")
            print(f"Elements: {stats.get('total_elements', 0)}")
            
            return True
    
    except Exception as e:
        print(f"Error processing {args.input}: {e}", file=sys.stderr)
        return False


def process_batch(args):
    """Process multiple files in batch mode"""
    try:
        # Setup converter
        validation_level = getattr(ValidationLevel, args.validation.upper())
        
        converter = EDIFACTToXMLConverter(
            validation_level=validation_level,
            generate_empty_tags=not args.no_empty_tags,
            use_semantic_names=not args.no_semantic_names,
            pretty_print=not args.no_pretty,
            include_statistics=not args.no_statistics,
            include_validation_info=not args.no_validation_info
        )
        
        # Process directory
        results = converter.batch_convert_directory(
            input_dir=args.input,
            output_dir=args.output,
            output_format=args.format,
            file_pattern=args.pattern
        )
        
        # Show results
        print(f"Batch Processing Results:")
        print(f"  Total files: {results['total_files']}")
        print(f"  Processed: {results['processed_files']}")
        print(f"  Failed: {results['failed_files']}")
        
        if results['errors']:
            print(f"\nErrors:")
            for error in results['errors']:
                print(f"  {error}")
        
        return results['failed_files'] == 0
    
    except Exception as e:
        print(f"Error in batch processing: {e}", file=sys.stderr)
        return False


def list_supported_formats():
    """List supported output formats"""
    formats = get_supported_output_formats()
    
    print("Supported Output Formats:")
    for fmt, description in formats.items():
        print(f"  {fmt}: {description}")


def main():
    """Main entry point"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Handle special cases
    if args.list_formats:
        list_supported_formats()
        return 0
    
    # Validate arguments
    errors = validate_arguments(args)
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1
    
    # Setup logging
    setup_parser_logging(args.log_level, args.log_file)
    
    # Process based on mode
    try:
        if args.batch:
            success = process_batch(args)
        else:
            success = process_single_file(args)
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

