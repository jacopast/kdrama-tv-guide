# 📺 U.S. K-Drama TV Guide (미국 K-드라마 채널별 주간 편성표)

미국 거주자를 위해 **Netflix, Rakuten Viki, Kocowa+, Hulu/Disney+, Amazon Prime Video, Apple TV+** 등 6대 스트리밍 서비스(채널)를 **행(ROW)**으로, **월~일 요일 및 전편 일괄(Batch) 공개**를 **열(COLUMN)**로 배치한 전통적인 레트로 TV 가이드 매트릭스 시스템입니다.

---

## 🌟 편성표 매트릭스 구조 (TV Guide Matrix)

```
+-------------------+---------+---------+---------+---------+---------+---------+---------+--------------------+
| CHANNEL / OTT     | 월(MON) | 화(TUE) | 수(WED) | 목(THU) | 금(FRI) | 토(SAT) | 일(SUN) | ⚡ 전편 일괄(BATCH)|
+-------------------+---------+---------+---------+---------+---------+---------+---------+--------------------+
| CH 01 NETFLIX     |         |         |         |         |  금요드 | 주말드  | 주말드  | 더글로리, 오겜2 등 |
| CH 02 VIKI        | 월화드  | 월화드  | 수목드  | 수목드  | 금토드  | 금토드  | 일요드  |                    |
| CH 03 KOCOWA+     |         |         |         |         | 금토드  | 금토드  |         | 지상파 VOD/주말극  |
| CH 04 HULU / D+   |         |         | 수요오리지널      | 금토드  | 금토드  |         | 무빙, 킬러쇼핑몰 등|
| CH 05 PRIME VIDEO | 월화드  | 월화드  |         |         | 금요드  |         |         | 내남결, 이재죽 등  |
| CH 06 APPLE TV+   |         |         |         |         | 금요드  |         |         | 파친코 S2          |
+-------------------+---------+---------+---------+---------+---------+---------+---------+--------------------+
```

---

## 📂 파일 구성

| 파일명 | 유형 | 설명 |
| :--- | :--- | :--- |
| **[`kdrama_tv_guide.html`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/kdrama_tv_guide.html)** | **인터랙티브 웹 앱** | `ROW=채널`, `COL=요일` 정통 매트릭스 그리드, 좌측 채널 고정 스크롤, CRT/신문 테마, 룰렛 |
| **[`K_DRAMA_TV_GUIDE.md`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/K_DRAMA_TV_GUIDE.md)** | **옵시디언 마크다운** | 옵시디언 노트에서 바로 보는 채널×요일 매트릭스 마크다운 테이블 및 채널별 상세 디렉토리 |
| **[`dramas.json`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/dramas.json)** | **데이터베이스** | 방영 요일 배열(`airDays`), 전편 공개 여부(`isBatch`), 미국 스트리밍 직링크 메타데이터 |
| **[`fetch_kdrama_schedule.py`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/fetch_kdrama_schedule.py)** | **동기화 엔진** | JSON을 기반으로 매트릭스 마크다운과 HTML 대시보드를 일괄 동기화하는 파이썬 스크립트 |
| **[`add_drama.py`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/add_drama.py)** | **CLI 도구** | 신규 드라마를 요일별/전편일괄 태그와 함께 추가하고 자동 동기화 |
| **[`REFRESH_GUIDE.md`](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/REFRESH_GUIDE.md)** | **최신화 워크플로우** | 웹 검색으로 dramas.json을 정기적으로 실제 데이터로 검증·교체하는 절차와 Claude용 프롬프트 |

---

## 🚀 실행 및 활용

1. **브라우저에서 대시보드 열기**:
   - [kdrama_tv_guide.html](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/kdrama_tv_guide.html) 파일을 더블 클릭하거나 브라우저로 열기.
2. **신규 드라마 추가 & 재동기화**:
   ```bash
   python3 fetch_kdrama_schedule.py
   ```
3. **데이터 최신화 (7일 이상 지났을 때)**:
   - [REFRESH_GUIDE.md](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/REFRESH_GUIDE.md) 의 프롬프트를 그대로 웹 검색 가능한 에이전트(Claude)에게 붙여넣어 `dramas.json`을 실제 편성 데이터로 갱신.

---

## 📝 변경 이력 (Changelog)

- **2026-08-19 [Claude/Cowork]**: 안티그래비티가 채운 `dramas.json`에 이미 종영했거나 존재하지 않는 편성(예: 옛날 시즌 정보, 가짜 URL)이 섞여 있던 문제를 웹 검색으로 실제 소스(Soompi, ScreenRant, 나무위키, 위키백과, 각 플랫폼 공식 페이지, 닐슨코리아 시청률)를 확인해 5개 항목으로 재작성. `fetch_kdrama_schedule.py`의 요일/주차 계산을 하드코딩 날짜에서 실행 시점 자동 계산으로 변경(`build_week()`), `kdrama_tv_guide.html`도 로드 시 헤더 날짜를 자동 계산하도록 수정(`updateDateHeaders()`). 평점(⭐) 필드를 실제 닐슨코리아 시청률(%)로 교체. 7일 이상 미갱신 시 경고 배너 추가, 정기 최신화 절차는 [REFRESH_GUIDE.md](file:///Users/sunghwanyoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/Obsvault/플레이그라운드/드라마/REFRESH_GUIDE.md) 참고.
- **2026-08-19 [Claude/Cowork] (2차)**: "이번 주만 보임" 요청에 따라 이번 주 + 다음 주 2주치를 함께 보여주도록 확장. `dramas.json`의 `airDays`/`dayEpisodes`를 날짜 기반 `schedule` 맵(`"2026-08-24": "EP 07"`)으로 스키마 변경해 몇 주가 됐든 확장 가능하게 만듦. `kdrama_tv_guide.html`에 "📅 이번 주 / ▶ 다음 주" 탭 추가. Netflix 8/28 공개 예정 『들쥐(Mousetrap)』을 다음 주 편성에 추가로 확인해 반영. 『신병4: 사보타주』, 『포핸즈』는 미국 스트리밍 플랫폼이 아직 확인되지 않아 편성표에서 제외(REFRESH_GUIDE.md 참고). `add_drama.py`도 새 스키마에 맞게 수정.

---

## 🌐 GitHub Pages (친구/SNS 공유용)

**https://jacopast.github.io/kdrama-tv-guide/kdrama_tv_guide.html**

로그인 없이 누구나 바로 열립니다. 저장소: https://github.com/jacopast/kdrama-tv-guide (공개)

업데이트하려면:
```bash
git add -A
git commit -m "드라마 편성 업데이트"
git push
```
푸시하면 1분 정도 뒤 GitHub Pages에 자동 반영됩니다.

- **2026-08-19 [Claude/Cowork] (3차)**: Kocowa+를 채널 목록 맨 아래(CH 06)로 이동. "이런 엿같은 사랑"이 매주 전편 공개 칸에 계속 뜨던 버그 수정 — 이제 배치(전편 공개) 작품은 실제 공개된 그 주에만 표시됨. "◀ 지난 주" 탭 추가로 지난 주/이번 주/다음 주 3주치를 볼 수 있게 확장(`WEEK_OFFSETS = [-1, 0, 1]`). GitHub 저장소(jacopast/kdrama-tv-guide)를 만들고 GitHub Pages로 배포해 로그인 없이 볼 수 있는 공개 링크 추가.
- **2026-08-19 [Claude/Cowork] (4차)**: 전체 스타일을 "종이에 타이핑된" 느낌의 플랫 모노크롬으로 전면 개편 — 버튼/카드/모달의 입체 그림자(box-shadow)와 hover 시 들뜨는 효과, 채널별 브랜드 컬러(Netflix 빨강/Viki 파랑 등)를 모두 제거하고 단일 잉크색+종이색 팔레트로 통일. 폰트도 타이핑 느낌의 모노스페이스(Nanum Gothic Coding)로 교체. 포스터 이미지는 grayscale 필터로 흑백 처리. CRT/모던 테마도 같은 규칙으로 플랫하게 정리(라벨: 종이/다크/네이비). 헤더의 "n주차" 배지가 하드코딩된 날짜였던 걸 오늘 날짜 기준 자동 계산으로 수정.
  전편 공개(batch) 작품 노출 기간도 개선: 공개된 그 주에만 반짝 보이던 것을, "회차수 ÷ 2주"만큼(예: 12부작 → 6주) 계속 볼 수 있도록 변경(`batch_window()`/`getBatchWindow()`).
- **2026-08-19 [Claude/Cowork] (5차)**: 디자인을 "타이포 중심 + 선 사용 최소화"로 재정리 — 표의 모든 칸 테두리를 없애고 헤더 밑줄 1개, 행 구분선 1개, 채널열/전편공개열 경계선 1개만 남김. 버튼도 테두리 박스 대신 밑줄/굵기로 상태 표현. 컬러 이모지(📺📅⭐🎲📊⚡ℹ️🎉 등)를 전부 제거하고 텍스트 라벨 또는 모노크롬 기호(★☆)만 사용. `fetch_kdrama_schedule.py`의 채널 배지 이모지(🔴🔷🟦 등)도 동일하게 정리.
- **2026-08-19 [Claude/Cowork] (6차)**: 검색창과 통계 바(방영작 수/찜 목록/평균 시청률 등)를 제거해 화면을 더 단순하게 정리. 드라마 카드에서 별표·정보 버튼을 제목 옆이 아니라 아래 줄로 내려서 제목이 카드 폭 전체를 쓰도록 변경. 주간 이동을 "지난 주/이번 주/다음 주" 3버튼에서 "◀/▶ + 현재 주 라벨" 방식으로 바꿔 앞뒤로 최대 4주(약 한 달)까지 이동 가능하도록 확장, 이번 주가 아닐 때는 "오늘로" 바로가기가 나타남(키보드 ← →로도 이동 가능).
- **2026-08-19 [Claude/Cowork] (7차)**: Viki를 Kocowa+ 바로 위(CH05)로 내림 — Netflix/Hulu·D+/Prime Video/Apple TV+/Viki/Kocowa+ 순. 전편 공개작(예: 들쥐)은 실제 공개된 날짜의 요일 칸에 먼저 표시되고, 그 주가 지나면 "전편 공개" 열로 넘어가도록 수정(중복 표시 방지). 최애의 사원·재벌X형사 2의 1~2회차를 실제 첫방일 기준으로 채워 넣어 더 과거 주차(8/3~8/9)가 비어 보이지 않게 함. 드라마 제목을 누르면 바로 시청 페이지로 가던 것을, 제목 클릭 시 상세 정보(모달)가 뜨고 실제 시청 링크는 모달 안에서 누르도록 변경 — 카드에서 별도 "정보" 버튼 제거. 에피소드 카드 내부 정렬(제목 아래 줄에 회차·별표를 좌측 정렬로 모아 흩어져 보이던 문제 수정)과 같은 칸에 여러 작품이 겹칠 때의 구분선을 정리. 요청에 따라 Claude Artifact 게시는 이번부터 생략(GitHub Pages만 유지).
- **2026-08-19 [Claude/Cowork] (8차)**: "오늘 뭐 보지?"(룰렛) 기능과 종이/다크/네이비 테마 전환 기능을 제거해 단일 디자인으로 고정. 페이지 배경을 살짝 회색으로, 각 에피소드 박스는 흰색으로 채워 항목 구분이 잘 되도록 변경.
- **2026-08-19 [Claude/Cowork] (9차)**: 셀 테두리 선(가로/세로 구분선)을 전부 제거하고, 모든 요일/전편공개 칸을 항상 흰 박스로 꽉 채워서 박스만으로 구분되게 정리(칸 사이 여백은 `border-spacing`으로 생기는 회색 틈만 사용). 오늘 강조도 칸 배경 대신 헤더에만 살짝 표시.
- **2026-08-19 [Claude/Cowork] (10차)**: 모바일 대응 — 화면이 좁으면 표가 채널별 세로 목록으로 바뀌고, 방영 없는 요일/채널은 자동으로 숨겨서 스크롤을 줄임. "CHANNEL / OTT" 헤더를 "CHANNEL"로 줄이고 채널 열 폭도 최소화(150px→92px). 명도 3단계로 재정리: 페이지 배경(회색) < 일반 에피소드 박스(옅은 회색) < 내가 찜한 작품(흰색) — 빈 칸은 아예 박스 없이 배경에 묻힘.
- **2026-08-19 [Claude/Cowork] (11차)**: 모바일 헤더(제목·날짜 배지)가 어중간하게 줄바꿈되던 것을 세로로 깔끔히 쌓이도록 수정. "월간" 보기 추가 — 채널×요일 격자 대신, 그 달에 실제로 방영/공개되는 날짜만 골라 세로 일정표로 보여주는 방식(빈 날짜는 생략)이 한 달 전체를 훑어보기에 가장 효율적이라 판단해 이렇게 구현. 각 항목에 채널명을 같이 표기(열 구분이 없어서). 최대 3달 앞뒤로 이동 가능, "오늘로" 바로가기 포함.
- **2026-08-19 [Claude/Cowork] (12차)**: 표 칸 사이 간격/여백을 clamp()로 유동화해서, 브라우저 폭을 줄이면(모바일 전환 전 구간에서도) 간격이 하드 브레이크포인트 없이 같이 줄어들도록 수정(테이블 min-width 1200px→700px). 제목 아래 날짜/시간도 폭이 좁아지면 자동으로 자기 줄로 내려가도록 h1 레이아웃을 flex-wrap 기반으로 재구성. 주간 보기에서 그 주 전체가 비어 있으면(아직 리서치 전이거나 방영작이 없는 과거 시점) "확인된 편성 데이터가 없습니다" 안내를 표시해 버그처럼 보이지 않게 함.
- **2026-08-19 [Claude/Cowork] (13차)**: "오늘" 강조를 헤더뿐 아니라 그 요일 칸 전체(위아래)로 확장, 색도 더 진하게. 7월(더 허즈번드·기막힌 사랑·동궁)과 9월(기존 작품들 최종화까지 + 포핸즈·스캔들 신작)까지 실제 리서치 데이터로 확장해서 지난 달/다음 달까지 채움. 월간 보기에서 넓은 화면(900px 이상)은 전통적인 달력 격자로, 좁은 화면은 기존 세로 목록으로 자동 전환. 헤더의 "K-DRAMA US STREAMING TV GUIDE" 제목을 누르면 언제나 이번 주 화면으로 돌아가도록 추가. (요청받은 kiwidisk.com은 비공식/저작권 미허가 사이트로 확인되어 추가하지 않음 — OnDemandKorea/Tubi를 정식 대안으로 제안했으나 채널 추가는 보류.)
- **2026-08-19 [Claude/Cowork] (14차)**: 오늘 칸 강조를 헤더-첫 채널 행 사이 간격은 그대로 두고, 그 아래 채널 행들 사이 간격은 같은 색으로 메워서 컬럼이 끊기지 않고 하나로 이어지도록 개선(표 뒤에 별도 칠 레이어를 깔아 border-spacing 틈을 채움). 창 폭이 바뀌거나(반응형 칸 너비) 찜 목록 필터로 행 수가 바뀔 때도 ResizeObserver로 자동 재계산.
- **2026-08-19 [Claude/Cowork] (15차)**: 페이지 맨 아래에 Threads(@sunghwan.yoon)·Bluesky(@jacopast.com) 링크 푸터 추가.
- **2026-08-19 [Claude/Cowork] (16차)**: 매주 월요일 오전 9시(미국 동부시간) 자동으로 데이터를 리서치·갱신하는 클라우드 예약 작업(routine) 등록. 기존 데이터는 삭제하지 않고 계속 이어붙이는 원칙을 REFRESH_GUIDE.md에 명시. 관리: https://claude.ai/code/routines/trig_015uL2G8vmxwaK4e2Foos3TQ
- **2026-08-19 [Claude/Cowork] (17차)**: 한국 영화(넷플릭스 스트리밍 공개작)도 가이드에 포함하기 시작 — 크로스 2(미션 크로스 2), 가능한 사랑(이창동 감독) 추가. 영화는 기존 전편 공개(batch) 방식 그대로 사용. 정확한 공개일 미발표 작품은 완전히 빼는 대신 확인된 "월"의 1일에 "(미정)" 표시로 임시 배치하고, 날짜 확정되면 다음 자동 갱신 때 교체하는 원칙을 REFRESH_GUIDE.md에 명시(제목 "K-DRAMA TV GUIDE"는 그대로 유지, 영화 포함은 내용만 확장). "스캔들"처럼 불확실성 설명이 길어서 칸을 넘던 항목은 짧은 "(예정)" 표시로 줄이고 자세한 내용은 상세 페이지(줄거리)로 이동.
- **2026-08-19 [Claude/Cowork] (18차)**: "Spooky in Love"의 한글 제목 오기 수정 — "기막힌 사랑"(오역/오타)에서 실제 정식 제목 "오싹한 연애"로 교체.
- **2026-08-19 [Claude/Cowork] (19차)**: 새로 만든 게 아니라 기존작이 플랫폼에 새로 스트리밍 라이브러리 추가되는 경우도 다루기 시작 — "감사합니다"(2024년 tvN 완결작, 2026-08-11 넷플릭스 미국 신규 추가) 추가. "(신작 아님, 라이브러리 추가)" 식으로 구분 표시. REFRESH_GUIDE.md에도 "신작뿐 아니라 기존작 라이브러리 추가도 조사 대상"이라고 명시해서 매주 자동 갱신 때 계속 잡히게 함.
- **2026-08-19 [Claude/Cowork] (20차)**: "아파트"(JTBC, 지성·하윤경·박병은·문소리, 7/11~8/16 방영 완결, 넷플릭스 독점) 추가 — 사용자가 넷플릭스에서 직접 확인해 알려준 누락 건.
- **2026-08-19 [Claude/Cowork] (21차)**: 신뢰도 문제 지적에 따라 리서치 방식 개선 — 기존엔 엔터 뉴스 사이트(신작 프리미어 위주)만 썼는데, 그것만으로는 "기존작이 플랫폼에 새로 풀리는 것"을 구조적으로 놓친다는 걸 확인(아파트 누락이 실제 사례). JustWatch 플랫폼별 "new" 페이지(justwatch.com/us/provider/{netflix,hulu,prime-video,apple-tv-plus,disney-plus}/new)를 매주 필수로 같이 확인하도록 REFRESH_GUIDE.md에 명시. 이 방식으로 즉시 재검증해서 "청부살인자의 가게 시즌 2"(Hulu/Disney+, 7/22~8/12) 추가 발견·반영. (검증 과정에서 후보로 나왔던 Yeonae Silheomsil은 한국 리얼리티쇼, Thunder 3와 GATE24는 일본 작품, Bid Coin Chef는 태국 작품이라 범위 밖으로 제외.)
