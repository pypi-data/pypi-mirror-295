import moapy.dgnengine.steel_bc as steel_bc
import moapy.dgnengine.steel_boltconnection as steel_boltconnection
import moapy.dgnengine.steel_composited_beam as steel_composited_beam
from moapy.data_pre import MemberForce, UnitLoads, EffectiveLength
from moapy.steel_pre import SteelMaterial, SteelSection, SteelConnectMember, SteelPlateMember, ConnectType, SteelBolt, Welding, SteelMember, ShearConnector, SteelLength_EC, SteelMomentModificationFactor_EC
from moapy.rc_pre import SlabSection, GirderLength

def test_report_bc():
    res = steel_bc.report_ec3_beam_column(SteelMaterial(), SteelSection(), MemberForce(), SteelLength_EC(), EffectiveLength(), SteelMomentModificationFactor_EC())

def test_report_boltconnection():
    res = steel_boltconnection.report_ec3_bolt_connection(SteelConnectMember(), SteelPlateMember(), ConnectType(), SteelBolt(), Welding())

def test_report_composited_beam():
    res = steel_composited_beam.report_ec3_composited_beam(SteelMember(), ShearConnector(), SlabSection(), GirderLength(), UnitLoads())