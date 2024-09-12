from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enConnectionType

# ==== Steel DB ====
class SteelLength_EC(MBaseModel):
    """
    Steel DB Length
    """
    l_x: float = dataclass_field(default=3000.0, unit="length", description="Lx")
    l_y: float = dataclass_field(default=3000.0, unit="length", description="Ly")
    l_t: float = dataclass_field(default=3000.0, unit="length", description="Torsional Buckling Length")
    l_b: float = dataclass_field(default=3000.0, unit="length", description="Lateral-Torsional Buckling Length")

    class Config(MBaseModel.Config):
        title = "Steel Member Length"
        description = "Steel Member Length"

class SteelMomentModificationFactor_EC(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c1: float = dataclass_field(default=1.0, description="ratio between the critical bending moment and the critical constant bending moment for a member with hinged supports")
    c_mx: float = dataclass_field(default=1.0, description="c_mx Modification Factor")
    c_my: float = dataclass_field(default=1.0, description="c_my Modification Factor")
    c_mlt: float = dataclass_field(default=1.0, description="equivalent uniform moment factor for LTB")

    class Config(MBaseModel.Config):
        title = "Steel Moment Modification Factor"
        description = "Steel Moment Modification Factor"

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

class SteelMember(MBaseModel):
    """
    Steel Member
    """
    sect: SteelSection = dataclass_field(default=SteelSection(), description="Section")
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Member"
        description = "Steel Member"

class SteelConnectMember(MBaseModel):
    """
    Steel Connect Member
    """
    supporting: SteelMember = dataclass_field(default=SteelMember(), description="Supporting Member")
    supported: SteelMember = dataclass_field(default=SteelMember(), description="Supported Member")

    class Config(MBaseModel.Config):
        title = "Steel Connect Member"
        description = "Steel Connect Member"

class SteelBolt(MBaseModel):
    """
    Steel Bolt
    """
    name: str = dataclass_field(default='M16', description="Bolt Size")
    matl: BoltMaterial = dataclass_field(default=BoltMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Bolt"
        description = "Steel Bolt"

class ShearConnector(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt = dataclass_field(default=SteelBolt(), description="Bolt")
    num: int = dataclass_field(default=1, unit="EA", description="Number of Bolts")
    space: float = dataclass_field(default=300.0, unit="mm", description="spacing")
    length: float = dataclass_field(default=100.0, unit="mm", description="length")

    class Config(MBaseModel.Config):
        title = "Shear Connector"
        description = "Shear Connector"

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
