import pypandoc
import os
import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import MemberForce, EffectiveLength
from moapy.data_post import ResultMD
from moapy.steel_pre import SteelMaterial, SteelSection, SteelLength_EC, SteelMomentModificationFactor_EC
from moapy.dgnengine.base import generate_report, load_dll
import re

def remove_html_blocks(markdown_content):
    # HTML 블록을 제거하기 위한 정규 표현식
    html_block_pattern = re.compile(r'```{=html}\s*<!--\s*-->\s*```', re.DOTALL)
    # 해당 패턴을 빈 문자열로 대체하여 제거
    cleaned_content = re.sub(html_block_pattern, '', markdown_content)
    
    # 또는 주석 부분만 제거하는 경우, 주석 패턴을 찾고 제거
    cleaned_content = re.sub(r'```{=html}\s*', '', cleaned_content)
    cleaned_content = re.sub(r'\s*<!--\s*-->\s*```', '', cleaned_content)

    return cleaned_content

def rtf_to_markdown(file_path):
    # 파일 경로가 bytes로 주어진 경우 문자열로 변환
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # RTF 파일을 Markdown으로 변환
        markdown_content = pypandoc.convert_file(file_path, 'md', format='rtf', extra_args=['--strip-comments'])

        # EMF 이미지 데이터를 찾기 위한 정규 표현식
        emf_pattern = re.compile(r'\\pict\\emfblip(.*?)\\bin', re.DOTALL)
        emf_matches = emf_pattern.findall(markdown_content)

        # EMF 데이터를 base64로 변환
        for match in emf_matches:
            emf_data = match.strip().replace('\n', '').replace('\r', '').replace(' ', '')
            # 16진수 문자열을 바이너리 데이터로 변환
            emf_bytes = bytes.fromhex(emf_data)
            # base64로 인코딩
            base64_emf = base64.b64encode(emf_bytes).decode('utf-8')
            # Markdown 이미지 태그 생성
            markdown_image = f'![EMF Image](data:image/emf;base64,{base64_emf})'
            # 원본 EMF 데이터를 Markdown 이미지 태그로 교체
            markdown_content = markdown_content.replace(match, markdown_image)

        # 불필요한 HTML 블록 제거 (```{=html} <!-- --> ``` 형식)
        markdown_content = remove_html_blocks(markdown_content)

        return markdown_content

    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error converting RTF to Markdown: {e}")

def read_txt_file(file_path):
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    # 파일 경로 검증
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # 파일 열기 및 내용 읽기
        with open(file_path, 'r', encoding='utf-16') as file:
            file_content = file.read()
        return file_content
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

@auto_schema
def report_ec3_beam_column(matl: SteelMaterial, sect: SteelSection, load: MemberForce, length: SteelLength_EC, eff_len: EffectiveLength, factor: SteelMomentModificationFactor_EC) -> ResultMD:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    return generate_report(dll, 'Report_EC3_BeamColumn', json_data_list)

# res = report_ec3_beam_column(SteelMaterial(code='KS18(S)', name='SS275'), SteelSection(shape='H', name='H 400x200x8/13'), MemberForce(Nz=1000.0, Mx=500.0, My=200.0, Vx=300.0, Vy=400.0), SteelLength_EC(Lb=3000.0), EffectiveLength(Lx=3000.0, Ly=3000.0), SteelMomentModificationFactor_EC(c1=1.0, c_mx=1.0, c_my=1.0, c_mlt=1.0))