import moapy.wgsd.wgsd_oapi as wgsd_oapi
from moapy.data_pre import Force, PMOptions, AxialForceOpt, AngleOpt, DgnCode, Lcom
from moapy.rc_pre import Material, Geometry

def test_calc_mm():
    res = wgsd_oapi.calc_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(), AxialForceOpt())
    return res

def test_report_mm():
    res = wgsd_oapi.report_rc_mm_interaction_curve(Material(), Geometry(), PMOptions(), AxialForceOpt())
    return res

def test_calc_pm():
    res = wgsd_oapi.calc_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(), AngleOpt())
    return res

def test_report_pm():
    res = wgsd_oapi.report_rc_pm_interaction_curve(Material(), Geometry(), PMOptions(), AngleOpt())
    return res

def test_calc_rc_uls_stress():
    res = wgsd_oapi.calc_rc_uls_stress(Material(), Geometry(), DgnCode(), AngleOpt(), AxialForceOpt())
    return res

def test_calc_rc_uls_bending_capacity():
    res = wgsd_oapi.calc_rc_uls_bending_capacity(Material(), Geometry(), DgnCode(), AngleOpt(), AxialForceOpt())
    return res

def test_calc_calc_rc_cracked_stress():
    res = wgsd_oapi.calc_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom())
    return res

def test_report_rc_cracked_stress():
    res = wgsd_oapi.report_rc_cracked_stress(Material(), Geometry(), DgnCode(), Lcom(name="lcom", f=Force(Nz=100.0, Mx=10.0, My=50.0)))
    return res

def test_calc_rc_moment_curvature():
    res = wgsd_oapi.calc_rc_moment_curvature(Material(), Geometry())
    return res
