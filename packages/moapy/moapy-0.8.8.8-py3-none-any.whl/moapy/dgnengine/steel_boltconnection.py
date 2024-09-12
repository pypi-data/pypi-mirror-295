from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.steel_pre import SteelConnectMember, SteelPlateMember, ConnectType, SteelBolt, Welding
from moapy.dgnengine.base import generate_report, load_dll

@auto_schema
def report_ec3_bolt_connection(conn: SteelConnectMember, plate: SteelPlateMember, conType: ConnectType, Bolt: SteelBolt, weld: Welding) -> ResultMD:
    dll = load_dll()
    json_data_list = [conn.supporting.json(), conn.supported.json(), plate.json(), conType.json(), Bolt.json(), weld.json()]
    return generate_report(dll, 'Report_EC3_BoltConnection', json_data_list)

# res = report_ec3_bolt_connection(SteelConnectMember(), SteelPlateMember(), ConnectType(), SteelBolt(), Welding())
# print(res.md)