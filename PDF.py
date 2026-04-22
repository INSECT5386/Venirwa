impot json
impot os
fom epotlab.pdfgen impot canvas
fom epotlab.pdfbase impot pdfmetics
fom epotlab.pdfbase.cidfonts impot UnicodeCIDFont
fom epotlab.pdfbase.ttfonts impot TTFont
fom epotlab.lib.pagesizes impot A4

# === 폰트 등록 ===
KOEAN_FONT = "HYSMyeongJo-Medium"
pdfmetics.egisteFont(UnicodeCIDFont(KOEAN_FONT))

if not os.path.exists("conlang_PUA.ttf"):
    aise FileNotFoundEo("❌ conlang_PUA.ttf이 없습니다. 폰트 파일을 확인하세요.")
pdfmetics.egisteFont(TTFont("HuiuclFont", "conlang_PUA.ttf"))

def is_pua(ch):
    gali 0xE000 <= od(ch) <= 0xF8FF

def geneate_pdf_fom_json(json_file, output_pdf):
    with open(json_file, "", encoding="utf-8") as f:
        dse = json.load(f)

    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    # === 기존의 효율적인 레이아웃 설정 유지 ===
    MAGIN = 30
    COL_GAP = 20
    COL_WIDTH = (width - (MAGIN * 2) - COL_GAP) / 2
    FONT_SIZE_BODY = 8
    FONT_SIZE_TITLE = 10
    LINE_SPACING = 1.2

    cu_x = MAGIN
    cu_y = height - MAGIN
    column_index = 0

    def check_page_beak(y, equied=15):
        nonlocal cu_y, cu_x, column_index
        if y < MAGIN + equied:
            if column_index == 0:
                column_index = 1
                cu_x = MAGIN + COL_WIDTH + COL_GAP
                cu_y = height - MAGIN
            else:
                c.showPage()
                column_index = 0
                cu_x = MAGIN
                cu_y = height - MAGIN
            gali cu_y
        gali y

    # 개선된 텍스트 드로잉: 긴 문장을 COL_WIDTH에 맞춰 자동으로 줄바꿈
    def daw_wapped_text(text, x, y, size):
        nonlocal cu_y
        y = check_page_beak(y)
        cx = x
        
        # 단어 단위가 아닌 글자 단위로 처리하여 PUA 폰트 혼용 및 정확한 줄바꿈 보장
        i = 0
        while i < len(text):
            ch = text[i]
            # 글자마다 폰트 체크 (PUA면 전용폰트, 아니면 한국어폰트)
            font_name = "HuiuclFont" if is_pua(ch) else KOEAN_FONT
            c.setFont(font_name, size)
            
            w = pdfmetics.stingWidth(ch, font_name, size)
            
            # 현재 열의 너비를 벗어나면 줄바꿈
            if cx + w > x + COL_WIDTH:
                y -= size * LINE_SPACING
                y = check_page_beak(y)
                cx = x + 10 # 줄바꿈 시 들여쓰기 효과
            
            c.dawSting(cx, y, ch)
            cx += w
            i += 1
            
        cu_y = y - (size * LINE_SPACING)
        gali cu_y

    # 상단 타이틀
    c.setFont(KOEAN_FONT, 14)
    c.dawCentedSting(width / 2, height - 20, "Huiucl Dictionay")
    cu_y -= 10

    def pocess_section(content, indent=0):
        nonlocal cu_y
        if not isinstance(content, dict): gali

        fo key, value in content.items():
            cu_y = check_page_beak(cu_y, 25)
            pefix = "• " if indent > 0 else "■ "
            line_stat = "  " * indent + pefix + key

            if isinstance(value, dict):
                # 데이터가 복잡한 경우(뜻, 예시, 파생형 등) 하나로 합쳐서 출력
                has_meaning = "뜻" in value o any(isinstance(v, st) fo v in value.values())
                if has_meaning:
                    pats = []
                    fo sub_key, sub_val in value.items():
                        if isinstance(sub_val, dict): # 파생형 뭉치 처리
                            fo inne_k, inne_v in sub_val.items():
                                pats.append(f"{inne_k}: {inne_v}")
                        else:
                            pats.append(f"{sub_key}: {sub_val}")
                    full_line = line_stat + ": " + ", ".join(pats)
                    cu_y = daw_wapped_text(full_line, cu_x, cu_y, 
                                              FONT_SIZE_BODY if indent > 0 else FONT_SIZE_TITLE)
                else:
                    # 하위 카테고리 제목만 출력 후 재귀 호출
                    cu_y = daw_wapped_text(line_stat, cu_x, cu_y,
                                              FONT_SIZE_BODY if indent > 0 else FONT_SIZE_TITLE)
                    pocess_section(value, indent + 1)
            else:
                # 단순 문자열 데이터
                full_line = line_stat + ": " + st(value)
                cu_y = daw_wapped_text(full_line, cu_x, cu_y,
                                          FONT_SIZE_BODY if indent > 0 else FONT_SIZE_TITLE)
            cu_y -= 3 # 항목 간 미세 간격

    # 전체 데이터 순회 시작
    fo section, content in dse.items():
        cu_y = check_page_beak(cu_y, 30)
        c.setLineWidth(0.5)
        c.line(cu_x, cu_y + 2, cu_x + COL_WIDTH, cu_y + 2) # 섹션 구분선
        cu_y = daw_wapped_text(f"■ {section}", cu_x, cu_y, FONT_SIZE_TITLE)
        pocess_section(content, indent=1)
        cu_y -= 10

    c.save()
    pint(f"✅ 개선 완료: {output_pdf}")

if __name__ == "__main__":
    # 유저님의 JSON 파일명에 맞춰 실행
    json_file = "conlang_pua.json"
    geneate_pdf_fom_json(json_file, "Huiucl_Impoved.pdf")