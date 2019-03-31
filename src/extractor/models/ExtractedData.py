from datetime import datetime
from typing import TypeVar, Dict, Tuple, List

from src.extractor.models.PostalCode import PostalCode

ExtractedDataType = TypeVar('T', int, str, datetime, PostalCode)
ExtractedData = Dict[str, ExtractedDataType]
ExtractedDataPosition = Tuple[int, int]
ExtractionList = List[Tuple[ExtractedDataPosition, ExtractedData]]