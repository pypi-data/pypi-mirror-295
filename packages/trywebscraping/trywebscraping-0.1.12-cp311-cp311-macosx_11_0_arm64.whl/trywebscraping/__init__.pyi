from typing import Dict, Any, List, Union, Callable, TypeAlias, Optional, overload
from typing_extensions import Self  # for Python <3.11

# Define a type alias for the extraction dictionary
ExtractionDict: TypeAlias = Dict[str, Union[str, Callable[[str], Any]]]

class Fetch:
    def __init__(self, url: str) -> None:
        ...
    
    def query(self, selector: str, key: Optional[str] = None) -> Self:
        ...
    
    def extract(self, extraction: ExtractionDict) -> Self:
        ...
    
    def limit(self, limit: int) -> Self:
        ...
    
    def count(self) -> int:
        ...
    
    def get_data(self) -> List[List[Dict[str, Any]]]:
        ...
    
    def reset(self) -> None:
        ...
    
    def __iter__(self) -> Self:
        ...
    
    def __next__(self) -> Optional[Dict[str, Any]]:
        ...
    
    def __len__(self) -> int:
        ...
    
    @overload
    def __getitem__(self, index: int) -> List[Dict[str, Any]]:
        ...
    
    @overload
    def __getitem__(self, index: slice) -> List[List[Dict[str, Any]]]:
        ...
    
    def __repr__(self) -> str:
        ...
    
    def __str__(self) -> str:
        ...