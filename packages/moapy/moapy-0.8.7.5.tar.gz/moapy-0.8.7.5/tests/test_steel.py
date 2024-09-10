import json
import pytest
import moapy.dgnengine.steel_bc as steel_bc
from moapy.data_pre import MemberForce
from moapy.steel_pre import SteelMaterial, SteelSection

def test_report_bc():
    res = steel_bc.report_steel_bc(matl=SteelMaterial(code='KS18(S)', name='SS275'),
                    sect=SteelSection(shape='H', name='H 400x200x8/13'),
                    load=MemberForce(Nz=1000.0, Mx=500.0, My=200.0, Vx=300.0, Vy=400.0))

def test_calc_bc():
    res = steel_bc.calc_steel_bc(matl=SteelMaterial(code='KS18(S)', name='SS275'),
                    sect=SteelSection(shape='H', name='H 400x200x8/13'),
                    load=MemberForce(Nz=1000.0, Mx=500.0, My=200.0, Vx=300.0, Vy=400.0))
