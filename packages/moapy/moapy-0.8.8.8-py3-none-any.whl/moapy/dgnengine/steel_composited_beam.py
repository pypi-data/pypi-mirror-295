from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.data_pre import UnitLoads
from moapy.rc_pre import SlabSection, GirderLength
from moapy.steel_pre import SteelMember, ShearConnector
from moapy.dgnengine.base import load_dll, generate_report

@auto_schema
def report_ec3_composited_beam(steel: SteelMember, shearconn: ShearConnector, slab: SlabSection, leng: GirderLength, load: UnitLoads) -> ResultMD:
    dll = load_dll()
    json_data_list = [steel.json(), shearconn.json(), slab.json(), leng.json(), load.json()]
    return generate_report(dll, 'Report_EC4_CompositedBeam', json_data_list)

# res = report_ec3_composited_beam(SteelMember(), ShearConnector(), SlabSection(), GirderLength(), UnitLoads())
