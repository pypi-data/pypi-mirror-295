"""
Models for attributes.
"""
from typing import List, Optional

from pydantic.main import BaseModel

from datajunction_server.enum import StrEnum
from datajunction_server.models.node_type import NodeType

RESERVED_ATTRIBUTE_NAMESPACE = "system"


class AttributeTypeIdentifier(BaseModel):
    """
    Fields that can be used to identify an attribute type.
    """

    namespace: str = "system"
    name: str


class UniquenessScope(StrEnum):
    """
    The scope at which this attribute needs to be unique.
    """

    NODE = "node"
    COLUMN_TYPE = "column_type"


class MutableAttributeTypeFields(AttributeTypeIdentifier):
    """
    Fields on attribute types that users can set.
    """

    description: str
    allowed_node_types: List[NodeType]
    uniqueness_scope: Optional[List[UniquenessScope]]


class AttributeTypeBase(MutableAttributeTypeFields):
    """Base attribute type."""

    id: int

    class Config:  # pylint: disable=missing-class-docstring, too-few-public-methods
        orm_mode = True
