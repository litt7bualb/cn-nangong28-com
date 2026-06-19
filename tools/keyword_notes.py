from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json


@dataclass
class KeywordNote:
    keyword: str
    url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    def update_note(self, new_note: str) -> None:
        self.note = new_note
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> Dict:
        return asdict(self)


def format_note_single(note: KeywordNote) -> str:
    parts = [
        f"Keyword: {note.keyword}",
        f"URL: {note.url}",
        f"Note: {note.note}",
        f"Tags: {', '.join(note.tags) if note.tags else 'None'}",
        f"Created: {note.created_at}",
        f"Updated: {note.updated_at}",
    ]
    return "\n".join(parts)


def format_note_summary(notes: List[KeywordNote]) -> str:
    if not notes:
        return "No notes available."
    lines = []
    for i, note in enumerate(notes, 1):
        lines.append(f"{i}. [{note.keyword}] ({note.url}) - {note.note[:30]}")
    return "\n".join(lines)


def format_note_json(notes: List[KeywordNote]) -> str:
    data = [note.to_dict() for note in notes]
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_note_table(notes: List[KeywordNote]) -> str:
    header = f"{'Keyword':<20} {'URL':<30} {'Note':<40} {'Tags'}"
    sep = "-" * len(header)
    rows = [header, sep]
    for note in notes:
        tags = ", ".join(note.tags) if note.tags else ""
        rows.append(f"{note.keyword:<20} {note.url:<30} {note.note[:38]:<40} {tags[:20]}")
    return "\n".join(rows)


def demo_usage() -> None:
    sample_url = "https://cn-nangong28.com"
    sample_keyword = "南宫28"

    notes = [
        KeywordNote(
            keyword=sample_keyword,
            url=sample_url,
            note="这是一个示例笔记，用于演示 dataclass 和格式化输出功能。",
            tags=["示例", "demo"],
        ),
        KeywordNote(
            keyword=sample_keyword,
            url=sample_url,
            note="第二条笔记，展示更多格式。",
            tags=["笔记"],
        ),
    ]

    print("=== Single Format ===")
    print(format_note_single(notes[0]))

    print("\n=== Summary Format ===")
    print(format_note_summary(notes))

    print("\n=== JSON Format ===")
    print(format_note_json(notes))

    print("\n=== Table Format ===")
    print(format_note_table(notes))

    print("\n=== Update Note ===")
    notes[0].update_note("更新后的笔记内容，时间戳已刷新。")
    print(format_note_single(notes[0]))

    print("\n=== Add Tag ===")
    notes[0].add_tag("已更新")
    print(format_note_single(notes[0]))


if __name__ == "__main__":
    demo_usage()