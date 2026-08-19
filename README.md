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
