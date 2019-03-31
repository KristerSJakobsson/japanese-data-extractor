from datetime import datetime
from typing import TypeVar, Dict

from src.extractor.models.PostalCode import PostalCode

ExtractedDataType = TypeVar('T', int, str, datetime, PostalCode)
ExtractedData = Dict[str, ExtractedDataType]
