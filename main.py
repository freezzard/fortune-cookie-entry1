"""Fortune Cookie Wisdom for Developers.

A local tournament of ten original fortune-cookie lines for software
developers.  Each line carries four axis marks — wisdom, developer
relevance, word economy, freshness — and the weighted total decides the
winner.  The winning line is written to ``/output/entry.txt``.  The run is
fully deterministic: the same line wins on every run.

Weights: wisdom x3, developer relevance x2, word economy x2, freshness x1.
Gate: the entry file holds UTF-8 text of 1 to 120 characters, not only
white space.  Lines that break the gate never enter the tournament.
"""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
CHAR_LIMIT = 120

WEIGHT_WISDOM = 3
WEIGHT_DEVELOPER = 2
WEIGHT_ECONOMY = 2
WEIGHT_FRESHNESS = 1


# Each candidate: (line, wisdom, developer relevance, word economy, freshness)
CANDIDATE_TABLE: tuple[tuple[str, int, int, int, int], ...] = (
    ("Your code will outlive you; write it like a letter to the tired stranger who inherits it.", 8, 8, 6, 7),
    ("The bug you cannot reproduce is the one teaching you patience.", 7, 7, 8, 6),
    ("Ship it Friday, and the weekend will teach you what code review could not.", 7, 8, 7, 7),
    ("Every legacy system was once a clever shortcut someone was proud of.", 9, 9, 8, 8),
    ("The best debugger is a good night's sleep; the second best is deleting the code.", 6, 7, 7, 6),
    ("Your estimate was a wish; the deadline is a rumor; the code is the truth.", 8, 8, 7, 7),
    ("A comment that lies is worse than silence; code that lies is worse than both.", 7, 7, 6, 6),
    ("The senior engineer you admire once deleted production too — and stayed to fix it.", 8, 9, 7, 9),
    ("Rubber-duck your problem aloud; the duck never judges, the bug always confesses.", 6, 8, 6, 5),
    ("Refactor not when the code is ugly, but when the next reader will misunderstand it.", 8, 8, 6, 7),
)


def tally_marks(wisdom: int, developer: int, economy: int, freshness: int) -> int:
    """Weighted total of one candidate's four axis marks."""
    return (
        wisdom * WEIGHT_WISDOM
        + developer * WEIGHT_DEVELOPER
        + economy * WEIGHT_ECONOMY
        + freshness * WEIGHT_FRESHNESS
    )


def gate_reason(line: str) -> str:
    """Return a reason when a line breaks the gate, or an empty string."""
    trimmed = line.strip()
    if trimmed == "":
        return "blank line"
    if len(line) > CHAR_LIMIT:
        return f"{len(line)} characters, over the {CHAR_LIMIT} limit"
    if line != trimmed:
        return "leading or trailing white space"
    return ""


def build_scorecard() -> list[dict[str, object]]:
    """Score every candidate, dropping any line the gate refuses."""
    scorecard: list[dict[str, object]] = []
    for line, wisdom, developer, economy, freshness in CANDIDATE_TABLE:
        reason = gate_reason(line)
        if reason:
            print(f"skipped a candidate the gate refuses ({reason}): {line}")
        scorecard.append(
            {
                "text": line,
                "wisdom": wisdom,
                "developer": developer,
                "economy": economy,
                "freshness": freshness,
                "total": tally_marks(wisdom, developer, economy, freshness),
                "gate_ok": reason == "",
            }
        )
    return [row for row in scorecard if row["gate_ok"]]


def crown_winner(scorecard: list[dict[str, object]]) -> dict[str, object]:
    """Pick the highest total; ties go to the shorter line, then the text."""
    ranked = sorted(
        scorecard,
        key=lambda row: (-int(row["total"]), len(str(row["text"])), str(row["text"])),
    )
    return ranked[0]


AXIS_NOTES: dict[str, str] = {
    "wisdom": "says something true and worth carrying past the moment",
    "developer": "belongs to a developer's day: bugs, reviews, deploys, estimates, legacy code",
    "economy": "one short balanced sentence that lands in a single breath",
    "freshness": "turns the truth in a way the reader has not heard before",
}


def strongest_axes(winner: dict[str, object]) -> list[str]:
    """Name the axes where the winner scored highest, best first."""
    marks = [
        ("wisdom", int(winner["wisdom"])),
        ("developer", int(winner["developer"])),
        ("economy", int(winner["economy"])),
        ("freshness", int(winner["freshness"])),
    ]
    ordered = sorted(marks, key=lambda pair: (-pair[1], pair[0]))
    return [axis for axis, _ in ordered]


def explain_win(winner: dict[str, object]) -> str:
    """One paragraph on why the winning line won, axis by axis."""
    lines = [f"Winner: {winner['text']} (total {winner['total']})."]
    for axis in strongest_axes(winner):
        lines.append(f"- {axis} ({winner[axis]}/10): {AXIS_NOTES[axis]}.")
    return "\n".join(lines)


def validate_scorecard(scorecard: list[dict[str, object]]) -> str:
    """Sanity-check the scorecard before crowning a winner.

    Returns an empty string when the scorecard is sound, or a short
    reason when something is off: duplicate lines, marks outside 0-10,
    or a total that does not match the four marks.
    """
    seen: set[str] = set()
    for row in scorecard:
        text = str(row["text"])
        if text in seen:
            return f"duplicate candidate line: {text}"
        seen.add(text)
        for axis in ("wisdom", "developer", "economy", "freshness"):
            mark = int(row[axis])
            if mark < 0 or mark > 10:
                return f"mark {mark} for {axis} is outside 0-10: {text}"
        expected = tally_marks(
            int(row["wisdom"]),
            int(row["developer"]),
            int(row["economy"]),
            int(row["freshness"]),
        )
        if int(row["total"]) != expected:
            return f"total mismatch for line: {text}"
    return ""


def render_standings(scorecard: list[dict[str, object]], winner: dict[str, object]) -> str:
    """Render the standings as a JSON audit trail for stdout."""
    ranked = sorted(
        scorecard,
        key=lambda row: (-int(row["total"]), len(str(row["text"])), str(row["text"])),
    )
    trail = {
        "candidates": ranked,
        "winner": winner["text"],
        "winner_total": winner["total"],
        "winner_chars": len(str(winner["text"])),
    }
    return json.dumps(trail, indent=2, ensure_ascii=False)


def inscribe_entry(line: str, destination: Path) -> None:
    """Write the winning line as UTF-8 bytes to the destination file."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(line.encode("utf-8"))


def main() -> int:
    """Run the tournament and write the winning line to the entry file."""
    scorecard = build_scorecard()
    if len(scorecard) == 0:
        print("no candidate passed the gate; nothing to write")
        return 1
    problem = validate_scorecard(scorecard)
    if problem:
        print(f"scorecard refused: {problem}")
        return 1
    winner = crown_winner(scorecard)
    winning_line = str(winner["text"])
    inscribe_entry(winning_line, OUTPUT_PATH)
    print(render_standings(scorecard, winner))
    print(explain_win(winner))
    print(f"wrote {len(winning_line)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
