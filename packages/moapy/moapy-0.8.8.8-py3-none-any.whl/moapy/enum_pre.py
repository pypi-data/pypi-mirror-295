from enum import Enum

# Enum 값을 리스트로 변환하는 함수
def enum_to_list(enum_class):
    return [member.value for member in enum_class]

class enDgnCode(Enum):
    """
    Enum for Design Code
    """
    ACI318M_19 = "ACI318M-19"
    Eurocode2_04 = "Eurocode2-04"

class enEccPu(Enum):
    """
    Enum for Design Code
    """
    ecc = "ecc"
    p_u = "P-U"

class enReportType(Enum):
    """
    Enum for Report Type
    """
    text = "text"
    markdown = "markdown"

# ---- Steel ----
class enConnectionType(Enum):
    """
    Enum for Connection Type
    """
    Fin_B_B = "Fin Plate - Beam to Beam"
    Fin_B_C = "Fin Plate - Beam to Column"
    End_B_B = "End Plate - Beam to Beam"
    End_B_C = "End Plate - Beam to Column"