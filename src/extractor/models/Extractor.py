import regex
import io
import os
from src.extractor import constants, converters
from typing import Tuple, List, Dict, Pattern, TypeVar

# For now we assume that the values returned by regex is int or str
ExtractedData = TypeVar('T', int, str)

