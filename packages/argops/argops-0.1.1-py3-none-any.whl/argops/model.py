"""Define the data models of the program."""

import logging
from typing import Any, List, Tuple

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class YamlDiff(BaseModel):
    """Model of a difference between two yaml source files."""

    unchanged: List[Tuple[str, Any]] = Field(default_factory=list)
    new: List[Tuple[str, Any]] = Field(default_factory=list)
    changed: List[Tuple[str, Any]] = Field(default_factory=list)
    deleted: List[str] = Field(default_factory=list)
