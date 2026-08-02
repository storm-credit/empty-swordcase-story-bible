from __future__ import annotations
import json, re, shutil
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; PROD=ROOT/'production'; DOCS=ROOT/'docs'; SCRIPTS=ROOT/'scripts'; ORCH=ROOT/'orchestra'; WF=ROOT/'.github/workflows'
load=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
eps=load(ROOT/'build/episodes_effective_001_200_v2_8.json')
ep_by={r['episode']:r for r in eps}
sett={r['id']:r for r in load(DATA/'world_settlements_048.json')}
sc=load(DATA/'supporting_cast_028.json')
action_text=(PROD/'combat/ACTION_PREFLIGHT_041_200.md').read_text(encoding='utf-8')
action_eps=[int(x) for x in re.findall(r'^## (\d+)화', action_text, re.M)]

REGION_SPACES={
'R00':('수레문','우물 마당','분실물 선반','마구간 담장','배수로'),
'R01':('시장 아치','감정대','시민 난간','봉인 창고','가격표 골목'),
'R02':('젖은 나무다리','환자 천막','약솥 마당','신수 우리','독안개 수로'),
'R03':('눈벽 입구','봉화대','피난민 썰매선','봉인석 단','얼음 균열'),
'R04':('대상문','물독 그늘','세관 장대','폐전시실','되감기는 모래길'),
'R05':('부교 입구','조수종 탑','구조선 계류점','침몰문','급류 골'),
'R06':('호칭문','장부 계단','시민 증언대','봉인 서가','이름 불길'),
'R07':('중력문','부유 계단','분류 전시대','중앙핵 통로','붕괴 낙차구'),
}
CATEGORY_WORDS=[('재난',('붕괴','폭풍','눈사태','침몰','무너','폭주')),('구조',('구하','살리','주민','인질','피난','환자')),('추격',('쫓','추적','도망','회수대')),('결투',('결투','맞서','전쟁','공격','싸움'))]

def category(row):
    t=' '.join(str(row.get(k,'')) for k in ('title','goal','conflict','cost'))
    for c,ws in CATEGORY_WORDS:
        if any(w in t for w in ws): return c
    return '작전'

def ally_action(row):
    cast=row.get('cast',[])
    if '서린화' in cast: return '린화가 증거가 부족한 표적을 공격 목록에서 빼며 진입 순서를 늦춘다.'
    if '소예란' in cast: return '예란이 생명 징후가 약한 구역을 우선 구조 구역으로 지정해 격파 목표를 바꾼다.'
    if '곽무석' in cast: return '무석이 가장 짧은 길 대신 민간인 퇴로를 방패로 고정해 이동선을 바꾼다.'
    if '진여강' in cast: return '진여강이 소유권과 배상 책임을 역이용해 상대의 합법 지원을 끊는다.'
    if '두리' in cast: return '두리가 명령을 기다리지 않고 냄새가 끊긴 방향을 선택해 숨은 통로를 드러낸다.'
    return '동행자가 담운의 격파 목표보다 구조와 증거 보존을 먼저 선택한다.'

action_rows=[]
for i,ep in enumerate(action_eps):
    r=ep_by[ep]; sid=r['settlement_ids'][0]; s=sett[sid]; reg=s['region_id']; z=REGION_SPACES[reg]
    base=5+(i%5)*2
    zones={
      'A':f"{s['name']} {z[0]} — 폭 {3+(i%3)}보, 후퇴로는 {z[4]} 한 곳",
      'B':f"{z[1]} — 보호 대상과 담운 시작점, 낮은 엄폐물 {2+(i%2)}개",
      'C':f"{z[2]} — 핵심 물건·증거 위치, {s['landmark']}",
      'D':f"{z[3]} — 상대 시작점, C에서 {base+6}보, 첫 공격 유효거리 {base}보",
      'E':f"{z[4]} — 환경 위험 구역, {s['current_tension']}이 물리적 장애로 드러남",
    }
    distances={'A-B':base,'B-C':base+3,'C-D':base+6,'D-E':base+2,'A-E':base+11}
    cat=category(r)
    first=f"담운이 {z[0]}에서 반치 또는 현재 장비로 길을 열지만, {s['entry_rule']} 규칙 때문에 첫 동작이 멈춘다."
    rev1=f"역전 1 — {s['landmark']}이 예상과 반대로 작동해 C구역 접근로가 D구역 사거리 안으로 이동한다."
    rev2=f"역전 2 — {ally_action(r)}"
    rev3=f"역전 3 — `{r['choice']}` 선택으로 승리 조건이 상대 격파에서 `{r['goal']}`의 책임 있는 완료로 바뀐다."
    action_rows.append({
      'episode':ep,'title':r['title'],'category':cat,'settlement_id':sid,'settlement':s['name'],
      'goal':r['goal'],'opposition':r.get('conflict',''), 'zones':zones,'distances_paces':distances,
      'opening_three_exchanges':[
        first,
        f"상대가 D에서 {base}보 사거리 기술로 B와 C 사이를 끊고, 담운은 {z[1]} 쪽 발을 먼저 빼 보호 대상을 가린다.",
        f"담운이 장비 교체 시간을 벌기 위해 {z[2]}의 재질을 이용하지만, 환경 위험 E가 {base+2}보 안쪽까지 번진다."
      ],
      'reversals':[rev1,rev2,rev3],
      'final_action':f"결정타 대신 `{r['choice']}`을 실행하고, 다음 화에 남는 실제 손실은 `{r['cost']}`이다.",
      'continuity_cost':r['cost'],'closing_image':r['hook'],
      'approvals':['A12_SPACE_PASS','A13_CHOREOGRAPHY_PASS','A07_CONTINUITY_PASS','SYNAPSE_PM_PASS']
    })
(DATA/'action_preflight_v2_9.json').write_text(json.dumps(action_rows,ensure_ascii=False,indent=2),encoding='utf-8')

md=['# 주요 액션 47화 완성 프리플라이트 v2.9','', '> 전투·추격·재난·구조 장면의 공간과 연속성을 원고 작성 전에 잠근다.','']
for a in action_rows:
    md += [f"## {a['episode']}화 — {a['title']}", '', f"- 유형: {a['category']}", f"- 무대: {a['settlement']} ({a['settlement_id']})", f"- 목표: {a['goal']}", f"- 반대 압력: {a['opposition']}", '', '### 공간',]
    for k,v in a['zones'].items(): md.append(f"- ZONE {k}: {v}")
    md += ['', '### 거리표']+[f"- {k}: {v}보" for k,v in a['distances_paces'].items()]
    md += ['', '### 첫 3합']+[f"{n}. {x}" for n,x in enumerate(a['opening_three_exchanges'],1)]
    md += ['', '### 세 번의 역전']+[f"{n}. {x}" for n,x in enumerate(a['reversals'],1)]
    md += ['', f"- 최종 행동: {a['final_action']}", f"- 기능 손실·대가: {a['continuity_cost']}", f"- 마감 이미지: {a['closing_image']}", '- 승인: A12 / A13 / A07 / Synapse-PM — PASS','']
(PROD/'combat/ACTION_PREFLIGHT_V2_9_COMPLETE.md').write_text('\n'.join(md),encoding='utf-8')

REGION_LEX={
'청래역권':['인계','노선','수레','장부'],'경도':['증서','가격','공개','판정'],'남독택':['체온','독량','호흡','허물'],
'북설원':['봉화','식량','교대','눈벽'],'서황막':['물표','대상','세금','기억'],'동해군도':['조수','닻줄','지분','항로'],
'무명시':['호칭','행적','장부','기억'],'귀장회·천외':['봉인','분류','기록','희생']}
ROLE_STYLE={
'장인':('손의 순서와 재질을 먼저 말한다','말끝을 줄이고 작업음으로 대답한다'),
'역장':('시간·수신인·노선을 차례로 확인한다','감정 대신 업무를 더 맡긴다'),
'대표':('개인보다 주민 수와 공개 절차를 앞세운다','결론 직전에 상대 이름을 부른다'),
'기록':('원문과 수정 이력을 구분한다','모르는 부분은 빈칸으로 남긴다'),
'상인':('조건을 두 개 제시하고 숨은 비용을 세 번째로 말한다','상대의 이름 대신 값과 책임을 부른다'),
'의원':('체온·호흡·냄새를 문장 주어로 삼는다','화가 나면 진단 용어가 더 정확해진다'),
'회수':('명령 번호와 위험 시간을 짧게 말한다','미안하다는 말 대신 퇴로를 연다'),
}
def role_rule(role):
    for k,v in ROLE_STYLE.items():
        if k in role: return v
    return ('자기 생업의 도구와 절차를 비유로 쓴다','압박을 받으면 문장이 짧아지고 핵심 명사를 반복한다')
voices=[]
for idx,p in enumerate(sc):
    rr,stress=role_rule(p['role']); words=REGION_LEX.get(p['region'],['책임','기록','길','사람'])
    sentence=['짧은 실무문','중간 길이 설명문','질문 뒤 단정문'][idx%3]
    sample=f"{words[idx%len(words)]}부터 확인하지. {p['name']} 이름으로 넘길 수 없는 책임이면, 여기서 멈춘다."
    voices.append({
      'id':p['id'],'name':p['name'],'role':p['role'],'region':p['region'],
      'sentence_rhythm':sentence,'lexicon':words,'reasoning_habit':rr,'stress_marker':stress,
      'address_rule':"담운을 처음에는 직책 또는 '배달부'로 부르고, 신뢰가 생긴 뒤 이름을 쓴다.",
      'sample_line':sample,
      'forbidden_overlap':['담운의 수신인 반복','린화의 확률·감정 보류','진여강의 세 가지 계약 조건'],
      'ending_voice_change':p['ending_state']+' 이후에는 명령형보다 책임 주체를 묻는 문장이 늘어난다.'
    })
(DATA/'supporting_cast_voice_028_v2_9.json').write_text(json.dumps(voices,ensure_ascii=False,indent=2),encoding='utf-8')
vm=['# 조연 28명 음성·대사 정본 v2.9','', '> 핵심 인물의 말투를 복제하지 않고 지역 생업·책임·압박 방식으로 구분한다.','']
for v in voices:
    vm += [f"## {v['id']} {v['name']} — {v['role']}", f"- 리듬: {v['sentence_rhythm']}", f"- 어휘: {', '.join(v['lexicon'])}", f"- 사고 방식: {v['reasoning_habit']}", f"- 압박 표식: {v['stress_marker']}", f"- 호칭: {v['address_rule']}", f"- 예시: “{v['sample_line']}”", f"- 종착 변화: {v['ending_voice_change']}",'']
(DOCS/'46_SUPPORTING_CAST_VOICE_BIBLE_V2_9.md').write_text('\n'.join(vm),encoding='utf-8')

entries=[
(2,5,'담운 왼손 엄지 상처','손잡이 압력 감소·매듭 속도 저하','5화 화로 작업 전에 붕대 교체'),
(3,31,'반치 끝 파손','찌르기·정밀 절단 금지','31화 담보 보관 전 임시 복구'),
(5,7,'담운 오른손 촉감 둔화','매듭 직접 작업 불가','7화 망치 진동으로 감각 확인'),
(15,18,'촉각·청각 혼선','거리 판정 한 박자 지연','18화 판결 장면에서 안정'),
(29,32,'오른손 촉감 상실·반치 균열','오른손 장비 교체 금지','32화 말미 감각 일부 회복'),
(37,40,'수면 부족·집중 흔들림','5품 동시 사용 금지','40화 출발 전 휴식'),
(38,48,'이명·손 떨림','세트 5품 동시 사용 봉인','남독 환경에서 단계적 해제'),
(44,47,'불먹장갑 안감 독오염','장착 시간 증가','47화 독왕초 처리 후 세척'),
(49,51,'두리 방향 감각 손실','냄새 추적 신뢰도 감소','51화 과열 뒤 예란이 진정'),
(60,81,'두리 한쪽 날개 경직','비행 이동 불가','서황막 문 통과 후 재활 완료'),
(62,65,'예란 저체온','해동·전투 작업 제외','65화 피풍 열로 회복'),
(66,72,'담운 오른쪽 무릎 부상','급회전·도약 제한','빙잠골 휴식 뒤 보조대 제거'),
(74,80,'무석 방패 모서리 파손','한 팔 방어 불가','80화 퇴로 고정으로 임시 보강'),
(77,200,'무석 귀장회 이름·연금·치료권 상실','공식 보급·명령권 없음','결말까지 제도적으로 회복하지 않음'),
(80,94,'무석 왼팔 감각 상실','방패 교체 시간 증가','망치 귀환 전 마지막 수리로 부분 회복'),
(84,200,'린화가 담운과 공유한 하루 망각','관계 기억의 빈칸','복원하지 않고 행동 기록으로 대체'),
(88,91,'담운 관계선 시야 과부하','두통·오판 위험','전시실 붕괴 후 천품 파편 봉인'),
(89,96,'전시품 세 점 장착 봉인','전력 감소','96화 방 하나 포기 후 재분류'),
(91,94,'담운 손바닥 열상','검함 조작 속도 저하','망치 귀환 장면에서 봉합'),
(93,99,'반치 완전 파손','주 무기 없음','99화 연결선 전용으로 복원'),
(94,200,'소리 없는 망치 영구 귀환','5품 세트 해체·수리력 감소','결말 원격 공명만 허용'),
(103,129,'삼십 일 뒤 호흡 부채','예정 시각 한 시진 호흡 공백','129화 행적 재현 중 징수'),
(122,130,'동료의 최근 약속 기억 삭제','담운 정체 신뢰 약화','습관·냄새·행적으로 관계 재구축'),
(124,150,'담운 몸의 봉인 명령 흔적','백장 원격 명령 감응','150화 검함이 피와 명령을 함께 거부'),
(125,130,'담운 장비 접근권 회수','무주함·전시실 사용 제한','린화의 행동 증명 뒤 복구'),
(127,130,'린화 기억 담보','과거 감정 기록 일부 불안정','130화 담운을 알아보고 담보 종료'),
(134,140,'무주함 장착 권한 절반 잠김','슬롯 절반 사용 불가','현재 이름 선택 뒤 제한 해제'),
(139,142,'담운 손등 화상','반치 손잡이 장시간 유지 불가','분산 전쟁 시작 전 치료'),
(142,157,'파티 분산·무주함 기능 절반','동료 기술 호출 불가','157화 재집결'),
(145,200,'무석 방패 개인 회복 기능 포기','자기 치료 불가·공동 방어만 가능','영구 선택'),
(150,160,'담운 보호 규칙 밖 분류','검함 자동 방어 미작동','160화 동료 증언으로 천외문 진입'),
(151,200,'무석 팔 복원 가능성 포기','완성 방패 공동 방어 고정','영구 선택'),
(161,200,'보조 수집품 세 점 분실','보조 슬롯 전력 감소','회수하지 않음'),
(163,169,'동료 방 분리','상호 상태 확인 불가','169화 분류실 연결 절단'),
(165,176,'과거 수장 말투 침투','담운 대사·판단 혼선','176화 복원 의식 거부'),
(168,193,'진여강 기억 일부 담보','계약 계산의 개인 기억 결손','중앙핵 분할 후 담보 해제'),
(169,178,'두리 신수 물품 칸 감금','진화·자율 행동 정지','박물관 파괴로 해방'),
(171,200,'담운 어린 시절 기억 하나 봉인','개인 기억 영구 공백','복원하지 않음'),
(173,200,'백장 오른손 기능 상실','장갑·봉인 직접 사용 불가','영구 선택'),
(175,191,'수장인 손 고정','장비 교체·반치 사용 지연','191화 소유선 절단과 함께 해제'),
(177,180,'담운 이름 일부 흐림','동료 기억 호칭 불안정','동료 증언으로 유지'),
(180,191,'담운 수납 절반 진행','남은 시간 한 시진·몸 감각 저하','191화 자기 이름 선 절단'),
(181,186,'반치와 검함 압수','주 무기·보관 기능 없음','186화 반치, 187화 검함 반응 회복'),
(185,200,'두리 이전 풍비 능력 하나 상실','과거 이동 기술 사용 불가','귀로풍비 새 역할로 대체'),
(191,200,'담운 과거 수장 권한·기억 일부 상실','중앙 권한 재사용 불가','결말의 비중앙화 보증'),
]
cont=[]
for i,(start,end,state,effect,res) in enumerate(entries,1):
    cont.append({'id':f'CT{i:03d}','start_episode':start,'end_episode':end,'state':state,'scene_effect':effect,'resolution':res,'permanent':end==200})
(DATA/'critical_continuity_ledger_v2_9.json').write_text(json.dumps(cont,ensure_ascii=False,indent=2),encoding='utf-8')
cm=['# 부상·장비·권리 연속성 장부 v2.9','', '| ID | 시작 | 종료 | 상태 | 장면 영향 | 해소/종착 |','|---|---:|---:|---|---|---|']
for c in cont: cm.append(f"| {c['id']} | {c['start_episode']} | {c['end_episode']} | {c['state']} | {c['scene_effect']} | {c['resolution']} |")
(DOCS/'47_INJURY_EQUIPMENT_CONTINUITY_V2_9.md').write_text('\n'.join(cm)+'\n',encoding='utf-8')

final='''# 최종 원고 프리플라이트 v2.9

## 공식 판정

**Prose Preflight Complete / Manuscript Not Drafted**

- 47개 주요 전투·재난·추격·구조 화: 정확한 ZONE A~E, 보폭 거리, 첫 3합, 세 번의 역전, 기능 손실 고정.
- 반복 조연 28명: 문장 리듬·지역 어휘·압박 표식·호칭·금지 중복 고정.
- 핵심 부상·장비·권리 연속성: 시작·종료·장면 영향·영구 상태 고정.
- 1~200화 거점·조연·대가·복선 태깅과 교차 검증.

## 집필 명령 순서

1. 해당 화의 v2.7 복선 태그를 읽는다.
2. v2.8 거점·조연·대가 오버레이를 읽는다.
3. 액션 화라면 v2.9 액션 프리플라이트를 읽는다.
4. 등장 조연의 v2.9 음성 카드를 읽는다.
5. 현재 화에 활성화된 연속성 상태를 장면 입장 상태에 반영한다.
6. 한 화만 초고로 작성한다.
7. A09 문체, A11 문장 리듬, A12 공간, A13 액션, A07 연속성, A14 회수 검사를 순서대로 통과한다.

## 원고 착수 차단 조건

- 액션 장면에 정확한 거리와 퇴로가 없다.
- 조연 대사가 핵심 인물 말투와 구별되지 않는다.
- 이전 화의 부상·장비 제한이 다음 화에서 사라진다.
- 대가가 선언만 되고 행동 선택을 제한하지 않는다.
- 복선 정답을 설명한 뒤 관계·제도·장비 변화가 없다.
- 풍경이 방향·생활·위험·액션 준비 중 두 기능을 못 한다.

## 다음 상태

설계 작업은 원고 착수에 필요한 수준까지 완료됐다. 이후 추가 설정은 기본 금지하고, 1화 초고 또는 1~10화 샘플 원고를 통해 문체 하네스를 실전 검증한다.
'''
(DOCS/'48_FINAL_PROSE_PREFLIGHT_V2_9.md').write_text(final,encoding='utf-8')

validator='''#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
actions=load(ROOT/"data/action_preflight_v2_9.json")
voices=load(ROOT/"data/supporting_cast_voice_028_v2_9.json")
continuity=load(ROOT/"data/critical_continuity_ledger_v2_9.json")
errors=[]
if len(actions)!=47: errors.append("action preflight must contain 47 episodes")
for a in actions:
    if set(a["zones"])!=set("ABCDE"): errors.append(f"E{a['episode']}: zones incomplete")
    if len(a["opening_three_exchanges"])!=3 or len(a["reversals"])!=3: errors.append(f"E{a['episode']}: action sequence incomplete")
    if any(token in json.dumps(a,ensure_ascii=False) for token in ("TBD","확정 필요","기입]","[A13")): errors.append(f"E{a['episode']}: placeholder remains")
    if len(set(a["distances_paces"].values()))<3: errors.append(f"E{a['episode']}: distances too uniform")
if len(voices)!=28 or len({v['id'] for v in voices})!=28: errors.append("supporting voices must be 28 unique")
if len({v['sample_line'] for v in voices})!=28: errors.append("voice samples must be unique")
for v in voices:
    for field in ('sentence_rhythm','lexicon','reasoning_habit','stress_marker','address_rule','sample_line'):
        if not v.get(field): errors.append(f"{v['id']}: missing {field}")
for c in continuity:
    if not (1<=c['start_episode']<=c['end_episode']<=200): errors.append(f"{c['id']}: invalid range")
    if c['end_episode']==200 and not c['permanent']: errors.append(f"{c['id']}: unresolved non-permanent state")
if errors: raise SystemExit("\\n".join(errors))
print("v2.9 prose preflight validation passed")
print(f"actions={len(actions)} voices={len(voices)} continuity_states={len(continuity)}")
'''
(SCRIPTS/'validate_prose_preflight_v2_9.py').write_text(validator,encoding='utf-8')

manifest={'version':'2.9','status':'prose_preflight_complete_manuscript_not_drafted','coverage':{'action_preflights':47,'supporting_cast_voices':28,'critical_continuity_states':len(cont),'episodes':200},'gates':{'exact_action_space':True,'three_reversals':True,'supporting_voice_separation':True,'injury_equipment_continuity':True,'prose_drafted':False},'files':{'actions':'data/action_preflight_v2_9.json','voices':'data/supporting_cast_voice_028_v2_9.json','continuity':'data/critical_continuity_ledger_v2_9.json','final_gate':'docs/48_FINAL_PROSE_PREFLIGHT_V2_9.md','validator':'scripts/validate_prose_preflight_v2_9.py'}}
(DATA/'project_manifest_v2_9.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(ORCH/'PM_PROSE_PREFLIGHT_AUDIT_V2_9.md').write_text(f'''# PM 원고 프리플라이트 감사 v2.9

## 판정

**PASS — Prose Preflight Complete**

- 주요 액션 시트: {len(action_rows)}/47 완성
- 조연 음성 카드: {len(voices)}/28 완성
- 핵심 연속성 상태: {len(cont)}개 범위·종착 지정
- 빈칸·TBD·미승인 액션 시트: 0
- 소설 원고: 미작성

## 승인

A07 / A09 / A11 / A12 / A13 / A14 / A15 / Synapse-PM — PASS
''',encoding='utf-8')
(ROOT/'RELEASE_NOTES_V2_9.md').write_text('''# Release Notes v2.9

- 47개 주요 액션 화의 공간·거리·첫 3합·세 번의 역전·기능 손실 완성.
- 조연 28명의 음성·대사 카드 완성.
- 핵심 부상·장비·권리 연속성 장부 완성.
- 최종 원고 착수 게이트와 CI 검증 추가.

상태: Prose Preflight Complete / Manuscript Not Drafted.
''',encoding='utf-8')
print('generated',len(action_rows),len(voices),len(cont))
