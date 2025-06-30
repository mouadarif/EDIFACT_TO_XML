#!/usr/bin/env python3
"""
Installation Script for EDIFACT Parser
======================================

This script helps install and setup the EDIFACT parser package.
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if all dependencies are available"""
    print("\n📦 Checking dependencies...")
    
    required_modules = [
        'xml.etree.ElementTree',
        'xml.dom.minidom', 
        'json',
        'csv',
        'logging',
        'datetime',
        'pathlib',
        'enum',
        'dataclasses',
        'typing'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        return False
    
    print("✅ All dependencies are available")
    return True


def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    try:
        # Add current directory to path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Test basic import
        from edifact_parser import __version__, convert_edifact_to_xml
        print(f"✅ Package import successful (version {__version__})")
        
        # Test basic functionality
        test_message = "UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"
        
        try:
            result = convert_edifact_to_xml(test_message)
            print("✅ Basic conversion test passed")
            return True
        except Exception as e:
            print(f"❌ Basic conversion test failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False


def create_shortcuts():
    """Create convenient shortcuts"""
    print("\n🔗 Creating shortcuts...")
    
    current_dir = Path(__file__).parent
    
    # Create a simple runner script
    runner_script = current_dir / "run_edifact_parser.py"
    
    runner_content = f'''#!/usr/bin/env python3
"""
EDIFACT Parser Runner
====================

Convenient script to run the EDIFACT parser.
"""

import sys
from pathlib import Path

# Add parser directory to path
parser_dir = Path(__file__).parent
sys.path.insert(0, str(parser_dir))

# Import and run CLI
from edifact_parser.cli import main

if __name__ == '__main__':
    sys.exit(main())
'''
    
    try:
        with open(runner_script, 'w') as f:
            f.write(runner_content)
        
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod(runner_script, 0o755)
        
        print(f"✅ Created runner script: {runner_script}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create runner script: {e}")
        return False


def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples:")
    print("=" * 50)
    
    examples = [
        ("Basic conversion", "python -c \"from edifact_parser import convert_edifact_to_xml; print('Parser ready!')\""),
        ("CLI help", "python -m edifact_parser.cli --help"),
        ("Convert file", "python -m edifact_parser.cli input.edi output.xml"),
        ("Run demo", "python demo.py"),
        ("Run tests", "python test_parser_fixed.py")
    ]
    
    for description, command in examples:
        print(f"\n{description}:")
        print(f"  {command}")


def main():
    """Main installation function"""
    print("EDIFACT Parser Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Test installation
    if not test_installation():
        return False
    
    # Create shortcuts
    create_shortcuts()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n" + "=" * 40)
    print("🎉 Installation completed successfully!")
    print("=" * 40)
    
    print("\nNext steps:")
    print("1. Try the demo: python demo.py")
    print("2. Run tests: python test_parser_fixed.py")
    print("3. Convert a file: python -m edifact_parser.cli sample_files/sample_orders.edi output.xml")
    print("4. Read the documentation in docs/README.md")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

