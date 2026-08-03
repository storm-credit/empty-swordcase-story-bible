#!/usr/bin/env python3
"""Restore v3.1 world-operability data from checked-in canon sources.

The generated files are operational overlays. They do not replace the protected
canon choices; they make the existing regions, settlements, factions, routes,
secrets, and glossary auditable from the repository.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


REGIONS = [
    {
        "id": "R00",
        "name": "청래역권",
        "episodes": "1-20, 191-200 return echoes",
        "core_question": "길과 물건은 누구의 책임으로 남는가.",
        "staple_food": "보리수제비",
        "shortage_trigger": "역마가 끊기면 말먹이와 마른 약재가 먼저 모자란다.",
        "transport": "역마 수레와 갈대나루 배편",
        "bottleneck": "폭우 뒤 우물마당 배수로가 막히면 모든 남행 화물이 한 칸 창고에 몰린다.",
        "taboo": "수신인 이름을 한 번만 부르고 물건을 선반에 올리는 일.",
        "ownership_custom": "분실물은 팔지 않고 서른 날 동안 공개 보관한다.",
        "civic_schedule": "해질 무렵 공개 보관 절차와 새벽 남행 분류.",
        "disaster_weakness": "야간 분류 인력이 줄면 출처 불명 유물이 폐기 창고로 밀린다.",
        "sensory_marks": ["젖은 쇠고리 소리", "마른 약재 냄새", "수레축에 묻은 진흙"],
        "local_terms": ["수신인 세 번", "마지막 배송"],
        "irrational_rule": "주인이 죽어도 수신인 확인 전에는 연료로 쓰지 않는다.",
        "finale_contribution": "첫 귀로인의 배달패와 분산 배송망의 보증.",
    },
    {
        "id": "R01",
        "name": "중원 경도",
        "episodes": "21-40, 141-153, 195",
        "core_question": "진품과 가격이 실제 쓰임보다 우선할 수 있는가.",
        "staple_food": "기름장 국수",
        "shortage_trigger": "시장 폭동 뒤 값싼 기름과 종이 표찰이 먼저 동난다.",
        "transport": "관물청 수레와 시장 인력 행렬",
        "bottleneck": "감정대 문이 닫히면 모든 거래와 숙박 보증이 동시에 멈춘다.",
        "taboo": "감정서 원문을 보지 않고 가격부터 부르는 일.",
        "ownership_custom": "증서, 사용 이력, 공개 증언을 세 줄로 나누어 기록한다.",
        "civic_schedule": "정오 경매종과 저녁 공개 감정회.",
        "disaster_weakness": "가격표가 먼저 움직이면 군중이 출구보다 감정대로 몰린다.",
        "sensory_marks": ["달군 인장 냄새", "가격표 종이 긁힘", "전시대 기름빛"],
        "local_terms": ["공개끈", "반론값"],
        "irrational_rule": "가짜라도 사람을 지킨 물건은 광장 바닥에 바로 놓지 않는다.",
        "finale_contribution": "공개 전시관과 원격 공명 설비.",
    },
    {
        "id": "R02",
        "name": "남독택",
        "episodes": "41-60, 146, 152, 196",
        "core_question": "생명과 물건의 경계는 누가 판정하는가.",
        "staple_food": "연잎 약죽",
        "shortage_trigger": "독안개가 짙어지면 해독재와 깨끗한 천이 먼저 끊긴다.",
        "transport": "나무다리, 얕은 배, 신수 발자국길",
        "bottleneck": "야생계약소 보호실 접근권이 막히면 치료와 심사가 함께 늦어진다.",
        "taboo": "신수에게 먼저 이름을 붙이고 소유자를 묻는 일.",
        "ownership_custom": "계약은 인간의 권리보다 신수의 철회권을 먼저 적는다.",
        "civic_schedule": "안개가 얇아지는 새벽 치료열과 저녁 촌회.",
        "disaster_weakness": "향로가 마을을 살리는 동안 숲 전체가 잠든다.",
        "sensory_marks": ["단내 섞인 독안개", "약솥 김", "젖은 허물의 냉기"],
        "local_terms": ["숨허락", "허물값"],
        "irrational_rule": "아픈 신수에게 먹이를 먼저 주지 않고 냄새를 확인한다.",
        "finale_contribution": "역계약 제도와 신수 자율 심사.",
    },
    {
        "id": "R03",
        "name": "북설원",
        "episodes": "61-80, 145, 151, 197",
        "core_question": "보호 장비는 한 사람의 전리품인가 공동 방어망인가.",
        "staple_food": "얼음보리죽",
        "shortage_trigger": "봉화 교대가 끊기면 장작과 말기름이 먼저 사라진다.",
        "transport": "설각마, 썰매, 봉화대 사이 눈길",
        "bottleneck": "눈벽 하나가 닫히면 일곱 촌락의 식량 순환이 끊긴다.",
        "taboo": "구조받은 사람 이름을 봉인 기록에서 지우는 일.",
        "ownership_custom": "방어구 조각은 촌락별 제한 사용권으로 보관한다.",
        "civic_schedule": "해 뜨지 않는 백야 교대와 봉화 점검일.",
        "disaster_weakness": "공동 방어망은 매일 인력을 요구해 가난한 집부터 무너진다.",
        "sensory_marks": ["눈벽 마찰음", "마른 장작 냄새", "얼음 밑 종소리"],
        "local_terms": ["교대몫", "눈벽값"],
        "irrational_rule": "혼자 살아남은 피난민을 바로 축하하지 않는다.",
        "finale_contribution": "열린 봉인소와 공동 방어 교대 체계.",
    },
    {
        "id": "R04",
        "name": "서황막",
        "episodes": "81-100, 147, 154, 184, 198",
        "core_question": "편리한 길은 무엇을 지우고 누구에게 비용을 청구하는가.",
        "staple_food": "마른 대추밥",
        "shortage_trigger": "대상로가 접히면 물표와 그늘천이 먼저 오르며 피난민이 밀린다.",
        "transport": "대상 낙타수레와 세관 물표",
        "bottleneck": "유리폐도의 세관 장대가 기억 통행료를 받기 시작한다.",
        "taboo": "남의 물표에 손가락으로 물방울을 찍는 일.",
        "ownership_custom": "우물과 그늘은 지분보다 하루 생존권으로 먼저 배정한다.",
        "civic_schedule": "정오 물표 검사와 밤 대상 출발.",
        "disaster_weakness": "지도 유물이 길을 줄이면 뒤쪽 길과 귀향 기억이 사라진다.",
        "sensory_marks": ["입안의 모래", "천막 줄 마찰음", "빈 물독의 쇳소리"],
        "local_terms": ["그늘몫", "기억세"],
        "irrational_rule": "지도에 없는 발자국은 세 번 밟지 않는다.",
        "finale_contribution": "책임거래소와 기억세 개혁.",
    },
    {
        "id": "R05",
        "name": "동해군도",
        "episodes": "101-120, 148, 194",
        "core_question": "바다에 잠긴 도시의 주인은 증서인가 기억인가.",
        "staple_food": "소금미역밥",
        "shortage_trigger": "조수종이 늦으면 마른 밧줄과 숨부적이 먼저 사라진다.",
        "transport": "부유역참, 조수 배, 닻줄 길",
        "bottleneck": "한 섬이 허락을 거부하면 여섯 가문의 창고가 열리지 않는다.",
        "taboo": "실종자 닻줄을 발로 넘는 일.",
        "ownership_custom": "바다 유산은 구조, 기억, 지분, 장례권을 나누어 기록한다.",
        "civic_schedule": "조수종, 장례 전 실종자 신호 확인, 공동 인양일.",
        "disaster_weakness": "축소지도가 도시를 접으면 숨빚 상환일이 앞당겨진다.",
        "sensory_marks": ["젖은 밧줄 냄새", "조수종 울림", "소금 묻은 나무바닥"],
        "local_terms": ["닻허락", "숨빚"],
        "irrational_rule": "새 배에 오르기 전 빈 매듭 하나를 남긴다.",
        "finale_contribution": "마지막 배송 항로와 중앙핵 조각 수신위원.",
    },
    {
        "id": "R06",
        "name": "무명시",
        "episodes": "121-160, 184",
        "core_question": "이름과 죄명도 소유되고 거래될 수 있는가.",
        "staple_food": "무명떡",
        "shortage_trigger": "장부 압수가 시작되면 잉크와 임시 호칭패가 먼저 사라진다.",
        "transport": "호칭문, 장부 계단, 지하 역로",
        "bottleneck": "임시 이름이 없으면 숙소, 치료, 통행이 동시에 거부된다.",
        "taboo": "상대가 먼저 말하지 않은 본명을 세 번 부르는 일.",
        "ownership_custom": "이름은 사용권, 기억은 보증, 행적은 공개 기록으로 나눈다.",
        "civic_schedule": "아침 호칭 경매와 밤 장부 수정 시간.",
        "disaster_weakness": "가난한 사람은 성씨를 팔아 하루를 살고 조상 제사권을 잃는다.",
        "sensory_marks": ["마른 먹가루", "이름표 태우는 냄새", "남의 목소리 호객"],
        "local_terms": ["빈호칭", "행적값"],
        "irrational_rule": "이름 없는 아이에게 물건을 바로 건네지 않고 습관을 확인한다.",
        "finale_contribution": "여섯 공개 기록과 행적명 체계.",
    },
    {
        "id": "R07",
        "name": "천외산맥",
        "episodes": "161-200",
        "core_question": "수장은 무엇을 소유해야 하며 무엇을 내려놓아야 하는가.",
        "staple_food": "건량 조각",
        "shortage_trigger": "중력 계단이 뒤집히면 물보다 장비 고정끈이 먼저 모자란다.",
        "transport": "천외문, 부유계단, 분류 전시실",
        "bottleneck": "문이 사람을 직업으로만 인식하면 동료가 장비 칸으로 분류된다.",
        "taboo": "살아 있는 사람을 전시 명패로 부르는 일.",
        "ownership_custom": "중앙 권한은 인격 침식 대가 없이는 사용할 수 없다.",
        "civic_schedule": "박물관 분류 갱신과 중앙핵 맥박 주기.",
        "disaster_weakness": "모든 길이 중앙핵으로 모여 재독점 위험을 만든다.",
        "sensory_marks": ["소독약과 돌먼지", "금속핵 맥박", "끊어지는 금빛 선"],
        "local_terms": ["분류거부", "귀로조각"],
        "irrational_rule": "문이 통과를 허락해도 동료 이름을 먼저 확인한다.",
        "finale_contribution": "중앙핵을 여섯 책임 조각으로 나누는 최종 무대.",
    },
]


SETTLEMENTS = [
    ("ST001", "R00", "청래역", [1, 3, 9, 10, 19], "분실물 선반에서 매일 위치가 바뀌는 낡은 신발"),
    ("ST002", "R00", "쇠울촌", [2, 3, 4, 5, 6, 7, 8], "죽은 수신인에게 20년째 도착하는 빈 편지"),
    ("ST003", "R00", "갈대나루", [11, 13, 20], "역마가 특정 봉인수레만 거부"),
    ("ST004", "R00", "돌배고개", [12, 14, 15], "우물 쇠고리에 남은 여러 세대의 구조 의흔"),
    ("ST005", "R00", "우엉들", [16, 17], "가짜 배달패를 찬 아이"),
    ("ST006", "R00", "비탈창고", [18, 19, 20], "폭우에 떠내려온 경도 왕실 표찰"),
    ("ST007", "R01", "경도 내성", [23, 24], "한 물건에 합법 증서가 세 장"),
    ("ST008", "R01", "만보시장", [21, 22, 25, 29], "가짜 왕검이 진품보다 더 많은 시민을 지킨 기록"),
    ("ST009", "R01", "열두손골", [27, 28, 31, 32, 33, 37], "거짓말을 먹지만 진실은 말하지 않는 귀걸이"),
    ("ST010", "R01", "공도원", [34, 35, 36, 141, 142, 143], "가격 없는 저울이 가난한 배달부 쪽에서 움직이지 않음"),
    ("ST011", "R01", "진수문", [24, 26, 35, 39, 40], "감정사가 자기 가문의 오류를 공개해야 하는 재판"),
    ("ST012", "R01", "시민전시거리", [22, 24, 29, 30, 37, 38, 144, 153], "왕실이 위조품을 정통성 선전에 이용"),
    ("ST013", "R02", "연무약곡", [52, 53, 54], "향로가 마을을 살리지만 숲 전체를 잠재움"),
    ("ST014", "R02", "부엽촌", [45, 46, 47, 48], "독을 없애면 서식지가 붕괴하는 치료 선택"),
    ("ST015", "R02", "향등나루", [41, 42, 43, 44], "신수가 계약을 세 번 거부"),
    ("ST016", "R02", "백옥습", [49, 50, 51], "인간 주민을 미끼로 신수를 유인하는 밀매단"),
    ("ST017", "R02", "독왕초림", [55, 56, 57], "허물 안에 천공무고 사육 표식"),
    ("ST018", "R02", "역계약림", [58, 59, 60, 146, 152], "독왕초 씨앗을 봉인할지 남길지 촌회 분열"),
    ("ST019", "R03", "칠화로진", [61, 62, 63, 64], "주인을 얼려 살린 피풍이 다시 주인을 가둠"),
    ("ST020", "R03", "봉인성", [65, 66, 67, 68, 145], "깨진 설갑 일곱 조각을 서로 다른 촌락이 보유"),
    ("ST021", "R03", "설각촌", [69, 70, 71], "봉인성은 안전하지만 마을의 기억을 삭제"),
    ("ST022", "R03", "빙잠골", [72, 73, 74], "방패가 지킨 사람과 버린 사람 이름을 동시에 품음"),
    ("ST023", "R03", "백야초소", [75, 76, 77, 151], "설각마가 목적지를 속인 기수를 버림"),
    ("ST024", "R03", "해빙나루", [78, 79, 80], "공동 징발된 유물이 돌아오지 않음"),
    ("ST025", "R04", "황문대시장", [81, 82, 83, 84, 147, 154], "사막을 접는 지도가 뒤의 길을 지움"),
    ("ST026", "R04", "첫물성", [85, 86, 87, 88], "기억을 물로 바꾸는 호리병이 사생활을 노출"),
    ("ST027", "R04", "유리폐도", [89, 90, 91], "대상이 물 대신 기억을 통행료로 요구"),
    ("ST028", "R04", "긴그늘역", [92, 93, 94], "첫 천품 파편이 전시실 상극을 일으킴"),
    ("ST029", "R04", "접힌문", [95, 96, 97], "유리폐도의 길이 매일 재분류"),
    ("ST030", "R04", "기억잔촌", [98, 99, 100], "우물 지분이 없는 피난민 행렬"),
    ("ST031", "R05", "육닻항", [101, 102, 103, 104, 148], "파도를 기억하는 닻의 주인이 여섯 공동체"),
    ("ST032", "R05", "해람섬", [105, 106, 107, 108], "숨 목걸이가 나중에 호흡 부채를 청구"),
    ("ST033", "R05", "빈매듭촌", [109, 110, 111], "라이벌이 합법적으로 핵심 유산 낙찰"),
    ("ST034", "R05", "조류탑섬", [112, 113, 114], "청묘가 여섯 섬 중 한 곳의 허락을 거부"),
    ("ST035", "R05", "침몰도시 입구", [115, 116, 117], "침몰도시 축소지도가 실제 도시를 접으려 함"),
    ("ST036", "R05", "파랑나루", [118, 119, 120], "빈매듭 장례 직전 실종자의 신호"),
    ("ST037", "R06", "첫호칭거리", [121, 122, 123, 124], "담운이 동료 기억에서 지워짐"),
    ("ST038", "R06", "빈호적골", [125, 126, 127, 128], "무명견이 이름 대신 습관으로 담운을 찾음"),
    ("ST039", "R06", "등표시장", [129, 130, 131], "빌린 칭호의 원한이 따라옴"),
    ("ST040", "R06", "기억매듭원", [132, 133, 134], "빈 호적죽간에 담운 이름만 쓰이지 않음"),
    ("ST041", "R06", "행적법정", [135, 136, 137], "이름장수의 주판이 사람의 빚을 계산"),
    ("ST042", "R06", "천외밑문", [138, 139, 140, 141, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160], "린화가 물건 다루는 습관으로 담운을 알아봄"),
    ("ST043", "R07", "하늘아래역", [155, 161, 162, 163, 164, 165, 166, 167], "문이 사람을 직업으로만 인식"),
    ("ST044", "R07", "부유계단군", [168, 169, 170, 171, 172, 173, 174], "살아 있는 전시실이 동료를 수집품 분류"),
    ("ST045", "R07", "십이문실", [175, 176, 177, 178, 179, 180, 181], "백장의 장갑이 중앙핵 열쇠"),
    ("ST046", "R07", "살아있는전시실", [182, 183, 184, 185, 186, 187, 188], "담운과 같은 얼굴의 수장 초상"),
    ("ST047", "R07", "중앙핵실", [189, 190, 191, 192, 193, 194], "수장인 반쪽이 담운을 완성품으로 요구"),
    ("ST048", "R07", "열린무고", [195, 196, 197, 198, 199, 200], "놓아준 유산들이 자발적으로 원격 공명"),
]


FACTIONS = [
    ("FC001", "청래역참망", "역마와 장부 신뢰", "위험 보관 시설", "운송료", "역마 사료와 야간 인력", "배송 질서 유지", "출처 불명 유물 사고를 역참 밖으로 내보내기", "폐기파", "귀환파", "오복산", "젊은 역부", "담운 실종 시 임시 귀로대를 만든다", "분산 배송 책임 비용을 누가 낼지 다툰다"),
    ("FC002", "만보상련", "감정 보험과 거래망", "현장 증언", "보증금과 수수료", "감정사 신용 한도", "안전한 유물 거래", "약탈품도 보험 안에 넣어 통제하기", "실적파", "공개파", "문하준", "피해 상인", "담운 실종 시 회수권을 경매한다", "공개 책임보험의 보험료 갈등"),
    ("FC003", "귀장회 봉장파", "봉인 명령권", "지역 식량과 치료권", "국가 위탁 보조금", "봉인소 유지비", "재앙 유산 봉인", "위험을 중앙 기록으로 독점", "희생파", "현장파", "백장", "윤봉", "담운 실종 시 무주함을 회수한다", "중앙 봉인 붕괴 뒤 책임 추궁"),
    ("FC004", "귀장회 귀환파", "삭제 기록과 피해자 명단", "공개 증언", "내부 보급", "비밀 운송비", "봉인 피해 복구", "봉장파 내부에서 생존", "폭로파", "잔류파", "손백하", "무석", "담운 실종 시 피해자 명단을 먼저 공개한다", "공개 기록의 복수 악용"),
    ("FC005", "경도 왕실 기록관", "왕실 원문 기록", "시장 여론", "열람료와 관물세", "기록 보존 약품", "정통성 유지", "위조 실패 은폐", "은폐파", "공개파", "윤세정", "하급 필사관", "담운 실종 시 왕검 기록을 봉한다", "왕실 오류 보상금"),
    ("FC006", "경도 귀족 수집회", "사병과 전시권", "실사용 증언", "대여료와 후원금", "사병 유지비", "유산 품격 보존", "권위 약화를 막기 위한 위조품 몰수", "몰수파", "보존파", "귀족 대리인", "가난한 방계", "담운 실종 시 진품 목록을 사들인다", "공개 전시관 참여 범위"),
    ("FC007", "시민공개감정회", "군중 증언", "전문 감정 기술", "기부와 전시 수익", "공개장 보안", "실사용 기록 공개", "왕실·상련 사이에서 생존", "급진파", "절차파", "한여정", "소상인", "담운 실종 시 모조 왕검을 지킨다", "거짓 증언 처리"),
    ("FC008", "남독 야생계약단", "신수 심사권", "약재와 보호 시설", "치료·심사 수수료", "보호실 유지비", "신수 철회권 보장", "인간 불신을 조직 생존 명분으로 유지", "불허파", "공존파", "미라", "연호", "담운 실종 시 두리 선택을 먼저 확인한다", "역계약 남용 분쟁"),
    ("FC009", "남독 밀매단", "불법 우리와 검은 운송로", "합법 치료 기록", "희귀 신수 판매", "뇌물과 위장 우리", "멸종종 상품화", "생태 붕괴를 숨기고 수요 유지", "포획파", "거래파", "사태오", "잡역꾼", "담운 실종 시 신수 표식을 팔아넘긴다", "잔당의 생계 범죄"),
    ("FC010", "북설 칠촌회의", "설갑 조각과 봉화대", "외부 식량", "공동 방어 분담금", "장작과 교대 인력", "일곱 마을 생존", "봉인성 기억 삭제를 감수하고 안전 확보", "독점파", "분산파", "노상린", "젊은 피난민", "담운 실종 시 조각 이동을 멈춘다", "교대 부담 불평등"),
    ("FC011", "북설 귀장회 현장대", "현장 봉인 기술", "마을 협조", "귀장회 보급", "치료권과 방패 수리", "북설 재앙 차단", "삭제 기록을 유지해 책임 회피", "명령파", "보호파", "윤봉", "탈퇴 파수꾼", "담운 실종 시 무석을 추적한다", "탈퇴자의 연금권"),
    ("FC012", "서황막 대상연합", "대상로와 물표", "우물 지분", "운송 이익", "물과 그늘천", "길 유지와 거래", "기억세를 새 수입으로 만들기", "통행세파", "책임거래파", "마지한", "짐꾼", "담운 실종 시 지도 유물을 임대한다", "피난민 통행료"),
    ("FC013", "서황 관물세관", "검문 장대와 보물세", "정확한 유산 위험 평가", "관물세", "세관 인장과 감시 인력", "위험 유산 통제", "세금을 책임 정보로 포장", "징수파", "개혁파", "우담", "하급 세리", "담운 실종 시 기억세를 강화한다", "책임정보 납부제의 사생활 침해"),
    ("FC014", "천공무고 폐분관 기록체", "분류실 알고리즘", "살아 있는 판단자", "자동 보관 권한", "상극 격리실", "오류 없는 보관", "실패 기록을 삭제해 체계 신뢰 유지", "자동분류파", "기록보존파", "서문록", "삭제 인격", "담운 실종 시 무주함 데이터를 흡수한다", "기록 인격의 권리"),
    ("FC015", "동해 여섯가문 회의", "인양권과 닻줄", "외부 조정자", "항로 지분", "구조선과 숨부적", "침몰도시 공동 관리", "지분 매각으로 빚을 갚기", "매각파", "공동파", "해라", "권해주", "담운 실종 시 창고 문을 닫는다", "장례권과 지분권 충돌"),
    ("FC016", "무명시 이름상회", "이름 사용권 시장", "행적 증명", "이름 대여료", "호칭패와 기억 담보", "이름 거래 안정", "가난한 이름을 계속 유통시키기", "매매파", "행적파", "윤무명", "이름 없는 아이", "담운 실종 시 그의 이름 권리를 판다", "성씨 판매 피해 복구"),
    ("FC017", "무명시 중앙장부국", "중앙 이름장부", "분산 증언", "수정 수수료", "장부 보존 인력", "이름 질서 유지", "사람을 항목으로 분류해 통제", "잠금파", "이력파", "류백", "단소아", "담운 실종 시 최종 수집 칸을 연다", "공개 기록의 오기 책임"),
    ("FC018", "원형 천공무고", "중앙핵과 수장인", "여섯 권역 응답", "중앙 보관 권한", "살아 있는 전시실", "천하 유산의 완전 보관", "사람까지 분류해 재앙을 막기", "완성파", "해체파", "묵언", "분류된 동료", "담운 실종 시 그를 완성품으로 수납한다", "중앙 없는 안전의 지속 비용"),
]


ROUTES = [
    ("RT001", "청래역", "쇠울촌", "1-10", "폭우 배수로", "파손 책임"),
    ("RT002", "청래역", "갈대나루", "11-13", "역마 거부", "봉인표 통행권"),
    ("RT003", "갈대나루", "돌배고개", "12-15", "냉철못 다리", "상극 장비 제한"),
    ("RT004", "돌배고개", "경도 입구", "16-20", "회수대 검문", "고향 이탈"),
    ("RT005", "경도 만보시장", "시민전시거리", "21-30", "경매 군중", "신용 손실"),
    ("RT006", "열두손골", "공도원", "31-40", "공개 감정대", "감정 노동 담보"),
    ("RT007", "경도 남문", "향등나루", "39-44", "남독 통행 검사", "약재 지연"),
    ("RT008", "부엽촌", "백옥습", "45-51", "독안개 수로", "신수 접근권 상실"),
    ("RT009", "연무약곡", "역계약림", "52-60", "잠든 숲길", "치료비와 비수집 대가"),
    ("RT010", "남독택", "칠화로진", "60-64", "북상 눈길", "두리 비행 제한"),
    ("RT011", "칠화로진", "봉인성", "65-70", "봉화 교대", "식량 분담"),
    ("RT012", "봉인성", "해빙나루", "71-80", "백야 회수선", "역참 이용권 상실"),
    ("RT013", "해빙나루", "황문대시장", "80-84", "눈 위 사막문", "귀향길 상실"),
    ("RT014", "첫물성", "유리폐도", "85-91", "물표 세관", "기억 통행료"),
    ("RT015", "긴그늘역", "동해문", "92-100", "상극 전시실", "핵심 장비 귀환"),
    ("RT016", "육닻항", "침몰도시", "101-120", "조수종과 닻줄", "숨빚"),
    ("RT017", "무명시 지하역로", "이름시장", "120-130", "임시 호칭문", "이름 사용권"),
    ("RT018", "중앙 장부실", "천외밑문", "131-160", "장부 계단", "기억·호칭 손실"),
    ("RT019", "천외문", "원형 천공무고", "161-180", "중력 계단", "인격 침식"),
    ("RT020", "중앙핵실", "열린무고", "181-200", "소유선 붕괴", "중앙 권한 상실"),
]


ITEM_TERMS = [
    ("IT01", "무주함", "system", 1, "무주·귀환·공동 책임 판정 장치"),
    ("IT02", "반치", "item", 2, "최종부 강제 소유 연결선을 자르는 실패작 단검"),
    ("IT03", "빈 명패", "item", 7, "본명보다 행적을 기록하는 정체 장치"),
    ("IT04", "모조 왕검", "item", 20, "진품보다 쓰임이 오래 남은 왕검"),
    ("IT05", "무명의 대장장이 세트", "set", 4, "완성과 후회 과부하를 보여주는 초기 세트"),
    ("IT06", "잠든 숲 향로", "item", 43, "수집하지 않고 공동체에 남기는 비수집 장치"),
    ("IT07", "설갑", "set", 63, "일곱 마을 공동 방어망으로 완성되는 갑옷"),
    ("IT08", "사막 지도", "item", 82, "길을 줄이는 대신 지나온 길을 지우는 지도"),
    ("IT09", "소리 없는 망치", "item", 94, "영구 귀환으로 두리를 살리는 핵심 도구"),
    ("IT10", "중앙핵", "system", 168, "중앙 소유 체계의 결말 장치"),
]


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_regions() -> list[dict]:
    return REGIONS


def build_settlements() -> list[dict]:
    regions = {r["id"]: r for r in REGIONS}
    rows = []
    for sid, rid, name, episodes, landmark in SETTLEMENTS:
        region = regions[rid]
        rows.append(
            {
                "id": sid,
                "name": name,
                "region_id": rid,
                "region": region["name"],
                "episodes": episodes,
                "landmark": landmark,
                "current_tension": region["core_question"],
                "entry_rule": region["taboo"],
                "daily_operation": region["civic_schedule"],
                "logistics_bottleneck": region["bottleneck"],
                "disaster_weakness": region["disaster_weakness"],
                "sensory_marks": region["sensory_marks"],
                "local_terms": region["local_terms"],
                "event_seed": f"{region['civic_schedule']} -> {landmark} -> {region['disaster_weakness']}",
            }
        )
    return rows


def build_factions() -> list[dict]:
    rows = []
    for raw in FACTIONS:
        (
            fid,
            name,
            monopoly,
            dependency,
            income,
            fixed_cost,
            public_goal,
            hidden_goal,
            hardline,
            moderate,
            beneficiary,
            loser,
            without_damun,
            post_act5_conflict,
        ) = raw
        rows.append(
            {
                "id": fid,
                "name": name,
                "monopoly_resource": monopoly,
                "external_dependency": dependency,
                "income_source": income,
                "largest_fixed_cost": fixed_cost,
                "public_goal": public_goal,
                "hidden_survival_goal": hidden_goal,
                "hardline_faction": hardline,
                "moderate_faction": moderate,
                "beneficiary_cast": beneficiary,
                "losing_cast": loser,
                "if_damun_disappears": without_damun,
                "post_act5_conflict": post_act5_conflict,
            }
        )
    return rows


def build_routes() -> list[dict]:
    return [
        {
            "id": rid,
            "from": start,
            "to": end,
            "episodes": episodes,
            "bottleneck": bottleneck,
            "cost": cost,
        }
        for rid, start, end, episodes, bottleneck, cost in ROUTES
    ]


def build_act_subacts() -> list[dict]:
    tracks = load_json(DATA / "payoff_tracks_v2_7.json")["a_tier"]
    episode_files = [
        "episodes_001_010.json",
        "episodes_011_020.json",
        "episodes_021_030.json",
        "episodes_031_040.json",
        "episodes_041_080.json",
        "episodes_081_120.json",
        "episodes_121_160.json",
        "episodes_161_200.json",
    ]
    episodes = []
    for name in episode_files:
        episodes.extend(load_json(DATA / name))
    by_ep = {row["episode"]: row for row in episodes}
    rows = []
    for aid in [f"A{i:02d}" for i in range(1, 21)]:
        track = tracks[aid]
        first, last = track["episodes"]
        first_row = by_ep[first]
        rows.append(
            {
                "id": aid,
                "act": first_row["act"],
                "act_title": first_row["act_title"],
                "episodes": list(range(first, last + 1)),
                "title": track["name"],
                "false_answer": track["false_answer"],
                "truth": track["truth"],
                "start_episode_title": first_row["title"],
                "end_episode_title": by_ep[last]["title"],
                "causal_input": "앞 서브액트의 선택 비용을 다음 생활 문제로 넘긴다.",
                "terminal_state_change": track["truth"],
            }
        )
    return rows


def build_secrets() -> list[dict]:
    tracks = load_json(DATA / "payoff_tracks_v2_7.json")
    secrets: list[dict] = []
    for sid, info in tracks["s_tier"].items():
        secrets.append(
            {
                "id": f"WS{len(secrets)+1:03d}",
                "source_id": sid,
                "type": "s_tier_truth",
                "setup_episode": info["install"],
                "reveal_episodes": info["payoff"],
                "secret": info["name"],
                "payoff_function": info["terminal"],
                "guardrail": "160화 이후 새 해결 법칙으로 확장하지 않는다.",
            }
        )
    for aid, info in tracks["a_tier"].items():
        secrets.append(
            {
                "id": f"WS{len(secrets)+1:03d}",
                "source_id": aid,
                "type": "subact_truth",
                "setup_episode": info["episodes"][0],
                "reveal_episodes": [info["episodes"][1]],
                "secret": info["false_answer"],
                "payoff_function": info["truth"],
                "guardrail": "정답 설명보다 행동 회수를 우선한다.",
            }
        )
    for region in REGIONS:
        secrets.append(
            {
                "id": f"WS{len(secrets)+1:03d}",
                "source_id": region["id"],
                "type": "regional_pressure",
                "setup_episode": int(region["episodes"].split("-")[0].split(",")[0]),
                "reveal_episodes": [],
                "secret": region["irrational_rule"],
                "payoff_function": region["finale_contribution"],
                "guardrail": "지역 규칙은 관광 설명이 아니라 장면 비용으로만 노출한다.",
            }
        )
    return secrets


def build_glossary(regions, settlements, factions) -> list[dict]:
    glossary: list[dict] = []

    def add(term_id: str, term: str, typ: str, first_episode: int, function: str) -> None:
        glossary.append(
            {
                "id": f"GL{len(glossary)+1:03d}",
                "source_id": term_id,
                "term": term,
                "type": typ,
                "first_episode": first_episode,
                "function": function,
            }
        )

    for region in regions:
        add(region["id"], region["name"], "region", int(region["episodes"].split("-")[0].split(",")[0]), region["core_question"])
    for settlement in settlements:
        add(settlement["id"], settlement["name"], "settlement", settlement["episodes"][0], settlement["landmark"])
    supporting = load_json(DATA / "supporting_cast_028.json")
    for cast in supporting:
        add(cast["id"], cast["name"], "supporting_cast", cast["first_episode"], cast["role"])
    for faction in factions:
        add(faction["id"], faction["name"], "faction", 1, faction["public_goal"])
    tracks = load_json(DATA / "payoff_tracks_v2_7.json")["s_tier"]
    for sid, info in tracks.items():
        add(sid, info["name"], "long_question", info["install"], info["terminal"])
    for item_id, term, typ, first_episode, function in ITEM_TERMS:
        add(item_id, term, typ, first_episode, function)
    if len(glossary) != 120:
        raise SystemExit(f"glossary must be 120 entries, got {len(glossary)}")
    return glossary


def main() -> None:
    regions = build_regions()
    settlements = build_settlements()
    factions = build_factions()
    routes = build_routes()
    act_subacts = build_act_subacts()
    secrets = build_secrets()
    glossary = build_glossary(regions, settlements, factions)

    write_json(DATA / "world_regions_008.json", regions)
    write_json(DATA / "world_settlements_048.json", settlements)
    write_json(DATA / "world_factions_018.json", factions)
    write_json(DATA / "world_routes_020.json", routes)
    write_json(DATA / "world_secrets_036.json", secrets)
    write_json(DATA / "world_glossary_120.json", glossary)
    write_json(DATA / "acts_subacts_005_020.json", act_subacts)
    print("built v3.1 world operability data: regions=8 settlements=48 factions=18 routes=20 secrets=36 glossary=120 subacts=20")


if __name__ == "__main__":
    main()
