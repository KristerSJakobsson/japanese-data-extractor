from datetime import datetime
from typing import TypeVar, Dict, Tuple, List, Any

from src.extractor.models.PostalCode import PostalCode

ExtractedDataType = Any #TypeVar('T', int, str, datetime, PostalCode)
ExtractedData = Dict[str, ExtractedDataType]
ExtractedDataPosition = Tuple[int, int]
ExtractedList = List[Tuple[ExtractedDataPosition, ExtractedData]]