import ctypes
import os
from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.steel_pre import SteelSupportingMember, SteelSupportedMember, SteelPlateMember, ConnectType, SteelBolt, Welding
from moapy.dgnengine.steel_bc import read_markdown_file
from moapy.mdreporter import ReportUtil

@auto_schema
def report_ec3_bolt_connection(supporting: SteelSupportingMember, supported: SteelSupportedMember, plate: SteelPlateMember, conType: ConnectType, Bolt: SteelBolt, weld: Welding) -> ResultMD:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)

    # JSON 데이터를 변환
    supporting_json = supporting.json()
    supported_json = supported.json()
    plate_json = plate.json()
    conType_json = conType.json()
    Bolt_json = Bolt.json()
    weld_json = weld.json()

    # process_data 함수 정의 및 호출
    dll.Report_EC3_BoltConnection.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    dll.Report_EC3_BoltConnection.restype = ctypes.c_char_p

    # JSON 데이터를 인코딩해서 전달
    result = dll.Report_EC3_BoltConnection(supporting_json.encode('utf-8'), supported_json.encode('utf-8'), plate_json.encode('utf-8'), conType_json.encode('utf-8'), Bolt_json.encode('utf-8'), weld_json.encode('utf-8'))
    util = ReportUtil("test.md")
    util.add_line(read_markdown_file(result))
    return ResultMD(md=util.get_md_text())

# res = report_ec3_bolt_connection(SteelSupportingMember(), SteelSupportedMember(), SteelPlateMember(), ConnectType(), SteelBolt(), Welding())
# print(res.md)