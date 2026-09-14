#!/usr/bin/env python3
"""
📺 K-Drama US Streaming TV Guide Generator & Synchronizer (Live Weekly On-Air Edition)
Description: Generates a clean weekly schedule matrix for THIS WEEK and NEXT WEEK, and syncs
the HTML dashboard & Markdown note. Dramas are scheduled by exact calendar date (drama["schedule"]
maps "YYYY-MM-DD" -> episode label), so the same data naturally supports any number of weeks.
"""

import json
import math
import re
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent.resolve()
JSON_PATH = BASE_DIR / "dramas.json"
MD_PATH = BASE_DIR / "K_DRAMA_TV_GUIDE.md"
HTML_PATH = BASE_DIR / "kdrama_tv_guide.html"

WEEK_OFFSETS = [-1, 0, 1]  # 지난 주, 이번 주, 다음 주. 범위를 늘리고 싶으면 이 리스트만 바꾸면 됨 (예: [-1, 0, 1, 2]).

CHANNELS = [
  # Netflix/Disney+/Prime Video/Apple TV+는 한국에서도 그대로 서비스되는 글로벌 앱이라 두 지역 모두에 해당.
  # Viki/Kocowa는 해외 시청자 대상 서비스라 한국 현지에서는 안 쓰여 US 전용으로 둔다.
  {"id": "Netflix", "badge": "`CH 01 NETFLIX`", "name": "Netflix", "num": "CH 01", "cssClass": "ch-num-netflix", "regions": ["US", "KR"]},
  {"id": "Hulu", "badge": "`CH 02 HULU / D+`", "name": "Hulu / Disney+", "num": "CH 02", "cssClass": "ch-num-hulu", "regions": ["US", "KR"]},
  {"id": "Prime Video", "badge": "`CH 03 PRIME VIDEO`", "name": "Prime Video", "num": "CH 03", "cssClass": "ch-num-prime", "regions": ["US", "KR"]},
  {"id": "Apple TV+", "badge": "`CH 04 APPLE TV+`", "name": "Apple TV+", "num": "CH 04", "cssClass": "ch-num-apple", "regions": ["US", "KR"]},
  {"id": "Viki", "badge": "`CH 05 RAKUTEN VIKI`", "name": "Rakuten Viki", "num": "CH 05", "cssClass": "ch-num-viki", "regions": ["US"]},
  {"id": "Kocowa", "badge": "`CH 06 KOCOWA+`", "name": "KOCOWA+", "num": "CH 06", "cssClass": "ch-num-kocowa", "regions": ["US"]},
  # 한국 방영/서비스 전용 채널.
  {"id": "SBS", "badge": "`KR 01 SBS`", "name": "SBS", "num": "KR 01", "cssClass": "ch-num-sbs", "regions": ["KR"]},
  {"id": "MBC", "badge": "`KR 02 MBC`", "name": "MBC", "num": "KR 02", "cssClass": "ch-num-mbc", "regions": ["KR"]},
  {"id": "KBS2", "badge": "`KR 03 KBS2`", "name": "KBS2", "num": "KR 03", "cssClass": "ch-num-kbs2", "regions": ["KR"]},
  {"id": "KBS Joy", "badge": "`KR 04 KBS JOY`", "name": "KBS Joy", "num": "KR 04", "cssClass": "ch-num-kbsjoy", "regions": ["KR"]},
  {"id": "tvN", "badge": "`KR 05 tvN`", "name": "tvN", "num": "KR 05", "cssClass": "ch-num-tvn", "regions": ["KR"]},
  {"id": "JTBC", "badge": "`KR 06 JTBC`", "name": "JTBC", "num": "KR 06", "cssClass": "ch-num-jtbc", "regions": ["KR"]},
  {"id": "ENA", "badge": "`KR 07 ENA`", "name": "ENA", "num": "KR 07", "cssClass": "ch-num-ena", "regions": ["KR"]},
  {"id": "KBS1", "badge": "`KR 08 KBS1`", "name": "KBS1", "num": "KR 08", "cssClass": "ch-num-kbs1", "regions": ["KR"]},
  {"id": "OCN", "badge": "`KR 09 OCN`", "name": "OCN", "num": "KR 09", "cssClass": "ch-num-ocn", "regions": ["KR"]},
  {"id": "Channel A", "badge": "`KR 10 CHANNEL A`", "name": "Channel A", "num": "KR 10", "cssClass": "ch-num-chana", "regions": ["KR"]},
  {"id": "MBN", "badge": "`KR 11 MBN`", "name": "MBN", "num": "KR 11", "cssClass": "ch-num-mbn", "regions": ["KR"]},
  {"id": "TV Chosun", "badge": "`KR 12 TV CHOSUN`", "name": "TV Chosun", "num": "KR 12", "cssClass": "ch-num-tvchosun", "regions": ["KR"]},
  {"id": "TVING", "badge": "`KR 13 TVING`", "name": "TVING", "num": "KR 13", "cssClass": "ch-num-tving", "regions": ["KR"]},
  {"id": "Wavve", "badge": "`KR 14 WAVVE`", "name": "Wavve", "num": "KR 14", "cssClass": "ch-num-wavve", "regions": ["KR"]},
  {"id": "Coupang Play", "badge": "`KR 15 COUPANG PLAY`", "name": "Coupang Play", "num": "KR 15", "cssClass": "ch-num-coupang", "regions": ["KR"]}
]

_KR_DAY_NAMES = [("Mon", "월"), ("Tue", "화"), ("Wed", "수"), ("Thu", "목"), ("Fri", "금"), ("Sat", "토"), ("Sun", "일")]
_KR_WEEK_LABEL = {-1: "지난 주", 0: "이번 주", 1: "다음 주", 2: "다다음 주"}


def build_week(offset=0, today=None):
    """offset=0(이번 주)/1(다음 주)/... 기준으로 해당 주 월~일 날짜와 라벨을 자동 계산한다.
    더 이상 날짜를 하드코딩하지 않으므로 스크립트를 실행하는 시점이 언제든 항상 맞는 날짜가 나온다."""
    today = today or datetime.now()
    this_monday = today - timedelta(days=today.weekday())
    monday = this_monday + timedelta(weeks=offset)
    sunday = monday + timedelta(days=6)

    days = []  # (day_key, date, label)
    for i, (key, kr) in enumerate(_KR_DAY_NAMES):
        d = monday + timedelta(days=i)
        label = f"{kr} ({d.month}/{d.day})"
        if d.date() == today.date():
            label += " (오늘)"
        days.append((key, d.date(), label))

    iso_year, iso_week, _ = monday.isocalendar()
    week_tag = f"{iso_year}-W{iso_week:02d} ({monday.month:02d}/{monday.day:02d} ~ {sunday.month:02d}/{sunday.day:02d})"
    week_title = f"{monday.year}년 {monday.month}월 {(monday.day - 1) // 7 + 1}주차 ({monday.month}/{monday.day} ~ {sunday.month}/{sunday.day})"
    fallback_label = f"{abs(offset)}주 전" if offset < 0 else f"{offset}주 후"
    week_kr = _KR_WEEK_LABEL.get(offset, fallback_label)
    return {
        "offset": offset,
        "label": week_kr,
        "days": days,
        "sunday": sunday.date(),
        "tag": week_tag,
        "title": week_title,
    }


def load_dramas():
    if not JSON_PATH.exists():
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_cell(d, channel_id, is_batch=False, ep_label=""):
    plat_obj = drama_platform_for(d, channel_id) or d.get("platforms", [{}])[0]
    url = plat_obj.get("url", "#")
    if is_batch:
        ep_label = d.get("batchEp", "전편")
    return f"[{d['title']}]({url}) `{ep_label}`"


def drama_platform_for(d, channel_id):
    return next((p for p in d.get("platforms", []) if channel_id in p["name"]), None)


def batch_window(d):
    """전편 공개(batch) 작품이 편성표에 노출되는 [시작일, 종료일) 구간을 계산한다.
    12부작이면 6주, 즉 '주 2회 편성이었다면 걸렸을 기간'만큼 공개일로부터 계속 보여준다 (회차 / 2 = 주 수)."""
    release = datetime.fromisoformat(d["releaseDate"]).date()
    m = re.search(r"\d+", d.get("episodes", ""))
    ep_count = int(m.group()) if m else 2
    visible_weeks = max(1, math.ceil(ep_count / 2))
    return release, release + timedelta(weeks=visible_weeks)


def channel_active(dramas, ch, today):
    """최근 2주 넘게 새로 뜬 게 없는 채널(행)은 접어서(마크다운에서는 아예 생략) 보여준다.
    정규 편성은 schedule 날짜 중 (오늘-14일) 이후가 하나라도 있으면, 전편 공개/라이브러리 추가는
    공개일 자체가 최근 14일 이내이거나 아직 배치 노출 기간(batch_window) 안이면 활성으로 본다 —
    해외 플랫폼이 오래된 국내 드라마를 뒤늦게 라이브러리에 새로 들여온 경우도 그 노출 기간 동안은 활성."""
    cutoff = today - timedelta(days=14)
    for d in dramas:
        if not drama_platform_for(d, ch["id"]):
            continue
        if d.get("isBatch"):
            if not d.get("releaseDate"):
                continue
            release, window_end = batch_window(d)
            if release >= cutoff or today < window_end:
                return True
        else:
            if any(datetime.fromisoformat(ds).date() >= cutoff for ds in d.get("schedule", {})):
                return True
    return False


def generate_markdown(dramas, weeks):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    current_week = next((w for w in weeks if w["offset"] == 0), weeks[0])
    active_channels = [ch for ch in CHANNELS if channel_active(dramas, ch, datetime.now().date())]

    md = []
    md.append("---")
    md.append("project: Playground")
    md.append("type: guide")
    md.append("status: active_weekly")
    md.append(f"week: {current_week['tag']}")
    md.append("tags: [kdrama, streaming, us_tv_guide, tv_schedule, channel_matrix, live_weekly]")
    md.append("---\n")

    md.append("# 한국·미국 K-드라마 생방송 편성표 (지난 주 + 이번 주 + 다음 주)")
    md.append(f"> **기준 주차**: `{current_week['title']}` | **기준 시간**: `{now_str}`\n")

    md.append("> [!TIP] **레트로 웹 대시보드 바로가기**")
    md.append("> 브라우저에서 타이포 중심의 미니멀한 화면으로, 지난 주/이번 주/다음 주 탭을 눌러가며 보려면:")
    md.append("> **[kdrama_tv_guide.html](file:///" + str(HTML_PATH) + ")** 파일을 더블 클릭하여 열어보세요!\n")

    # 1. Authentic Clean TV Guide Matrix Table — one per week
    for week in weeks:
        md.append(f"## {week['label']} 편성표 ({week['title']})")
        md.append("각 드라마 제목을 클릭하면 해당 OTT의 본방 시청 페이지로 바로 이동합니다.\n")

        header_cols = ["채널 / OTT"] + [label for _, _, label in week["days"]] + ["전편 공개 (Batch)"]
        md.append("| " + " | ".join(header_cols) + " |")
        md.append("| " + " | ".join([":---"] + [":---"] * 8) + " |")

        week_monday = week["days"][0][1]

        for ch in active_channels:
            row_cells = [f"**{ch['badge']}**"]

            for day_key, day_date, _ in week["days"]:
                date_str = day_date.isoformat()
                day_dramas = [
                    d for d in dramas
                    if drama_platform_for(d, ch["id"]) and date_str in d.get("schedule", {})
                ]
                # 전편 공개작은 공개된 그 날짜의 요일 칸에도 표시한다 (예: 들쥐는 8/28 금요일 칸에).
                batch_today = [
                    d for d in dramas
                    if drama_platform_for(d, ch["id"]) and d.get("isBatch") and d.get("releaseDate") == date_str
                ]
                cells = [format_cell(d, ch["id"], ep_label=d["schedule"][date_str]) for d in day_dramas]
                cells += [format_cell(d, ch["id"], is_batch=True) for d in batch_today]
                row_cells.append("<br>".join(cells) if cells else "-")

            # 전편 공개(Batch) 열: 공개된 주가 지난 뒤부터 (회차/2)주 동안 "계속 볼 수 있는 작품"으로 노출.
            # 공개된 바로 그 주는 위에서 실제 공개 날짜 칸에 표시했으므로 이 열에서는 제외해 중복을 막는다.
            batch_dramas = []
            for d in dramas:
                if not (drama_platform_for(d, ch["id"]) and d.get("isBatch", False) and d.get("releaseDate")):
                    continue
                release, window_end = batch_window(d)
                if release < week_monday and week_monday < window_end:
                    batch_dramas.append(d)
            if batch_dramas:
                batch_cell = "<br>".join(format_cell(d, ch["id"], is_batch=True) for d in batch_dramas)
            else:
                batch_cell = "-"
            row_cells.append(batch_cell)

            md.append("| " + " | ".join(row_cells) + " |")

        md.append("")

    md.append("---\n")

    # 2. Detailed Program Directory (모든 주 통합 — 채널별 현재/예정 프로그램 한눈에 보기)
    md.append("## 채널별 프로그램 상세 (Live + Upcoming)")
    md.append("> 최근 2주 넘게 새로 뜬 게 없는 채널은 목록에서 접혀 있습니다 (해외 스트리밍의 뒤늦은 라이브러리 추가는 그 노출 기간 동안 계속 활성으로 집니다).\n")
    for ch in active_channels:
        ch_dramas = [d for d in dramas if drama_platform_for(d, ch["id"])]
        md.append(f"### {ch['badge']}")
        if not ch_dramas:
            md.append("*편성 없음*\n")
            continue

        for d in ch_dramas:
            plat_url = drama_platform_for(d, ch["id"])["url"]
            if d.get("isBatch"):
                badge = f" `[전편 공개: {d.get('releaseDate', '?')}~]`"
            else:
                air_dates = sorted(d.get("schedule", {}).keys())
                badge = f" `[방영일: {', '.join(air_dates)}]`" if air_dates else ""
            verified = d.get("verifiedAt")
            verified_tag = f" `(확인: {verified})`" if verified else ""
            md.append(f"- **[{d['title']} ({d['engTitle']})]({plat_url})**{badge}{verified_tag} — 📊 시청률 {d['rating']} | {d['episodes']} | {d['cast']}")
            md.append(f"  > {d['synopsis']}")
        md.append("")

    # 3. Data freshness banner — dramas.json이 오래되면 경고를 남겨 다음 리서치 시점을 알려준다.
    if JSON_PATH.exists():
        age_days = (datetime.now().timestamp() - JSON_PATH.stat().st_mtime) / 86400
        md.append("---\n")
        if age_days > 7:
            md.append(f"> [!WARNING] **데이터가 {age_days:.0f}일 전에 마지막으로 업데이트되었습니다.** "
                       f"`REFRESH_GUIDE.md`의 절차대로 최신 편성 정보를 다시 리서치해 `dramas.json`을 갱신해 주세요.\n")
        else:
            md.append(f"> [!NOTE] 데이터 최종 확인: `{age_days:.1f}일 전`. 신선한 상태입니다. (기준: 7일 초과 시 재확인 권장)\n")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"✅ Generated Clean Matrix Markdown: {MD_PATH}")


def update_html_with_json(dramas):
    if not HTML_PATH.exists():
        return
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    start_tag = "const DRAMA_DATA = "
    end_tag = "];\n\n// CHANNELS"

    s_idx = html_content.find(start_tag)
    e_idx = html_content.find(end_tag)

    if s_idx != -1 and e_idx != -1:
        json_str = json.dumps(dramas, ensure_ascii=False, indent=2)
        new_html = html_content[:s_idx + len(start_tag)] + json_str + html_content[e_idx + 1:]
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"✅ Synced HTML Dashboard with latest JSON: {HTML_PATH}")


def main():
    dramas = load_dramas()
    print(f"Loaded {len(dramas)} dramas.")
    weeks = [build_week(offset=i) for i in WEEK_OFFSETS]
    generate_markdown(dramas, weeks)
    update_html_with_json(dramas)


if __name__ == "__main__":
    main()
