#!/usr/bin/env python3
"""
Interactive CLI tool to easily add a new drama to dramas.json and re-sync everything.
"""

import json
import sys
from datetime import date
from pathlib import Path
from fetch_kdrama_schedule import main as sync_all

BASE_DIR = Path(__file__).parent.resolve()
JSON_PATH = BASE_DIR / "dramas.json"

# 요일 카테고리 → 실제 airDays 키(Mon~Sun). fetch_kdrama_schedule.py의 매트릭스는
# 이 키들로만 채널×요일 셀을 채우므로, 여기서 실제 스케줄 키로 변환해야 가이드에 반영된다.
DAY_CATEGORY_MAP = {
    "1": ("월화", ["Mon", "Tue"]),
    "2": ("수목", ["Wed", "Thu"]),
    "3": ("금토", ["Fri", "Sat"]),
    "4": ("주말(토일)", ["Sat", "Sun"]),
    "5": ("OTT 전편 공개(배치)", []),
}

def add_drama_cli():
    print("========================================")
    print("📺 신규 K-드라마 등록 마법사 (US Guide)")
    print("========================================")

    title = input("1. 한국어 제목 (예: 눈물의 여왕): ").strip()
    if not title:
        print("제목은 필수입니다.")
        return

    eng_title = input("2. 영어 제목 (예: Queen of Tears): ").strip()
    id_slug = input(f"3. 고유 ID (기본값: {eng_title.lower().replace(' ', '-')}): ").strip() or eng_title.lower().replace(' ', '-')

    print("\n[요일 카테고리 선택]")
    print("1) 월화  2) 수목  3) 금토  4) 주말  5) OTT 전편 공개(배치)")
    day_choice = input("선택 (1~5): ").strip()
    day_cat, air_days = DAY_CATEGORY_MAP.get(day_choice, DAY_CATEGORY_MAP["5"])
    is_batch = (day_choice == "5")

    time_str = input("4. 방영 시간 / 주기 (예: 21:20 KST / 전편 공개): ").strip() or "21:00 KST"
    status = input("5. 상태 [Completed / Airing / Upcoming] (기본: Completed): ").strip() or "Completed"
    genre_raw = input("6. 장르 (쉼표 구분, 예: 로맨스, 코미디, 스릴러): ").strip() or "드라마"
    genres = [g.strip() for g in genre_raw.split(",") if g.strip()]

    episodes = input("7. 회차 정보 (예: 16부작 / 8부작): ").strip() or "16부작"
    rating = input("8. 닐슨코리아 시청률 % (예: 4.0, 모르면 'TBD'): ").strip() or "TBD"
    cast = input("9. 주요 출연진 (예: 김수현, 김지원): ").strip()
    synopsis = input("10. 1줄 시놉시스/줄거리: ").strip()
    
    print("\n[미국 스트리밍 플랫폼]")
    print("쉼표로 구분하여 번호 입력: 1) Netflix 2) Viki 3) Kocowa 4) Hulu/Disney+ 5) Prime Video 6) Apple TV+")
    plat_choice = input("선택 (예: 1,2): ").strip()
    plat_dict = {
        "1": {"name": "Netflix", "label": "Netflix US", "url": "https://www.netflix.com"},
        "2": {"name": "Viki", "label": "Rakuten Viki", "url": "https://www.viki.com"},
        "3": {"name": "Kocowa", "label": "Kocowa+", "url": "https://www.kocowa.com"},
        "4": {"name": "Hulu", "label": "Hulu / Disney+", "url": "https://www.hulu.com"},
        "5": {"name": "Prime Video", "label": "Prime Video", "url": "https://www.amazon.com"},
        "6": {"name": "Apple TV+", "label": "Apple TV+", "url": "https://tv.apple.com"}
    }
    platforms = []
    for c in plat_choice.split(","):
        c = c.strip()
        if c in plat_dict:
            custom_url = input(f"   * {plat_dict[c]['label']} 직링크 URL (Enter시 기본 URL): ").strip()
            item = dict(plat_dict[c])
            if custom_url:
                item["url"] = custom_url
            platforms.append(item)
            
    new_drama = {
        "id": id_slug,
        "title": title,
        "engTitle": eng_title,
        "airDays": air_days,
        "dayEpisodes": {},
        "isBatch": is_batch,
        "dayCategory": day_cat,
        "time": time_str,
        "status": status,
        "genre": genres,
        "episodes": episodes,
        "rating": rating,
        "cast": cast,
        "synopsis": synopsis,
        "platforms": platforms,
        "poster": "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?auto=format&fit=crop&w=300&q=80",
        "verifiedAt": date.today().isoformat()
    }
    if is_batch:
        new_drama["batchEp"] = f"{episodes} 전편 공개"

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    data = [d for d in data if d["id"] != id_slug]
    data.insert(0, new_drama)
    
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 '{title}' 등록 완료! 마크다운 및 대시보드를 동기화합니다...")
    sync_all()
    print("✅ 동기화 완료!")

if __name__ == "__main__":
    add_drama_cli()
