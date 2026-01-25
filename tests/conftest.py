"""Pytest configuration and fixtures."""
import os

# Set Qt platform to offscreen for headless testing - must be set before Qt imports
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import sys
