"""videos/ と motion/ の中身を調べて videos.json(一覧)を作るスクリプト。
GitHub Actions が自動で実行するので、普段は触らなくて大丈夫です。
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO_EXT = {".mp4", ".m4v", ".mov", ".webm"}


def commit_date(path: Path) -> str:
    """そのファイルが最後に追加・更新された日時(なければ空)。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip()
        return out
    except Exception:
        return ""


def title_of(name: str) -> str:
    return name.replace("_", " ").strip()


def category_of(rel: Path, base: str) -> str:
    # videos/安全教育/xxx.mp4 → 「安全教育」。直下なら「未分類」
    parts = rel.parts
    return parts[1] if len(parts) > 2 else "未分類"


def main():
    items = []

    vdir = ROOT / "videos"
    if vdir.exists():
        for p in sorted(vdir.rglob("*")):
            if p.is_file() and p.suffix.lower() in VIDEO_EXT:
                rel = p.relative_to(ROOT)
                items.append({
                    "type": "video",
                    "title": title_of(p.stem),
                    "category": category_of(rel, "videos"),
                    "src": rel.as_posix(),
                    "size": p.stat().st_size,
                    "date": commit_date(p),
                })

    mdir = ROOT / "motion"
    if mdir.exists():
        for p in sorted(mdir.rglob("*.html")):
            rel = p.relative_to(ROOT)
            # motion/名前/index.html の形なら、フォルダ名をタイトルにする
            if p.name.lower() == "index.html" and p.parent != mdir:
                name = p.parent.name
                cat = rel.parts[1] if len(rel.parts) > 3 else "未分類"
            else:
                # フォルダ型の作品の中にある他の HTML は一覧に出さない
                if (p.parent / "index.html").exists() and p.parent != mdir:
                    continue
                name = p.stem
                cat = category_of(rel, "motion")
            items.append({
                "type": "html",
                "title": title_of(name),
                "category": cat,
                "src": rel.as_posix(),
                "size": p.stat().st_size,
                "date": commit_date(p),
            })

    yt = ROOT / "youtube.json"
    if yt.exists():
        try:
            for e in json.loads(yt.read_text(encoding="utf-8")):
                if e.get("url"):
                    items.append({
                        "type": "youtube",
                        "title": e.get("title") or "YouTube動画",
                        "category": e.get("category") or "未分類",
                        "src": e["url"],
                        "size": 0,
                        "date": e.get("date", ""),
                    })
        except json.JSONDecodeError as err:
            print(f"youtube.json の書き方に誤りがあります: {err}")

    items.sort(key=lambda x: x["date"], reverse=True)
    (ROOT / "videos.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    total = sum(i["size"] for i in items)
    print(f"{len(items)} 件 / 合計 {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
