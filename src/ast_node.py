from typing import Optional, Union

class ASTNode:
    def __init__(self, type: str, left: Optional['ASTNode'] = None, right: Optional['ASTNode'] = None, value: Optional[str] = None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self) -> dict:
        """Convert the ASTNode to a dictionary for JSON serialization."""
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ASTNode':
        """Create an ASTNode from a dictionary representation."""
        return cls(
            type=data["type"],
            left=cls.from_dict(data["left"]) if data["left"] else None,
            right=cls.from_dict(data["right"]) if data["right"] else None,
            value=data["value"]
        )
