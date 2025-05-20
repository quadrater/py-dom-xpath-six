import os
import sys

# Add project package directory to sys.path so tests can import xpath
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE_DIR = os.path.join(ROOT, 'XPath')
if os.path.isdir(PACKAGE_DIR):
    sys.path.insert(0, PACKAGE_DIR)
