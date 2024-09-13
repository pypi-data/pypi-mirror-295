from typing import Dict, Any, Union, Callable, TypeAlias, Optional
from typing_extensions import Self  # for Python <3.11

# Define a type alias for the extraction dictionary
ExtractionDict: TypeAlias = Dict[str, Union[str, Callable[[str], Any]]]

class Fetch:
    def __init__(self, url: str) -> None:
        ...
    
    def query(self, selector: str, key: Optional[str] = None) -> Fetch:
        ...
    
    def extract(self, extraction: ExtractionDict) -> Fetch:
        ...
    
    def limit(self, limit: int) -> Fetch:
        ...
    
    def get_data(self) -> Any:  # Returns PyObject, which could be a single list or a nested list
        ...
    
    def count(self) -> int:
        ...
    
    def __getitem__(self, index: int) -> list:  # Always returns a list
        ...
    
    def __repr__(self) -> str:
        ...
    
    def __str__(self) -> str:
        ...