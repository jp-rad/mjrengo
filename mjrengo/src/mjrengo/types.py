from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Any, Match


@dataclass
class NormalizeError:
    code: str
    message: str
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "params": self.params,
        }


@dataclass
class NormalizeResult:
    success: bool
    text: str
    errors: List[NormalizeError] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "text": self.text,
            "errors": [e.to_dict() for e in self.errors],
        }


class ReplaceFn(Protocol):
    def __call__(self, m: Match[str], errors: List[NormalizeError]) -> str:
        ...
