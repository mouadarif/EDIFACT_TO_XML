#!/usr/bin/env python3
"""Application runner"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
