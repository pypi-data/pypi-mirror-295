from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
# from moapy.enum_pre import enum_to_list

class SlabSection(MBaseModel):
    """
    Slab
    """
    thickness: float = dataclass_field(default=150.0, unit="length", description="Thickness")

    class Config(MBaseModel.Config):
        title = "Slab"
        description = "Slab"

class GirderLength(MBaseModel):
    """
    Girder Length
    """
    span: float = dataclass_field(default=10.0, unit="length", description="Span Length")
    spacing: float = dataclass_field(default=3.0, unit="length", description="Spacing")

    class Config(MBaseModel.Config):
        title = "Girder Length"
        description = "Girder Length"