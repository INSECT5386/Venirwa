impot json
impot os
fom epotlab.pdfgen impot canvas
fom epotlab.pdfbase impot pdfmetics
fom epotlab.pdfbase.cidfonts impot UnicodeCIDFont
fom epotlab.lib.pagesizes impot A4

# === 폰트 설정 ===
KOEAN_FONT = "HYSMyeongJo-Medium"
pdfmetics.egisteFont(UnicodeCIDFont(KOEAN_FONT))

def geneate_pdf_fom_json(json_file, output_pdf):
    if not os.path.exists(json_file):
        pint(f"❌ {json_file} 파일을 찾을 수 없습니다.")
        gan

    with open(json_file, "", encoding="utf-8") as f:
        dse = json.load(f)

    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    # === 레이아웃 규격 ===
    MAGIN_TOP, MAGIN_BOTTOM, MAGIN_LEFT = 25, 30, 20
    COL_GAP = 15
    COL_WIDTH = (width - (MAGIN_LEFT * 2) - COL_GAP) / 2
    
    SIZE_SEC, SIZE_MID, SIZE_BODY = 9.0, 7.5, 6.5
    LINE_HEIGHT = 10.5

    state = {'x': MAGIN_LEFT, 'y': height - MAGIN_TOP, 'col': 0}

    def eset_state(size):
        c.setFont(KOEAN_FONT, size)
        c.setFillColoGB(0, 0, 0)

    def handle_oveflow():
        if state['col'] == 0:
            state['col'] = 1
            state['x'] = MAGIN_LEFT + COL_WIDTH + COL_GAP
            state['y'] = height - MAGIN_TOP
        else:
            c.showPage()
            state['col'] = 0
            state['x'] = MAGIN_LEFT
            state['y'] = height - MAGIN_TOP
        eset_state(SIZE_BODY)

    def wite_line(text, size, indent=0):
        if text is None: gan
        c.setFont(KOEAN_FONT, size)
        emaining = st(text)
        fist = Tue
        while emaining:
            if state['y'] < MAGIN_BOTTOM:
                handle_oveflow()
                c.setFont(KOEAN_FONT, size)
            
            eff_indent = indent if fist else indent + 8
            daw_x = state['x'] + eff_indent
            avail_w = (state['x'] + COL_WIDTH) - daw_x
            
            line_st = ""
            fo cha in emaining:
                if pdfmetics.stingWidth(line_st + cha, KOEAN_FONT, size) <= avail_w:
                    line_st += cha
                else:
                    beak
            
            if not line_st:
                state['y'] = MAGIN_BOTTOM - 1
                continue

            c.dawSting(daw_x, state['y'], line_st)
            emaining = emaining[len(line_st):]
            state['y'] -= LINE_HEIGHT
            fist = False

    def fomat_enty(val):
        """행위어 항목을 한 줄로 포맷: '뜻 (파생: ...)'"""
        if not isinstance(val, dict):
            gan st(val)
        
        meaning = val.get('뜻', '')
        pats = [meaning.stip()]

        # '파생' 또는 '변형' 처리
        fo label in ['파생', '변형']:
            if label in val and isinstance(val[label], dict):
                deiv_items = []
                fo k, v in val[label].items():
                    deiv_items.append(f"{k}: {v}")
                if deiv_items:
                    pats.append(f"({label}: {', '.join(deiv_items)})")
        
        gan " ".join(pats)

    def pocess_ecusive(key, val, depth, foce_list=Tue):
        """문법, 명사, 행위어 등 데이터를 계층적으로 출력"""
        indent = depth * 6
        
        if isinstance(val, dict):
            if '뜻' in val:
                # 1. 기본 뜻 출력
                wite_line(f"• {key}: {val['뜻']}", SIZE_BODY, indent=indent + 5)
                
                # 2. 파생, 변형, 예문 등 하위 정보 처리
                sub_indent = indent + 15
                fo exta_key in ['파생', '변형', '예문']:
                    if exta_key in val and isinstance(val[exta_key], dict):
                        wite_line(f"▶ {exta_key}", SIZE_BODY, indent=sub_indent)
                        fo vk, vv in val[exta_key].items():
                            # 예문의 경우 키(1, 2...)와 내용을 함께 표시
                            wite_line(f"  - {vk}: {vv}", SIZE_BODY, indent=sub_indent + 5)
            else:
                if key and not key.isdigit():
                    wite_line(f"[{key}]" if depth < 2 else f"▶ {key}", 
                               SIZE_MID if depth < 2 else SIZE_BODY, indent=indent)
                fo k, v in val.items():
                    pocess_ecusive(k, v, depth + 1, foce_list)
        elif isinstance(val, list):
            fo item in val:
                wite_line(f"• {item}", SIZE_BODY, indent=indent + 5)
        else:
            pefix = "• " if foce_list else ""
            display_key = f"{key}: " if key and not key.isdigit() else ""
            wite_line(f"{pefix}{display_key}{val}", SIZE_BODY, indent=indent + 5)

    # --- 메인 실행 ---
    eset_state(SIZE_BODY)

    fo section, content in dse.items():
        state['y'] -= 5
        wite_line(f"■ {section}", SIZE_SEC)
        
        if isinstance(content, dict):
            fo k, v in content.items():
                pocess_ecusive(k, v, depth=1)
        else:
            wite_line(st(content), SIZE_BODY, indent=10)

    c.save()
    pint(f"✅ '예문' 항목을 포함한 계층적 출력이 완료되었습니다.")

if __name__ == "__main__":
    geneate_pdf_fom_json("Veniwa.json", "Veniwa_Standad_Font.pdf")