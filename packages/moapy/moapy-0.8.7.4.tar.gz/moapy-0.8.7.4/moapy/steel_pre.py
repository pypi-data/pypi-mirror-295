from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enConnectionType

# ==== Steel DB ====
class SteelSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = dataclass_field(default='H', description="Shape")
    name: str = dataclass_field(default='H 400x200x8/13', description="Section Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Section"
        description = "Steel DB Section"

class SteelMaterial(MBaseModel):
    """
    Steel DB Material
    """
    code: str = dataclass_field(default='KS18(S)', description="Material Code")
    name: str = dataclass_field(default='SS275', description="Material Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Material"
        description = "Steel DB Material"

class BoltMaterial(MBaseModel):
    """
    Bolt Material
    """
    name: str = dataclass_field(default='F10T', description="Bolt Material Name")

    class Config(MBaseModel.Config):
        title = "Bolt Material"
        description = "Bolt Material"

class SteelSupportingMember(MBaseModel):
    """
    Steel Supporting Member
    """
    sect: SteelSection = dataclass_field(default=SteelSection(), description="Section")
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Supporting Member"
        description = "Steel Supporting Member"

class SteelSupportedMember(MBaseModel):
    """
    Steel Supported Member
    """
    sect: SteelSection = dataclass_field(default=SteelSection(), description="Section")
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Supported Member"
        description = "Steel Supported Member"

class SteelBolt(MBaseModel):
    """
    Steel Bolt
    """
    name: str = dataclass_field(default='M16', description="Bolt Size")
    matl: BoltMaterial = dataclass_field(default=BoltMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Bolt"
        description = "Steel Bolt"

class Welding(MBaseModel):
    """
    Welding
    """
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")
    length: float = dataclass_field(default=6.0, unit="mm", description="Leg of Length")

    class Config(MBaseModel.Config):
        title = "Welding"
        description = "Welding"

class SteelPlateMember(MBaseModel):
    """
    Steel Plate Member
    """
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")
    bolt_num: int = dataclass_field(default=4, unit="EA", description="Number of Bolts")
    thk: float = dataclass_field(default=6.0, unit="mm", description="Thickness")

    class Config(MBaseModel.Config):
        title = "Steel Plate Member"
        description = "Steel Plate Member"

class ConnectType(MBaseModel):
    """
    Connect Type class

    Args:
        type (str): Connection type
    """
    type: str = dataclass_field(default="Fin Plate - Beam to Beam", description="Connect type", enum=enum_to_list(enConnectionType))

    class Config(MBaseModel.Config):
        title = "Connection Type"
