from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class PetStatus(str, Enum):
  AVAILABLE = "available"
  PENDING = "pending"
  SOLD = "sold"

  def __str__(self):
    return self.value

  def __repr__(self):
    return self.value

@dataclass
class Category:
  id: Optional[int] = None
  name: Optional[str] = None

@dataclass
class Tag:
  id: Optional[int] = None
  name: Optional[str] = None

@dataclass
class Pet:
  id: Optional[int] = None
  category: Optional[Category] = None
  name: Optional[str] = None
  photo_urls: Optional[List[str]] = field(default_factory=list)
  tags: Optional[List[Tag]] = field(default_factory=list)
  status: Optional[str] = None
