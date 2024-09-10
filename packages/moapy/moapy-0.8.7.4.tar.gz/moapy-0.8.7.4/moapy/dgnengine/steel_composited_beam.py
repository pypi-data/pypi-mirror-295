from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.data_pre import MemberForce
from moapy.steel_pre import SteelSection, SteelMaterial
from moapy.dgnengine.steel_bc import read_markdown_file
from moapy.mdreporter import ReportUtil

@auto_schema
def report_ec3_composited_beam(girder_sect: SteelSection, girder_matl: SteelMaterial, load: MemberForce) -> ResultMD: