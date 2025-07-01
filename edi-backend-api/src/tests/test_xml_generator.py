import unittest
import sys
from pathlib import Path
import re # Ensure re is imported if used directly by test utility, though _sanitize_xml_tag_name uses it

# Adjust path to import from the root package (app)
# This assumes 'app' is the effective package name as established in previous steps
# For local testing, if 'tests' is a subdir of 'app', '..' might be needed
# Or, if PYTHONPATH is set to '/', then 'from app.xml_generator import XMLGenerator'
# Given the successful execution path, we assume 'app' is the package name.

# To make this runnable standalone and also via a test runner from project root:
# We need to ensure 'app' (the project root) is in sys.path
# This is tricky for unit tests. A common way is to have a test runner setup PYTHONPATH
# or the tests are structured as part of the package.
# For now, let's assume this test will be run from the project root,
# and the XMLGenerator can be imported via the package 'app'.

# Simplified import for subtask environment, assuming 'app' package context
# The subtask environment might need to adjust this if it runs tests differently.
# The core logic is to get XMLGenerator.
# try:
    # This path assumes the 'app' directory (project root) is in PYTHONPATH
    # as per the successful execution strategy (PYTHONPATH="/", then 'app.module')
    # When running 'python -m unittest tests.test_xml_generator' from project root,
    # if project root is 'app', this should work.
    # from app.xml_generator import XMLGenerator # This was incorrect for current structure
# except ImportError:
    # Fallback for environments where 'app' is not directly in path,
    # but the script is in 'tests/' and 'xml_generator.py' is in parent.
    # This is less ideal for package structures but can work for simple execution.
    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # No longer needed
    # try:
        # from xml_generator import XMLGenerator # Assumes xml_generator.py is in root
    # except ImportError as e:
        # raise ImportError(f"Could not import XMLGenerator. Ensure PYTHONPATH is set correctly or test structure matches. Original error: {e}")

from src.xml_generator import XMLGenerator


class TestXMLGeneratorSanitizeTagName(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an instance of XMLGenerator to access the method
        # We don't need a specific config for just testing sanitize method
        cls.generator = XMLGenerator()
        # The method is protected, access it via name mangling for testing,
        # or make a public static helper if preferred in actual code.
        # For testing, this is acceptable:
        cls.sanitize = cls.generator._sanitize_xml_tag_name

    def test_valid_names(self):
        self.assertEqual(self.sanitize("ElementName"), "ElementName")
        self.assertEqual(self.sanitize("Element_Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element-Name"), "Element-Name")
        self.assertEqual(self.sanitize("Element.Name"), "Element.Name")
        self.assertEqual(self.sanitize("_ElementName"), "_ElementName")
        self.assertEqual(self.sanitize("E123"), "E123")

    def test_spaces_and_commas(self):
        self.assertEqual(self.sanitize("Element Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element,Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element Name, With Comma"), "Element_Name_With_Comma")

    def test_various_separators(self):
        # From regex: r"[\s,:;()\/?#*']+"
        self.assertEqual(self.sanitize("Element:Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element;Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element(Name)"), "Element_Name_") # () replaced by _
        self.assertEqual(self.sanitize("Element/Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element?Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element#Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element*Name"), "Element_Name")
        self.assertEqual(self.sanitize("Element'Name"), "Element_Name")

    def test_leading_invalid_chars(self):
        self.assertEqual(self.sanitize("1ElementName"), "Element_1ElementName") # Default prefix "Element"
        self.assertEqual(self.sanitize("-ElementName"), "Element_-ElementName")
        self.assertEqual(self.sanitize(".ElementName"), "Element_.ElementName")
        self.assertEqual(self.sanitize("123"), "Element_123")
        self.assertEqual(self.sanitize("_123Name"), "_123Name") # Already starts with underscore

    def test_other_invalid_chars_stripped(self):
        # From regex: r"[^a-zA-Z0-9_.-]" (now includes hyphen)
        self.assertEqual(self.sanitize("Element!Name@"), "ElementName") # !, @ stripped
        self.assertEqual(self.sanitize("Element<Value>"), "ElementValue") # <, > stripped by second regex
        self.assertEqual(self.sanitize("Element<Value>", default_prefix="Tag"), "ElementValue") # Prefix not applied if result is valid


    def test_empty_and_default_prefix(self):
        self.assertEqual(self.sanitize(""), "ElementUnnamed") # Default prefix "Element"
        self.assertEqual(self.sanitize("", default_prefix="Tag"), "TagUnnamed")
        self.assertEqual(self.sanitize("___", default_prefix="Tag"), "TagSanitizedEmpty")
        self.assertEqual(self.sanitize("   ", default_prefix="Test"), "Test_") # "   " -> "" -> prefixed "Test_"

    def test_name_that_becomes_invalid_after_strip(self):
        # Example: "---" -> "---" (by first re.sub if - was in it, or stays "---")
        # Then, if it was "---", it becomes "---" (second re.sub keeps it)
        # Then, prepended with "Element_" because it starts with "-". -> "Element_---"
        # The current first regex `r"[\s,:;()\/?#*']+"` does *not* include hyphen.
        # The second regex `[^a-zA-Z0-9_.]` *allows* hyphen.
        # So "---Test" -> "---Test" -> "Element_---Test" (correct)
        self.assertEqual(self.sanitize("---Test"), "Element_---Test")
        self.assertEqual(self.sanitize("1---Test", default_prefix="Pfx"), "Pfx_1---Test")

    def test_complex_name(self):
        name = "Document/Message Name, Coded (Official)"
        # Expected: Document_Message_Name_Coded_Official_
        # Current first regex: r"[\s,:;()\/?#*']+" -> replaces space, /, ,, (, ) with _
        # "Document_Message_Name_Coded_Official_" (multiple consecutive separators become one _)
        # Second regex keeps this. Start is valid.
        self.assertEqual(self.sanitize(name), "Document_Message_Name_Coded_Official_")

    def test_double_quotes_and_hyphens(self):
        # The current main sanitizing regex: r"[\s,:;()\/?#*']+"
        # It does NOT include double quotes (") or hyphens (-).
        # The second regex `[^a-zA-Z0-9_.]` allows hyphens and periods, but strips double quotes.
        self.assertEqual(self.sanitize("Test-Name"), "Test-Name") # Hyphen allowed
        self.assertEqual(self.sanitize("Test\"Name"), "TestName")   # Double quote stripped by second regex

if __name__ == '__main__':
    unittest.main()
