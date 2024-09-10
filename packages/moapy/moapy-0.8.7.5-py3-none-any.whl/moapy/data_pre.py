from typing import Optional
from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enDgnCode, enEccPu, enReportType

# ==== Forces ====
class UnitLoads(MBaseModel):
    """
    Unit Loads class
    """
    construction: float = dataclass_field(default=0.0, unit="unit force", description="Construction Load")
    live: float = dataclass_field(default=0.0, unit="unit force", description="Live Load")
    finish: float = dataclass_field(default=0.0, unit="unit force", description="Finishing Load")

    class Config(MBaseModel.Config):
        title = "Unit Loads"

class MemberForce(MBaseModel):
    """Force class

    Args:
        Nz (float): Axial force
        Mx (float): Moment about x-axis
        My (float): Moment about y-axis
        Vx (float): Shear about x-axis
        Vy (float): Shear about y-axis
    """
    Nz: float = dataclass_field(default=0.0, unit="force", description="Axial force")
    Mx: float = dataclass_field(default=0.0, unit="moment", description="Moment about x-axis")
    My: float = dataclass_field(default=0.0, unit="moment", description="Moment about y-axis")
    Vx: float = dataclass_field(default=0.0, unit="force", description="Shear about x-axis")
    Vy: float = dataclass_field(default=0.0, unit="force", description="Shear about y-axis")

    class Config(MBaseModel.Config):
        title = "Member Force"
        description = "Member Force"

class Force(MBaseModel):
    """Force class

    Args:
        Nz (float): Axial force
        Mx (float): Moment about x-axis
        My (float): Moment about y-axis
    """
    Nz: float = dataclass_field(default=0.0, unit="force", description="Axial force")
    Mx: float = dataclass_field(default=0.0, unit="moment", description="Moment about x-axis")
    My: float = dataclass_field(default=0.0, unit="moment", description="Moment about y-axis")

    class Config(MBaseModel.Config):
        title = "Force"
        description = "Force class"

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: float = dataclass_field(default=0.0, unit="force", description="Axial Force")

    class Config:
        title = "Axial Force Option"

class DesignCode(MBaseModel):
    """Design Code class

    Args:
        design_code (str): Design code
        sub_code (str): Sub code
    """    
    design_code: str = dataclass_field(default="ACI 318-19", max_length=30)
    sub_code: str = dataclass_field(default="SI")

    class Config(MBaseModel.Config):
        title = "GSD Design Code"

class DgnCode(MBaseModel):
    """
    DgnCode
    """
    name: str = dataclass_field(default="", description="DgnCode")

    class Config:
        title = "DgnCode"

# ==== Lcoms ====
class Lcom(MBaseModel):
    """
    Lcom class

    Args:
        name (str): load combination name
        f (Force): load combination force
    """
    name: str = dataclass_field(default="lcom", description="load combination name")
    f: Force = dataclass_field(default=Force(), description="load combination force")

    class Config(MBaseModel.Config):
        title = "Lcom Result"

class Lcoms(MBaseModel):
    """
    Lcoms class

    Args:
        lcoms (list[Lcom]): load combination result
    """
    lcoms: list[Lcom] = dataclass_field(default=[Lcom(name="uls1", f=Force(Nz=100.0, Mx=10.0, My=50.0))], description="load combination result")

    class Config(MBaseModel.Config):
        title = "Strength Result"

class AngleOpt(MBaseModel):
    """
    Angle Option
    """
    theta: float = dataclass_field(default=0.0, unit="angle", description="theta")

    class Config:
        title = "Theta Option"

class ElasticModulusOpt(MBaseModel):
    """
    Elastic Modulus Option
    """
    E: float = dataclass_field(default=200.0, unit="stress", description="Elastic Modulus")

    class Config:
        title = "Elastic Modulus Option"

class Unit(MBaseModel):
    """
    GSD global unit class
    
    Args:
        force (str): Force unit
        length (str): Length unit
        section_dimension (str): Section dimension unit
        pressure (str): Pressure unit
        strain (str): Strain unit
    """
    force: str = dataclass_field(
        default="kN", description="Force unit")
    length: str = dataclass_field(
        default="m", description="Length unit")
    section_dimension: str = dataclass_field(
        default="mm", description="Section dimension unit")
    pressure: str = dataclass_field(
        default="MPa", description="Pressure unit")
    strain: str = dataclass_field(
        default="%", description="Strain unit")

    class Config(MBaseModel.Config):
        title = "GSD Unit"

# ==== Stress Strain Curve ====
class Stress_Strain_Component(MBaseModel):
    """Stress Strain Component class

    Args:
        stress (float): Stress
        strain (float): Strain
    """
    stress: float = dataclass_field(default=0.0, description="Stress")
    strain: float = dataclass_field(default=0.0, description="Strain")

    class Config(MBaseModel.Config):
        title = "Stress Strain Component"

# ==== Concrete Material ====
class ConcreteGrade(MBaseModel):
    """
    GSD concrete class

    Args:
        design_code (str): Design code
        grade (str): Grade of the concrete
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", description="Design code")
    grade: str = dataclass_field(
        default="C12", description="Grade of the concrete")

    class Config(MBaseModel.Config):
        title = "GSD Concrete Grade"

class Concrete_General_Properties(MBaseModel):
    """
    GSD concrete general properties for calculation
    
    Args:
        strength (int): Grade of the concrete
        elastic_modulus (float): Elastic modulus of the concrete
        density (float): Density of the concrete
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the concrete
        poisson_ratio (float): Poisson ratio of the concrete
    """
    strength: int = dataclass_field(
        gt=0, default=12, description="Grade of the concrete")
    elastic_modulus: float = dataclass_field(
        gt=0, default=30000, description="Elastic modulus of the concrete")
    density: float = dataclass_field(
        gt=0, default=2400, description="Density of the concrete")
    thermal_expansion_coefficient: float = dataclass_field(
        gt=0, default=0.00001, description="Thermal expansion coefficient of the concrete")
    poisson_ratio: float = dataclass_field(
        gt=0, default=0.2, description="Poisson ratio of the concrete")

    class Config(MBaseModel.Config):
        title = "GSD Concrete General Properties"

class Concrete_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        factor_b1 (float): Plastic strain limit for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", description="Material model for ULS")
    factor_b1: float = dataclass_field(
        default=0.85, description="Plastic strain limit for ULS")
    compressive_failure_strain: float = dataclass_field(
        default=0.003, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "GSD Concrete Stress Options for ULS"

class Concrete_Stress_ULS_Options_Eurocode(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        partial_factor_case (float): Partial factor case for ULS
        partial_factor (float): Partial factor for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", description="Material model for ULS")
    partial_factor_case: float = dataclass_field(
        default=1.0, description="Partial factor case for ULS")
    partial_factor: float = dataclass_field(
        default=1.5, description="Partial factor for ULS")
    compressive_failure_strain: float = dataclass_field(
        default=0.003, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "GSD Concrete Stress Options for ULS"

class Concrete_SLS_Options(MBaseModel):
    """
    GSD concrete stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        plastic_strain_limit (float): Plastic strain limit for SLS
        failure_compression_limit (float): Failure compression limit for SLS
        material_model_tension (str): Material model for SLS tension
        failure_tension_limit (float): Failure tension limit for SLS
    """
    material_model: str = dataclass_field(
        default="Linear", description="Material model for SLS")
    plastic_strain_limit: float = dataclass_field(
        default=0.002, description="Plastic strain limit for SLS")
    failure_compression_limit: float = dataclass_field(
        default=0.003, description="Failure compression limit for SLS")
    material_model_tension: str = dataclass_field(
        default="interpolated", description="Material model for SLS tension")
    failure_tension_limit: float = dataclass_field(
        default=0.003, description="Failure tension limit for SLS")

    class Config(MBaseModel.Config):
        title = "GSD Concrete Stress Options for SLS"

# ==== Rebar & Tendon Materials ====
class RebarGrade(MBaseModel):
    """
    GSD rebar grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the rebar
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", description="Design code")
    grade: str = dataclass_field(
        default="Grade 420", description="Grade of the rebar")

    class Config(MBaseModel.Config):
        title = "GSD Rebar Grade"

class TendonGrade(MBaseModel):
    """
    GSD Tendon grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the tendon
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", description="Design code")
    grade: str = dataclass_field(default="Grade 420", description="Grade of the tendon")

    class Config(MBaseModel.Config):
        title = "GSD Tendon Grade"

class RebarProp(MBaseModel):
    """
    GSD rebar prop
    
    Args:
        area (float): Area of the rebar
        material (RebarGrade): Material of the rebar
    """
    area: float = dataclass_field(default=287.0, description="Area of the rebar")
    material: RebarGrade = dataclass_field(default=RebarGrade(), description="Material of the rebar")

    class Config(MBaseModel.Config):
        title = "GSD Rebar Properties"

class TendonProp(MBaseModel):
    """
    GSD Tendon prop
    
    Args:
        area (float): Area of the tendon
        material (TendonGrade): Material of the tendon
        prestress (float): Prestress of the tendon
    """
    area: float = dataclass_field(default=287.0, description="Area of the tendon")
    material: TendonGrade = dataclass_field(default=TendonGrade(), description="Material of the tendon")
    prestress: float = dataclass_field(default=0.0, description="Prestress of the tendon")

    class Config(MBaseModel.Config):
        title = "GSD Tendon Properties"

class Rebar_General_Properties(MBaseModel):
    """
    GSD rebar general properties for calculation
    
    Args:
        strength (int): Grade of the rebar
        elastic_modulus (float): Elastic modulus of the rebar
        density (float): Density of the rebar
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the rebar
        poisson_ratio (float): Poisson ratio of the rebar
    """
    strength: int = dataclass_field(
        default=420, description="Grade of the rebar")
    elastic_modulus: float = dataclass_field(
        default=200000, description="Elastic modulus of the rebar")
    density: float = dataclass_field(
        default=7850, description="Density of the rebar")
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, description="Thermal expansion coefficient of the rebar")
    poisson_ratio: float = dataclass_field(
        default=0.3, description="Poisson ratio of the rebar")

    class Config(MBaseModel.Config):
        title = "GSD Rebar General Properties"

class Rebar_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD rebar stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", description="Material model for ULS")
    failure_strain: float = dataclass_field(
        default=0.7, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "GSD Rebar Stress Options for ULS"

class Rebar_Stress_SLS_Options(MBaseModel):
    """
    GSD rebar stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        failure_strain (float): Failure strain limit for SLS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", description="Material model for SLS")
    failure_strain: float = dataclass_field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})

    class Config(MBaseModel.Config):
        title = "GSD Rebar Stress Options for SLS"

class MaterialRebar(MBaseModel):
    """
    GSD rebar class
    
    Args:
        grade (RebarGrade): Grade of the rebar
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    grade: RebarGrade = dataclass_field(
        default=RebarGrade(), description="Grade of the rebar")
    curve_uls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "GSD Material Rebar"

class MaterialTendon(MBaseModel):
    """
    GSD tendon class
    
    Args:
        grade (TendonGrade): Grade of the tendon
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    grade: TendonGrade = dataclass_field(default=TendonGrade(), description="Grade of the tendon")
    curve_uls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "GSD Material Tendon"

class MaterialConcrete(MBaseModel):
    """
    GSD material for Concrete class
    
    Args:
        grade (ConcreteGrade): Grade of the concrete
        curve_uls (list[Stress_Strain_Component]): Stress strain curve concrete ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve
    """
    grade: ConcreteGrade = dataclass_field(
        default=ConcreteGrade(), description="Grade of the concrete")
    curve_uls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = dataclass_field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "GSD Material Concrete"

class Material(MBaseModel):
    """
    GSD concrete class

    Args:
        concrete (MaterialConcrete): Concrete properties
        rebar (MaterialRebar): Rebar properties
        tendon (MaterialTendon): Tendon properties
    """
    concrete: MaterialConcrete = dataclass_field(default=MaterialConcrete(), description="Concrete properties")
    rebar: Optional[MaterialRebar] = dataclass_field(default=MaterialRebar(), description="Rebar properties")
    tendon: Optional[MaterialTendon] = dataclass_field(default=MaterialTendon(), description="Tendon properties")

    def __post_init__(self):
        if self.rebar is None and self.tendon is None:
            raise ValueError("Either rebar or tendon must be provided.")

    class Config(MBaseModel.Config):
        title = "GSD Material"

# ==== Geometry ====
class Point(MBaseModel):
    """
    Point class
    
    Args:
        x (float): x-coordinate
        y (float): y-coordinate
    """
    x: float
    y: float

    class Config(MBaseModel.Config):
        title = "Point"

class Points(MBaseModel):
    """
    GSD Points class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = dataclass_field(default=[Point(x=0.0, y=0.0), Point(x=400.0, y=0.0), Point(x=400.0, y=600.0), Point(x=0.0, y=600.0)], description="Points")

    class Config(MBaseModel.Config):
        title = "GSD Points"

class OuterPolygon(MBaseModel):
    """
    GSD Outer Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = dataclass_field(default=[Point(x=0.0, y=0.0), Point(x=400.0, y=0.0), Point(x=400.0, y=600.0), Point(x=0.0, y=600.0)], description="Outer Polygon")

    class Config(MBaseModel.Config):
        title = "GSD Outer Polygon"

class InnerPolygon(MBaseModel):
    """
    GSD Inner Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = dataclass_field(default=[Point(x=0.0, y=0.0), Point(x=400.0, y=0.0), Point(x=400.0, y=600.0), Point(x=0.0, y=600.0)], description="Inner Polygon")

    class Config(MBaseModel.Config):
        title = "GSD Inner Polygon"

class ConcreteGeometry(MBaseModel):
    """
    GSD concrete geometry class
    
    Args:
        material (ConcreteGrade): Material of the concrete
        outerPolygon (list[Point]): Outer polygon of the concrete
        innerPolygon (list[Point]): Inner polygon of the concrete
    """
    material: ConcreteGrade = dataclass_field(default=ConcreteGrade(), description="Material of the concrete")
    outerPolygon: list[Point] = dataclass_field(default=[Point(x=0.0, y=0.0), Point(x=400.0, y=0.0), Point(x=400.0, y=600.0), Point(x=0.0, y=600.0)], description="Outer polygon of the concrete")
    innerPolygon: list[Point] = dataclass_field(default=[Point(x=80.0, y=80.0), Point(x=320.0, y=80.0), Point(x=320.0, y=520.0), Point(x=80.0, y=520.0)], description="Inner polygon of the concrete")

    class Config(MBaseModel.Config):
        title = "GSD Concrete Geometry"

class RebarGeometry(MBaseModel):
    """
    GSD rebar geometry class

    Args:
        prop (RebarProp): properties of the rebar
        points (list[Point]): Rebar Points
    """
    prop: RebarProp = dataclass_field(default=RebarProp(), description="properties of the rebar")
    points: list[Point] = dataclass_field(default=[Point(x=40.0, y=40.0), Point(x=360.0, y=40.0), Point(x=360.0, y=560.0), Point(x=40.0, y=560.0)], description="Rebar Points")

    class Config(MBaseModel.Config):
        title = "GSD Rebar Geometry"

class TendonGeometry(MBaseModel):
    """
    GSD tendon geometry class
    
    Args:
        prop (TendonProp): properties of the tendon
        points (list[Point]): Tendon Points
    """
    prop: TendonProp = dataclass_field(default=TendonProp(), description="properties of the tendon")
    points: list[Point] = dataclass_field(default=[], description="Tendon Points")

    class Config(MBaseModel.Config):
        title = "GSD Tendon Geometry"

class Geometry(MBaseModel):
    """
    GSD geometry class
    
    Args:
        concrete (ConcreteGeometry): Concrete geometry
        rebar (RebarGeometry): Rebar geometry
        tendon (TendonGeometry): Tendon geometry
    """
    concrete: ConcreteGeometry = dataclass_field(default=ConcreteGeometry(), description="Concrete geometry")
    rebar: Optional[RebarGeometry] = dataclass_field(default=RebarGeometry(), description="Rebar geometry")
    tendon: Optional[TendonGeometry] = dataclass_field(default=TendonGeometry(), description="Tendon geometry")

    class Config(MBaseModel.Config):
        title = "GSD Geometry"

class Lcb(MBaseModel):
    """
    GSD load combination class
    
    Args:
        uls (Lcoms): uls load combination
    """
    uls: Lcoms = dataclass_field(default=Lcoms(), description="uls load combination")

    class Config(MBaseModel.Config):
        title = "GSD Load Combination"

# ==== options ====
class PMOptions(MBaseModel):
    """
    GSD options class
    
    Args:
        dgncode (str): Design code
        by_ecc_pu (str): ecc
    """
    dgncode: str = dataclass_field(default=enDgnCode.Eurocode2_04, description="Design code", enum=enum_to_list(enDgnCode))
    by_ecc_pu: str = dataclass_field(default="ecc", description="ecc or P-U", enum=enum_to_list(enEccPu))

    class Config(MBaseModel.Config):
        title = "GSD Options"

class ReportType(MBaseModel):
    """
    Report Type class
    
    Args:
        report_type (str): Report type
    """
    type: str = dataclass_field(default="markdown", description="Report type", enum=enum_to_list(enReportType))

    class Config(MBaseModel.Config):
        title = "Report Type"