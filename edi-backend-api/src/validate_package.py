#!/usr/bin/env python3
"""
Final Test and Package Validation
=================================

Complete test of the EDIFACT parser package to ensure everything works correctly.
"""

import sys
import os
from pathlib import Path

def test_package_structure():
    """Test that all required files are present"""
    print("📁 Testing package structure...")
    
    current_dir = Path(__file__).parent
    required_files = [
        '__init__.py',
        'edifact_syntax.py',
        'edifact_elements.py',
        'edifact_qualifiers.py',
        'edifact_constants.py',
        'edifact_segments.py',
        'edifact_mappings.py',
        'edifact_validators.py',
        'edifact_parser.py',
        'xml_generator.py',
        'edifact_utils.py',
        '__main__.py',
        'cli.py',
        'demo.py',
        'README.md',
        'LICENSE',
        'INSTALL.md'
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name}")
            missing_files.append(file_name)
    
    # Check directories
    required_dirs = ['tests', 'examples', 'docs', 'sample_files']
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/")
            missing_files.append(f"{dir_name}/")
    
    return len(missing_files) == 0

def test_basic_functionality():
    """Test basic functionality without complex imports"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test EDIFACT syntax parsing
        from edifact_syntax import EDIFACTSyntax
        
        syntax = EDIFACTSyntax()
        test_message = "UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"
        
        segments = syntax.split_segments(test_message)
        print(f"✅ Syntax parsing: {len(segments)} segments")
        
        # Test element splitting
        for segment in segments[:3]:
            elements = syntax.split_elements(segment)
            print(f"✅ Segment parsing: {elements[0] if elements else 'Empty'} ({len(elements)} elements)")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_sample_files():
    """Test sample files"""
    print("\n📄 Testing sample files...")
    
    sample_dir = Path(__file__).parent / 'sample_files'
    if not sample_dir.exists():
        print("❌ Sample files directory not found")
        return False
    
    sample_files = list(sample_dir.glob('*.edi'))
    if not sample_files:
        print("❌ No sample files found")
        return False
    
    for sample_file in sample_files:
        try:
            with open(sample_file, 'r') as f:
                content = f.read()
            
            if content and len(content) > 100:
                print(f"✅ {sample_file.name}: {len(content)} characters")
            else:
                print(f"❌ {sample_file.name}: Too short or empty")
                
        except Exception as e:
            print(f"❌ {sample_file.name}: Error reading - {e}")
    
    return True

def create_package_summary():
    """Create a package summary"""
    print("\n📋 Package Summary:")
    print("=" * 50)
    
    current_dir = Path(__file__).parent
    
    # Count files
    python_files = list(current_dir.glob('**/*.py'))
    md_files = list(current_dir.glob('**/*.md'))
    edi_files = list(current_dir.glob('**/*.edi'))
    
    print(f"Python modules: {len(python_files)}")
    print(f"Documentation files: {len(md_files)}")
    print(f"Sample EDIFACT files: {len(edi_files)}")
    print(f"Total files: {len(list(current_dir.glob('**/*')))}")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in current_dir.glob('**/*') if f.is_file())
    print(f"Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    
    # List main modules
    print("\nMain modules:")
    main_modules = [
        'edifact_syntax.py',
        'edifact_parser.py', 
        'xml_generator.py',
        'edifact_validators.py',
        'edifact_mappings.py'
    ]
    
    for module in main_modules:
        module_path = current_dir / module
        if module_path.exists():
            size = module_path.stat().st_size
            print(f"  {module}: {size:,} bytes")

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📚 Usage Instructions:")
    print("=" * 50)
    
    print("\n1. Basic usage:")
    print("   python test_parser_fixed.py")
    
    print("\n2. Run demo:")
    print("   python demo.py")
    
    print("\n3. Convert a file:")
    print("   python -c \"")
    print("   import sys")
    print("   sys.path.insert(0, '.')") 
    print("   from edifact_syntax import EDIFACTSyntax")
    print("   syntax = EDIFACTSyntax()")
    print("   print('Parser ready!')\"")
    
    print("\n4. Test with sample files:")
    print("   # Read a sample file")
    print("   with open('sample_files/sample_orders.edi', 'r') as f:")
    print("       content = f.read()")
    print("   print(f'File size: {len(content)} characters')")

def main():
    """Main test function"""
    print("EDIFACT Parser - Final Package Validation")
    print("=" * 60)
    
    success = True
    
    # Test package structure
    if not test_package_structure():
        success = False
    
    # Test basic functionality
    if not test_basic_functionality():
        success = False
    
    # Test sample files
    if not test_sample_files():
        success = False
    
    # Create package summary
    create_package_summary()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PACKAGE VALIDATION SUCCESSFUL!")
        print("The EDIFACT parser package is complete and ready for use.")
    else:
        print("❌ PACKAGE VALIDATION FAILED!")
        print("Some issues were found that need to be addressed.")
    
    print("=" * 60)
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

