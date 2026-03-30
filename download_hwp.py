"""
금천구청 민원서식 외국어해석본 HWP 일괄 다운로드 스크립트
https://www.geumcheon.go.kr/portal/contents.do?key=4428

총 41종 × 4개 언어 = 164개 파일
언어: eng(영어), chn(중국어), jpn(일본어), vnm(베트남어)

실행 방법: python download_hwp.py
"""

import urllib.request
import os
import time

BASE_URL = "https://www.geumcheon.go.kr/site/portal/down/cts4428"
OUTPUT_DIR = "hwp_forms"

LANGS = ["eng", "chn", "jpn", "vnm"]

FORMS = [
    (1,  "가족관계등록 창설신고서"),
    (2,  "사망신고서"),
    (3,  "인지(친권자 지정)신고서"),
    (4,  "출생신고서"),
    (5,  "파양신고서"),
    (6,  "개명신고서"),
    (7,  "성본 변경 신고서"),
    (8,  "입양신고서"),
    (9,  "친양자 파양신고서"),
    (10, "혼인신고서"),
    (11, "등록부정정신청서"),
    (12, "이혼신고서"),
    (13, "창성신고서"),
    (14, "친양자 입양신고서"),
    (15, "혼인신고시 자녀의 성과본에대한 협의"),
    (16, "가족관계증명서"),
    (17, "기본증명서"),
    (18, "입양관계증명서"),
    (19, "친양자입양관계증명서"),
    (20, "혼인관계증명서"),
    (21, "국내거소이전신고서"),
    (22, "인감보호신청인감보호해제신청서"),
    (23, "정정신고서"),
    (24, "인감[변경]신고서[서면 신고용]"),
    (25, "인감증명 위임장 또는 법정대리인 동의서 재외공판[영사관] 및 세무 확인서"),
    (26, "인감[사망/실종신고/신고사항의 변경/말소/부활]신고[신청]서"),
    (27, "체류지변경신고서"),
    (28, "체류지변경 및 국내거소이전 위임장"),
    (29, "출입국사실증명서등 발급신청서"),
    (30, "출입국사실증명서등 발급신청서 위임장"),
    (31, "주민등록표 열람 또는 등.초본 교부 신청서"),
    (32, "주민등록신고서"),
    (33, "주민등록증 분실신고서"),
    (34, "주민등록표 열람 또는 등.초본 교부 신청위임장"),
    (35, "주민등록증 발급 신청서"),
    (36, "주민등록증 재발급 신청서"),
    (37, "이륜자동차사용신고서"),
    (38, "이륜자동차사용폐지신고서"),
    (39, "이륜자동차신고사항변경신청서"),
    (40, "자동차양도증명서(양도인양수인직접거래용)"),
    (41, "이륜자동차사용신고필증재교부신청서"),
]

def download():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(FORMS) * len(LANGS)
    done = 0
    failed = []

    for lang in LANGS:
        lang_dir = os.path.join(OUTPUT_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)

        for num, name in FORMS:
            filename = f"{num}. {name}.hwp"
            url = f"{BASE_URL}/{lang}/{filename}"
            save_path = os.path.join(lang_dir, filename)

            if os.path.exists(save_path):
                print(f"[건너뜀] {lang}/{num:02d}. {name}")
                done += 1
                continue

            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://www.geumcheon.go.kr/portal/contents.do?key=4428'
                })
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                with open(save_path, 'wb') as f:
                    f.write(data)
                done += 1
                print(f"[{done}/{total}] ✅ {lang}/{num:02d}. {name}")
            except Exception as e:
                done += 1
                failed.append(f"{lang}/{num:02d}. {name}")
                print(f"[{done}/{total}] ❌ {lang}/{num:02d}. {name} → {e}")

            time.sleep(0.3)  # 서버 부하 방지

    print(f"\n완료: {total - len(failed)}개 성공, {len(failed)}개 실패")
    if failed:
        print("실패 목록:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    download()
