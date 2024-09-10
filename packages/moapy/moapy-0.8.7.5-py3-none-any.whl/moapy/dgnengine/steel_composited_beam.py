import ctypes
import os
from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.data_pre import UnitLoads
from moapy.rc_pre import SlabSection, GirderLength
from moapy.steel_pre import SteelMember, ShearConnector
from moapy.dgnengine.steel_bc import read_markdown_file
from moapy.mdreporter import ReportUtil

@auto_schema
def report_ec3_composited_beam(steel: SteelMember, shearconn: ShearConnector, slab: SlabSection, leng: GirderLength, load: UnitLoads) -> ResultMD:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dbg_dll', 'dgn_apid.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    steel_json = steel.json()
    shearconn_json = shearconn.json()
    slab_json = slab.json()
    leng_json = leng.json()
    load_json = load.json()

    # process_data 함수 정의 및 호출
    dll.Report_EC4_CompositedBeam.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_EC4_CompositedBeam.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_EC4_CompositedBeam(steel_json.encode('utf-8'), shearconn_json.encode('utf-8'), slab_json.encode('utf-8'), leng_json.encode('utf-8'), load_json.encode('utf-8'))
    util = ReportUtil("test.md")
    util.add_line(read_markdown_file(result))
    return ResultMD(md=util.get_md_text())

res = report_ec3_composited_beam(SteelMember(), ShearConnector(), SlabSection(), GirderLength(), UnitLoads())
